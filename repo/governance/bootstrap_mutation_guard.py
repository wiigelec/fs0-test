#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit("FS0 post-cutover mutation guard: " + message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing required record: {path}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON {path}: {exc}")


def load_committed_json(root: Path, rel: str):
    proc = subprocess.run(
        ["git", "show", f"HEAD:{rel}"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        fail(f"unable to resolve committed authorization record {rel}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        fail(f"committed authorization record is invalid JSON {rel}: {exc}")


def load_module(path: Path, name: str):
    if not path.is_file():
        fail(f"required Governance realization is missing: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dirty_guarded_paths(root: Path, protected_record: str):
    proc = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        fail("unable to inspect repository mutation state")
    paths = []
    for line in proc.stdout.splitlines():
        if len(line) < 4:
            continue
        rel = line[3:]
        if rel.startswith("repo/bootstrap/") or rel == protected_record:
            paths.append(rel)
    return sorted(set(paths))


def gh_json(root: Path, endpoint: str):
    proc = subprocess.run(
        ["gh", "api", endpoint],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        fail(
            "GitHub Governance resolution failed for "
            + endpoint
            + ": "
            + (proc.stderr.strip() or proc.stdout.strip())
        )
    try:
        value = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        fail(f"GitHub API returned invalid JSON for {endpoint}: {exc}")
    return value


def resolve_plan_issue(accepted_state, repo: str, accepted_plan_id: str):
    matches = []
    for issue in accepted_state.github_issues(repo):
        body = issue.get("body")
        try:
            work = accepted_state.governed_work_from_issue_body(body)
        except Exception:
            continue
        if work.get("work_id") == accepted_plan_id:
            matches.append((issue, work))
    if len(matches) != 1:
        fail("accepted_plan_id must resolve to exactly one Governance Plan issue")
    return matches[0]


def recovery_authority_required(policy, changed_paths):
    protected = set(policy.get("protected_paths", []))
    return bool(protected & set(changed_paths))


def recovery_authority_allowed(policy, plan, changed_paths):
    if not recovery_authority_required(policy, changed_paths):
        return True
    purposes = set(policy.get("permitted_authority_purposes", []))
    return plan.get("authority_purpose") in purposes


def validate_policy(policy):
    if (
        not isinstance(policy, dict)
        or policy.get("schema_version") != "1"
        or policy.get("record_type") != "bootstrap-recovery-authority-policy"
        or policy.get("authority_stage") != "plan"
        or policy.get("required_disposition") != "accepted"
    ):
        fail("committed bootstrap recovery authority policy is invalid")
    protected = policy.get("protected_paths")
    purposes = policy.get("permitted_authority_purposes")
    if (
        not isinstance(protected, list)
        or not protected
        or not all(isinstance(x, str) and x for x in protected)
        or not isinstance(purposes, list)
        or set(purposes) != {"bootstrap-recovery", "bootstrap-reconstruction"}
    ):
        fail("committed bootstrap recovery authority policy is incomplete")
    if policy.get("cutover_record") not in protected:
        fail("recovery policy does not protect its cutover record")
    if policy.get("canonical_cutover_source") not in protected:
        fail("recovery policy does not protect canonical cutover state source")
    return policy


def committed_head_exists(root: Path) -> bool:
    proc = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD^{commit}"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    return proc.returncode == 0


def committed_object_exists(root: Path, rel: str) -> bool:
    if not committed_head_exists(root):
        return False
    proc = subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{rel}"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    return proc.returncode == 0


def authorize_preinstallation(root: Path, protected_record: str):
    canonical_rel = "repo/bootstrap/data/state/bootstrap.json"
    canonical = load_json(root / canonical_rel)
    if (
        canonical.get("schema_version") != "1"
        or canonical.get("record_type") != "bootstrap-state"
        or canonical.get("state") != "candidate"
    ):
        fail(
            "retained bootstrap pre-installation state must be a canonical candidate"
        )

    # If committed FS0 bootstrap material exists, absence of the committed
    # installed state is an inconsistent existing installation, not a fresh target.
    if committed_object_exists(root, "repo/bootstrap"):
        fail(
            "committed FS0 bootstrap material exists without committed "
            "repo/state/bootstrap.json"
        )

    changed = dirty_guarded_paths(root, protected_record)
    return {
        "schema_version": "1",
        "record_type": "bootstrap-mutation-authorization",
        "state": "candidate",
        "authorized": True,
        "governance_work_id": None,
        "changed_guarded_paths": changed,
        "recovery_authority_required": False,
        "authority_source": canonical_rel,
        "preinstallation": True,
    }


def authorize(root: Path):
    protected_record = "repo/state/bootstrap.json"

    if not committed_object_exists(root, protected_record):
        return authorize_preinstallation(root, protected_record)

    committed_state = load_committed_json(root, protected_record)
    if (
        committed_state.get("schema_version") != "1"
        or committed_state.get("record_type") != "bootstrap-state"
    ):
        fail("committed bootstrap state has invalid envelope")

    lifecycle = committed_state.get("state")
    changed = dirty_guarded_paths(root, protected_record)

    if lifecycle == "candidate":
        return {
            "schema_version": "1",
            "record_type": "bootstrap-mutation-authorization",
            "state": "candidate",
            "authorized": True,
            "governance_work_id": None,
            "changed_guarded_paths": changed,
            "recovery_authority_required": False,
            "authority_source": f"HEAD:{protected_record}",
            "preinstallation": False,
        }

    if lifecycle != "cutover":
        fail("committed bootstrap state is neither candidate nor cutover")

    policy_rel = "repo/bootstrap/data/bootstrap_recovery_authority.json"
    policy = validate_policy(load_committed_json(root, policy_rel))
    protected_record = policy["cutover_record"]
    changed = dirty_guarded_paths(root, protected_record)

    if not changed:
        return {
            "schema_version": "1",
            "record_type": "bootstrap-mutation-authorization",
            "state": "cutover",
            "authorized": True,
            "governance_work_id": None,
            "changed_guarded_paths": [],
            "recovery_authority_required": False,
            "authority_source": f"HEAD:{protected_record}",
            "preinstallation": False,
        }

    issue_raw = os.environ.get("FS0_GOVERNED_BUILD_ISSUE")
    try:
        build_issue_number = int(issue_raw) if issue_raw is not None else 0
    except ValueError:
        build_issue_number = 0
    if build_issue_number < 1:
        fail(
            "cutover bootstrap mutation requires FS0_GOVERNED_BUILD_ISSUE "
            "naming the pending Governance Build issue"
        )

    work_module = load_module(
        root / "repo/governance/work.py",
        "fs0_governance_work",
    )
    accepted_state = load_module(
        root / "repo/governance/accepted_state.py",
        "fs0_accepted_state",
    )

    repo = accepted_state.origin_repository(root)
    build_issue = gh_json(
        root,
        f"repos/{repo}/issues/{build_issue_number}",
    )
    if not isinstance(build_issue, dict) or "pull_request" in build_issue:
        fail("FS0_GOVERNED_BUILD_ISSUE must identify a GitHub issue")

    try:
        build_record = accepted_state.governed_work_from_issue_body(
            build_issue.get("body")
        )
        build = work_module.validate_work(dict(build_record))
    except Exception as exc:
        fail(f"Governance Build issue is invalid: {exc}")

    if build.get("stage") != "build":
        fail("post-cutover mutation requires Governance Build work")
    if build.get("disposition") != "pending":
        fail(
            "post-cutover mutation is authorized only while Build is pending"
        )

    accepted_plan_id = build.get("accepted_plan_id")
    if not isinstance(accepted_plan_id, str) or not accepted_plan_id:
        fail("Governance Build does not identify an accepted Plan")
    if build.get("predecessor_id") != accepted_plan_id:
        fail(
            "Governance Build predecessor does not match accepted_plan_id"
        )

    plan_issue, plan_record = resolve_plan_issue(
        accepted_state,
        repo,
        accepted_plan_id,
    )
    try:
        plan = work_module.validate_work(dict(plan_record))
    except Exception as exc:
        fail(f"resolved Governance Plan issue is invalid: {exc}")

    if plan.get("stage") != "plan":
        fail(
            "accepted_plan_id does not resolve to Governance Plan work"
        )
    plan_scope = plan.get(
        "realization_intent", {}
    ).get("build_scope", [])
    if not set(build.get("scope", [])) <= set(plan_scope):
        fail(
            "Governance Build scope exceeds accepted Plan build_scope"
        )

    pull_requests = accepted_state.github_pull_requests_for_issue(
        repo,
        plan_issue.get("number"),
    )
    plan_acceptance = accepted_state.resolve_governance_work_acceptance(
        plan_issue.get("body"),
        pull_requests,
        "plan",
        accepted_plan_id,
    )
    if plan_acceptance.get("status") != "accepted":
        fail(
            "resolved Governance Plan lacks authorized merged-PR acceptance"
        )

    if not recovery_authority_allowed(
        policy,
        plan,
        changed,
    ):
        fail(
            "bootstrap cutover record/source mutation requires accepted Plan "
            "authority_purpose bootstrap-recovery|bootstrap-reconstruction"
        )

    scope = build.get(
        "bounded_authorization", {}
    ).get("mutation_scope", [])
    missing = [
        path for path in changed if path not in scope
    ]
    if missing:
        fail(
            "Governance Build mutation_scope does not authorize guarded paths: "
            + ", ".join(missing)
        )

    return {
        "schema_version": "1",
        "record_type": "bootstrap-mutation-authorization",
        "state": "cutover",
        "authorized": True,
        "governance_work_id": build.get("work_id"),
        "governance_issue_number": build_issue_number,
        "accepted_plan_id": accepted_plan_id,
        "accepted_plan_issue_number": plan_issue.get("number"),
        "plan_acceptance_pr_number": plan_acceptance[
            "acceptance_records"
        ][0]["pull_request_number"],
        "authority_purpose": plan.get("authority_purpose"),
        "changed_guarded_paths": changed,
        "recovery_authority_required": (
            recovery_authority_required(policy, changed)
        ),
        "authority_source": f"HEAD:{protected_record}",
        "preinstallation": False,
    }




def main() -> int:
    root = Path.cwd().resolve()
    if not (root / ".git").exists():
        fail("must be invoked from repository root")
    report = authorize(root)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
