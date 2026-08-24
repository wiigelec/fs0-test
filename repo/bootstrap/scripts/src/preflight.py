#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def run(args, *, cwd: Path, allowed=(0,)) -> subprocess.CompletedProcess:
    proc = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if proc.returncode not in allowed:
        detail = (proc.stderr or proc.stdout).strip()
        raise SystemExit(
            f"FS0 bootstrap prerequisite failed: {' '.join(args)}"
            + (f": {detail}" if detail else "")
        )
    return proc


def require_command(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(
            f"FS0 bootstrap prerequisite failed: required command not found: {name}"
        )
    return path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="FS0 local bootstrap construction preflight"
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--initial-commit", action="store_true")
    args = parser.parse_args()

    root = Path.cwd().resolve()

    for command in ("git", "python3"):
        require_command(command)

    if args.initial_commit:
        run(["git", "var", "GIT_AUTHOR_IDENT"], cwd=root)
        run(["git", "var", "GIT_COMMITTER_IDENT"], cwd=root)
    else:
        run(["git", "rev-parse", "--git-dir"], cwd=root)
        top = Path(
            run(["git", "rev-parse", "--show-toplevel"], cwd=root).stdout.strip()
        ).resolve()
        if top != root:
            raise SystemExit(
                "FS0 bootstrap prerequisite failed: current directory is not repository root"
            )

    result = {
        "schema_version": "1",
        "record_type": "fs0-local-bootstrap-preflight",
        "initial_commit": args.initial_commit,
        "capabilities": {
            "git_command": True,
            "python_command": True,
            "git_repository_inspection": (
                "deferred-until-initialization"
                if args.initial_commit
                else True
            ),
            "git_local_commit_identity": (
                True if args.initial_commit else "not-required"
            ),
            "maintained_script_execution": True,
        },
        "remote_prerequisites_required": False,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        mode = (
            "initial candidate construction"
            if args.initial_commit
            else "maintenance"
        )
        print(f"FS0 local bootstrap preflight: PASS ({mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
