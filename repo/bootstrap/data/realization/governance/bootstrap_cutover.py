#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BRANCH = "fs0-bootstrap-cutover"
RESULT = Path.home() / "Downloads" / "fs0-bootstrap-cutover-result.json"
TOTAL_STEPS = 16

try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass


def write_result(result):
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


def phase(name):
    print(f"\n===== {name} =====\n", flush=True)


def step(number, phase_name, description):
    print(f"[{number:02d}/{TOTAL_STEPS:02d}] {phase_name} {description}", flush=True)


def passed(detail):
    print("PASS " + detail, flush=True)


def failed(detail):
    print("FAIL " + detail, file=sys.stderr, flush=True)


def run(args, *, input_text=None, allowed=(0,), show=True):
    if show:
        print("$ " + " ".join(args), flush=True)
    proc = subprocess.run(args, text=True, input=input_text, capture_output=True)
    if show:
        for line in proc.stdout.splitlines():
            print("OUT | " + line, flush=True)
        for line in proc.stderr.splitlines():
            print("ERR | " + line, flush=True)
    if proc.returncode not in allowed:
        detail = proc.stderr.strip() or proc.stdout.strip() or "no diagnostic output"
        raise RuntimeError(
            f"{' '.join(args)} failed ({proc.returncode}): {detail}"
        )
    return proc


def git(*args, allowed=(0,), show=True):
    return run(["git", *args], allowed=allowed, show=show)


def gh(endpoint, *, method="GET", payload=None, show=True):
    args = ["gh", "api", endpoint]
    input_text = None
    if method != "GET":
        args += ["--method", method]
    if payload is not None:
        args += ["--input", "-"]
        input_text = json.dumps(payload)
    value = json.loads(run(args, input_text=input_text, show=show).stdout)
    if not isinstance(value, dict):
        raise RuntimeError("GitHub API response is not an object")
    return value


def root():
    value = Path.cwd().resolve()
    if not (value / ".git").exists():
        raise RuntimeError("run from repository root")
    return value


def repo_name():
    raw = git("remote", "get-url", "origin").stdout.strip()
    for prefix in ("https://github.com/", "git@github.com:"):
        if raw.startswith(prefix):
            value = raw[len(prefix):]
            return value[:-4] if value.endswith(".git") else value
    raise RuntimeError(f"unsupported origin URL: {raw}")


def remote_main():
    fields = git(
        "ls-remote", "--heads", "origin", "refs/heads/main"
    ).stdout.split()
    if len(fields) != 2 or fields[1] != "refs/heads/main":
        raise RuntimeError("cannot resolve origin/main")
    return fields[0].lower()


def status_paths():
    proc = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        text=True,
        capture_output=True,
        check=True,
    )
    paths = []
    for raw in proc.stdout.splitlines():
        line = raw.rstrip("\r\n")
        if not line:
            continue
        if len(line) < 4:
            raise RuntimeError(f"unexpected porcelain: {line!r}")
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path)
    return sorted(paths)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def bootstrap_issue_body(base, actor_id, actor_login):
    record = {"schema_version":"1","record_type":"bootstrap-authorization",
              "acceptance_actor":{"id":actor_id,"login":actor_login},
              "accepted_repository_predecessor":base,"accepted_ref":"refs/heads/main"}
    return "# FS0 Bootstrap Provenance\n\nThis issue is the one-time bootstrap work identity and authorization anchor.\n\n```json\n" + json.dumps(record, indent=2) + "\n```\n"

def bootstrap_pr_body(issue_number, candidate, base):
    record = {"schema_version":"1","record_type":"bootstrap-cutover-candidate",
              "bootstrap_provenance_issue":issue_number,"head_sha":candidate,
              "accepted_repository_predecessor":base,"base_ref":"refs/heads/main"}
    return f"Governed by bootstrap provenance issue #{issue_number}.\n\nThis exact PR head is the designated bootstrap-cutover candidate. Merging is bootstrap acceptance only when exact-head remote FS0 Conformance has passed.\n\n```json\n" + json.dumps(record, indent=2) + "\n```\n"



