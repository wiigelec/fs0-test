#!/usr/bin/env python3
from __future__ import annotations
import re

SHA_RE = re.compile(r"^[0-9a-f]{40}$")

class GitHubBindingError(ValueError):
    pass

def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())
def _valid_actor(value):
    if not isinstance(value, dict):
        return False
    actor_id = value.get("id")
    return (
        not isinstance(actor_id, bool)
        and isinstance(actor_id, int)
        and actor_id > 0
        and ("login" not in value or _nonempty(value.get("login")))
    )

def _issue_number(value):
    return isinstance(value, int) and value > 0

def validate_governed_issue(issue, expected_stage):
    if expected_stage not in {"design", "plan", "build"}:
        raise GitHubBindingError("invalid governed stage")
    if not isinstance(issue, dict) or issue.get("kind") != "issue":
        raise GitHubBindingError("governed work must use GitHub issue")
    if not _issue_number(issue.get("number")):
        raise GitHubBindingError("governed issue requires positive number")
    work = issue.get("governed_work")
    if not isinstance(work, dict) or work.get("stage") != expected_stage:
        raise GitHubBindingError("issue governed_work stage mismatch")
    if not _nonempty(work.get("work_id")):
        raise GitHubBindingError("issue governed_work requires work_id")
    return issue

def validate_candidate(candidate):
    if not isinstance(candidate, dict):
        raise GitHubBindingError("candidate must be an object")
    if not _nonempty(candidate.get("branch")):
        raise GitHubBindingError("candidate requires branch")
    sha = candidate.get("commit_sha")
    if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
        raise GitHubBindingError("candidate requires exact commit SHA")
    return candidate

def validate_review_surface(pr, candidate):
    candidate = validate_candidate(candidate)
    if not isinstance(pr, dict) or pr.get("kind") != "pull_request":
        raise GitHubBindingError("candidate review surface must be pull request")
    if not _issue_number(pr.get("number")):
        raise GitHubBindingError("pull request requires positive number")
    if pr.get("head_branch") != candidate["branch"]:
        raise GitHubBindingError("pull request head branch mismatch")
    if pr.get("head_sha") != candidate["commit_sha"]:
        raise GitHubBindingError("pull request head SHA mismatch")
    return pr

def validate_bootstrap_provenance_issue(issue):
    if not isinstance(issue, dict) or issue.get("kind") != "issue":
        raise GitHubBindingError("bootstrap provenance must use GitHub issue")
    if not _issue_number(issue.get("number")):
        raise GitHubBindingError("bootstrap provenance issue requires positive number")
    if "governed_work" in issue:
        raise GitHubBindingError("bootstrap provenance must not be governed work")
    auth = issue.get("bootstrap_authorization")
    if not isinstance(auth, dict) or not _valid_actor(auth.get("acceptance_actor")):
        raise GitHubBindingError(
            "bootstrap provenance acceptance_actor requires positive GitHub user id"
        )
    return issue

def resolve_remote_governance_state(snapshot):
    if not isinstance(snapshot, dict):
        raise GitHubBindingError("snapshot must be an object")
    design = validate_governed_issue(snapshot.get("design_issue"), "design")
    plan = validate_governed_issue(snapshot.get("plan_issue"), "plan")
    build = validate_governed_issue(snapshot.get("build_issue"), "build")
    if len({design["number"], plan["number"], build["number"]}) != 3:
        raise GitHubBindingError("Design Plan and Build must use separate issues")
    candidate = validate_candidate(snapshot.get("candidate"))
    pr = validate_review_surface(snapshot.get("pull_request"), candidate)
    dw = design["governed_work"]
    pw = plan["governed_work"]
    bw = build["governed_work"]
    if pw.get("predecessor_id") != dw.get("work_id"):
        raise GitHubBindingError("Plan predecessor mismatch")
    if bw.get("predecessor_id") != pw.get("work_id"):
        raise GitHubBindingError("Build predecessor mismatch")
    acceptance = snapshot.get("acceptance") or {"disposition": "pending"}
    if not isinstance(acceptance, dict):
        raise GitHubBindingError("acceptance must be object")
    status = acceptance.get("disposition", "pending")
    if status not in {"pending", "accepted", "rejected"}:
        raise GitHubBindingError("invalid acceptance disposition")
    resulting = acceptance.get("resulting_accepted_state")
    if resulting is not None and (not isinstance(resulting, str) or not SHA_RE.fullmatch(resulting)):
        raise GitHubBindingError("invalid resulting accepted revision")
    unauthorized = snapshot.get("remaining_unauthorized_work", [])
    if not isinstance(unauthorized, list) or not all(_nonempty(x) for x in unauthorized):
        raise GitHubBindingError("remaining_unauthorized_work must be string list")
    return {
        "active_design_work_id": dw["work_id"],
        "initiating_proposal_id": dw.get("initiating_proposal_id"),
        "normative_delta": dw.get("normative_delta"),
        "accepted_realization_intent": pw.get("candidate_result") if pw.get("disposition") == "accepted" else None,
        "build_work_id": bw["work_id"],
        "revision_under_review": candidate["commit_sha"],
        "candidate_branch": candidate["branch"],
        "pull_request_number": pr["number"],
        "acceptance_status": status,
        "resulting_accepted_revision": resulting,
        "remaining_unauthorized_work": list(unauthorized),
    }

def post_cutover_mutation_allowed(bootstrap_state, governed_build):
    if not isinstance(bootstrap_state, dict):
        raise GitHubBindingError("bootstrap state must be object")
    state = bootstrap_state.get("state")
    if state not in {"candidate", "cutover"}:
        raise GitHubBindingError("invalid bootstrap state")
    if state == "candidate":
        return True
    return (
        isinstance(governed_build, dict)
        and governed_build.get("stage") == "build"
        and governed_build.get("disposition") == "pending"
        and isinstance(governed_build.get("accepted_plan_id"), str)
        and bool(governed_build.get("accepted_plan_id"))
        and isinstance(governed_build.get("bounded_authorization"), dict)
        and bool(governed_build["bounded_authorization"].get("mutation_scope"))
    )