def bootstrap_candidate_binding(issue_number, actor_id, actor_login, base):
    return {
        "schema_version": "1", "record_type": "bootstrap-candidate-binding",
        "bootstrap_provenance_issue": issue_number,
        "acceptance_actor": {"id": actor_id, "login": actor_login},
        "accepted_repository_predecessor": base, "base_ref": "refs/heads/main",
    }


def bootstrap_candidate_commit_message(issue_number, actor_id, actor_login, base):
    return "Bind FS0 bootstrap cutover candidate\n\n```json\n" + json.dumps(bootstrap_candidate_binding(issue_number, actor_id, actor_login, base), indent=2, sort_keys=True) + "\n```\n"


def main():
    parser = argparse.ArgumentParser(
        description="Create the one-time FS0 bootstrap cutover PR."
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = {
        "schema_version": "1",
        "record_type": "bootstrap-cutover-result",
        "status": "error",
        "operation": "bootstrap-cutover",
        "repository": None,
        "branch": "main",
        "expected_base_or_head": None,
        "observed_base_or_head": None,
        "governing_issue": None,
        "files_changed": [],
        "validation_performed": [],
        "validation_results": {},
        "diff_summary": None,
        "commit_sha": None,
        "commit_count": 0,
        "push_mode": "normal-non-force",
        "remote_head": None,
        "candidate_branch": BRANCH,
        "pull_request": None,
        "history_rewrite_or_force_push_occurred": False,
        "merge_occurred": False,
        "errors": [],
        "result_json": str(RESULT),
    }

    write_result(result)
    print("FS0 Script Transfer: START", flush=True)
    print("Operation: bootstrap-cutover", flush=True)
    print("Result JSON: " + str(RESULT), flush=True)

    current_step = 0

    try:
        repo_root = root()

        phase("PRECHECK")

        current_step += 1
        step(current_step, "PRECHECK", "verify repository identity")
        repository = repo_name()
        result["repository"] = repository
        passed(repository)

        current_step += 1
        step(current_step, "PRECHECK", "verify branch, clean worktree, and exact local HEAD")
        branch = git("branch", "--show-current").stdout.strip()
        if branch != "main":
            raise RuntimeError("must start on main")
        dirty = status_paths()
        if dirty:
            raise RuntimeError("working tree must be clean: " + ", ".join(dirty))
        base = git("rev-parse", "HEAD").stdout.strip().lower()
        result["branch"] = branch
        result["expected_base_or_head"] = base
        result["observed_base_or_head"] = base
        passed(f"main @ {base}")

        current_step += 1
        step(current_step, "PRECHECK", "verify origin/main matches local main")
        remote = remote_main()
        if remote != base:
            raise RuntimeError(
                f"local main {base} does not match origin/main {remote}"
            )
        passed(remote)

        current_step += 1
        step(current_step, "PRECHECK", "verify bootstrap candidate state and cutover branch absence")
        state_path = repo_root / "repo/bootstrap/data/state/bootstrap.json"
        state = load(state_path)
        if state.get("state") != "candidate":
            raise RuntimeError("bootstrap state is not candidate")
        existing_branch = git(
            "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"
        ).stdout.strip()
        if existing_branch:
            raise RuntimeError(f"remote branch already exists: {BRANCH}")
        passed("candidate state; cutover branch absent")

        phase("MUTATE")

        current_step += 1
        step(current_step, "MUTATE", "resolve authenticated GitHub actor")
        actor = gh("user")
        actor_id = actor.get("id")
        actor_login = actor.get("login")
        if not isinstance(actor_id, int) or actor_id < 1 or not actor_login:
            raise RuntimeError("authenticated GitHub actor identity is invalid")
        passed(f"{actor_login} ({actor_id})")

        current_step += 1
        step(current_step, "MUTATE", "create bootstrap provenance issue")
        issue = gh(
            f"repos/{repository}/issues",
            method="POST",
            payload={
                "title": "FS0 bootstrap provenance",
                "body": bootstrap_issue_body(base, actor_id, actor_login),
            },
        )
        issue_number = issue.get("number")
        if not isinstance(issue_number, int) or issue_number < 1:
            raise RuntimeError("failed to create provenance issue")
        result["governing_issue"] = issue_number
        passed(f"issue #{issue_number}")

        current_step += 1
        step(current_step, "MUTATE", "create cutover branch and update bootstrap state")
        git("switch", "-c", BRANCH)
        state.update(
            {
                "state": "cutover",
                "bootstrap_provenance_issue": issue_number,
                "accepted_ref": "refs/heads/main",
                "cutover_timestamp": now(),
            }
        )
        save(state_path, state)
        result["files_changed"] = status_paths()
        passed(f"{BRANCH}; bootstrap state -> cutover")

        phase("GENERATE")

        current_step += 1
        step(current_step, "GENERATE", "regenerate canonical repository surfaces")
        run([str(repo_root / "repo/bootstrap/scripts/bootstrap")])
        result["validation_performed"].append("bootstrap generation")
        result["files_changed"] = status_paths()
        passed(f"{len(result['files_changed'])} changed paths")

        phase("VALIDATE")

        current_step += 1
        step(current_step, "VALIDATE", "verify deterministic generation correspondence")
        run([str(repo_root / "repo/bootstrap/scripts/bootstrap"), "--check"])
        result["validation_performed"].append("bootstrap --check")
        passed("generation correspondence")

        current_step += 1
        step(current_step, "VALIDATE", "run canonical FS0 Conformance")
        conformance = run(
            [str(repo_root / "repo/scripts/validate"), "--json"]
        )
        report = json.loads(conformance.stdout)
        result["validation_performed"].append("canonical Conformance")
        result["validation_results"]["canonical"] = report
        if report.get("status") != "pass":
            failed_assertions = [
                item.get("assertion_id")
                for item in report.get("results", [])
                if item.get("status") != "pass"
            ]
            raise RuntimeError(
                "canonical validation failed"
                + (
                    ": " + ", ".join(failed_assertions)
                    if failed_assertions
                    else ""
                )
            )
        passed(
            f"{report.get('passed_assertions', 0)}/"
            f"{report.get('declared_mechanical_assertions', 0)} assertions"
        )

        current_step += 1
        step(current_step, "VALIDATE", "verify whitespace and patch integrity")
        run(["git", "diff", "--check"])
        result["diff_summary"] = run(
            ["git", "diff", "--stat"], show=True
        ).stdout.strip()
        passed("git diff --check")

        phase("COMMIT")

        current_step += 1
        step(current_step, "COMMIT", "stage complete cutover candidate")
        git("add", "-A")
        run(["git", "diff", "--cached", "--check"])
        passed("candidate staged")

        current_step += 1
        step(current_step, "COMMIT", "commit cutover mutation state")
        run(["git", "commit", "-m", "Prepare FS0 bootstrap cutover state"])
        source_candidate = git("rev-parse", "HEAD").stdout.strip().lower()
        result["commit_count"] = 1
        passed(source_candidate)

        current_step += 1
        step(current_step, "COMMIT", "create final bootstrap candidate binding commit")
        run(
            ["git", "commit", "--allow-empty", "-F", "-"],
            input_text=bootstrap_candidate_commit_message(
                issue_number, actor_id, actor_login, base
            ),
        )
        candidate = git("rev-parse", "HEAD").stdout.strip().lower()
        result["commit_sha"] = candidate
        result["commit_count"] = 2
        passed(candidate)

        phase("PUBLISH")

        current_step += 1
        step(current_step, "PUBLISH", "re-check origin/main before candidate publication")
        observed_main = remote_main()
        if observed_main != base:
            raise RuntimeError(
                f"origin/main changed from {base} to {observed_main}"
            )
        passed(observed_main)

        current_step += 1
        step(current_step, "PUBLISH", "push cutover candidate branch non-force")
        git("push", "-u", "origin", BRANCH)
        branch_fields = git(
            "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}"
        ).stdout.split()
        if (
            len(branch_fields) != 2
            or branch_fields[0].lower() != candidate
            or branch_fields[1] != f"refs/heads/{BRANCH}"
        ):
            raise RuntimeError("remote cutover branch does not resolve to candidate")
        result["remote_head"] = candidate
        passed(candidate)

        current_step += 1
        step(current_step, "PUBLISH", "open designated bootstrap-cutover pull request")
        pr = gh(
            f"repos/{repository}/pulls",
            method="POST",
            payload={
                "title": "FS0 bootstrap cutover",
                "head": BRANCH,
                "base": "main",
                "body": bootstrap_pr_body(issue_number, candidate, base),
            },
        )
        pr_number = pr.get("number")
        pr_url = pr.get("html_url")
        if not isinstance(pr_number, int) or pr_number < 1 or not pr_url:
            raise RuntimeError("pull request creation did not return valid identity")
        result["pull_request"] = {
            "number": pr_number,
            "url": pr_url,
            "head_sha": candidate,
        }
        passed(f"PR #{pr_number}: {pr_url}")

        phase("VERIFY")

        current_step += 1
        step(current_step, "VERIFY", "verify PR head and confirm main is untouched")
        verify_pr = gh(f"repos/{repository}/pulls/{pr_number}")
        pr_head = verify_pr.get("head", {}).get("sha")
        pr_base = verify_pr.get("base", {}).get("ref")
        final_main = remote_main()
        if pr_head != candidate:
            raise RuntimeError("PR head does not match candidate")
        if pr_base != "main":
            raise RuntimeError("PR base is not main")
        if final_main != base:
            raise RuntimeError("main changed during bootstrap cutover preparation")
        if status_paths():
            raise RuntimeError("worktree is dirty after cutover candidate publication")
        passed(
            f"PR head {candidate}; origin/main unchanged at {base}"
        )

        result["status"] = "awaiting-merge"
        write_result(result)

        print("\nFS0 Script Transfer: PASS", flush=True)
        print("Operation: bootstrap-cutover", flush=True)
        print("Repository: " + repository, flush=True)
        print("Branch: " + BRANCH, flush=True)
        print("Expected HEAD: " + base, flush=True)
        print("Observed HEAD: " + base, flush=True)
        print("Files Changed: " + str(len(result["files_changed"])), flush=True)
        print(
            "Validation: "
            + str(report.get("passed_assertions", 0))
            + "/"
            + str(report.get("declared_mechanical_assertions", 0))
            + " PASS",
            flush=True,
        )
        print("Commit: " + candidate, flush=True)
        print("Remote HEAD: " + candidate, flush=True)
        print("Result JSON: " + str(RESULT), flush=True)
        print("", flush=True)
        print("Bootstrap cutover candidate is ready.", flush=True)
        print(f"PR: {pr_url}", flush=True)
        print("Status: AWAITING USER MERGE", flush=True)
        return 0

    except Exception as exc:
        result["errors"].append(str(exc))
        write_result(result)
        failed(str(exc))
        print("FS0 Script Transfer: FAILED", flush=True)
        print("Operation: bootstrap-cutover", flush=True)
        print("Repository: " + str(result.get("repository")), flush=True)
        print("Branch: " + str(result.get("branch")), flush=True)
        print(
            "Expected HEAD: " + str(result.get("expected_base_or_head")),
            flush=True,
        )
        print(
            "Observed HEAD: " + str(result.get("observed_base_or_head")),
            flush=True,
        )
        print("Files Changed: " + str(len(result.get("files_changed", []))), flush=True)
        print("Commit: " + str(result.get("commit_sha")), flush=True)
        print("Remote HEAD: " + str(result.get("remote_head")), flush=True)
        print("Result JSON: " + str(RESULT), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
