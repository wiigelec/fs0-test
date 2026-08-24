#!/usr/bin/env python3
from __future__ import annotations
from copy import deepcopy
import re

STAGE_STEPS = {
    "design": ["audit", "normalize", "accept"],
    "plan": ["analyze", "specify", "accept"],
    "build": ["implement", "verify", "accept"],
}
DISPOSITIONS = {"pending", "accepted", "rejected"}
ADVERSE_FINDINGS = {"defect", "insufficient", "governance-required"}

class GovernanceWorkError(ValueError):
    pass

def _nonempty(v):
    return isinstance(v, str) and bool(v.strip())
def _valid_actor(v):
    if not isinstance(v, dict):
        return False
    actor_id = v.get("id")
    return (
        not isinstance(actor_id, bool)
        and isinstance(actor_id, int)
        and actor_id > 0
        and ("login" not in v or _nonempty(v.get("login")))
    )

def _string_list(v, nonempty=False):
    return isinstance(v, list) and (bool(v) or not nonempty) and all(_nonempty(x) for x in v)

def validate_work(r):
    common = {
        "schema_version", "record_type", "stage", "stage_steps", "work_id",
        "predecessor_id", "scope", "material_exclusions", "candidate_result",
        "completion_conditions", "disposition", "provenance", "bounded_authorization",
        "required_assurance_obligation_ids",
    }
    if not isinstance(r, dict) or not common <= set(r):
        raise GovernanceWorkError("governed work lacks required fields")
    if r["schema_version"] != "1" or r["record_type"] != "governed-work":
        raise GovernanceWorkError("invalid governed-work envelope")
    stage = r.get("stage")
    if stage not in STAGE_STEPS or r.get("stage_steps") != STAGE_STEPS[stage]:
        raise GovernanceWorkError("invalid stage or stage_steps")
    if not _nonempty(r.get("work_id")) or not _nonempty(r.get("predecessor_id")):
        raise GovernanceWorkError("work_id and predecessor_id are required")
    if not _string_list(r.get("scope"), True):
        raise GovernanceWorkError("scope must be non-empty")
    if not _string_list(r.get("material_exclusions")):
        raise GovernanceWorkError("material_exclusions must be a string list")
    if not isinstance(r.get("candidate_result"), dict) or not r["candidate_result"]:
        raise GovernanceWorkError("candidate_result must be non-empty")
    if not _string_list(r.get("completion_conditions"), True):
        raise GovernanceWorkError("completion_conditions must be non-empty")
    if r.get("disposition") not in DISPOSITIONS:
        raise GovernanceWorkError("invalid disposition")
    if not isinstance(r.get("provenance"), dict) or not r["provenance"]:
        raise GovernanceWorkError("provenance must be non-empty")
    auth = r.get("bounded_authorization")
    if not isinstance(auth, dict) or not _valid_actor(auth.get("acceptance_actor")):
        raise GovernanceWorkError("bounded_authorization.acceptance_actor requires positive GitHub user id")
    if not _string_list(auth.get("mutation_scope", [])):
        raise GovernanceWorkError("mutation_scope must be a string list")
    if not set(auth.get("mutation_scope", [])) <= set(r["scope"]):
        raise GovernanceWorkError("mutation_scope exceeds work scope")
    required_assurance = r.get("required_assurance_obligation_ids")
    if not _string_list(required_assurance):
        raise GovernanceWorkError("required_assurance_obligation_ids must be a string list")
    if len(required_assurance) != len(set(required_assurance)):
        raise GovernanceWorkError("required_assurance_obligation_ids must be unique")
    if stage == "design":
        if not _nonempty(r.get("initiating_proposal_id")) or not isinstance(r.get("normative_delta"), dict):
            raise GovernanceWorkError("Design requires initiating proposal and normative_delta")
    elif stage == "plan":
        if not _nonempty(r.get("accepted_design_id")):
            raise GovernanceWorkError("Plan requires accepted_design_id")
        intent = r.get("realization_intent")
        fields = {"affected_artifacts", "conformance_work", "assurance_work", "dependencies", "sequencing", "build_scope"}
        if not isinstance(intent, dict) or not fields <= set(intent):
            raise GovernanceWorkError("Plan realization_intent incomplete")
        if any(not _string_list(intent.get(f)) for f in fields) or not intent["build_scope"]:
            raise GovernanceWorkError("Plan realization_intent fields invalid")
        if sorted(intent.get("assurance_work", [])) != sorted(required_assurance):
            raise GovernanceWorkError("Plan realization_intent.assurance_work must equal required_assurance_obligation_ids")
    else:
        if not _nonempty(r.get("accepted_plan_id")):
            raise GovernanceWorkError("Build requires accepted_plan_id")
        verification = r.get("verification")
        if not isinstance(verification, dict) or not _string_list(verification.get("evidence"), True):
            raise GovernanceWorkError("Build verification evidence required")
        if verification.get("conformance_status") not in {"pending", "pass", "fail"}:
            raise GovernanceWorkError("invalid Build conformance_status")
    return r

def create_design(work_id, proposal_id, scope, candidate_result, completion_conditions,
                  provenance, bounded_authorization, normative_delta, material_exclusions=None,
                  required_assurance_obligation_ids=None):
    return validate_work({
        "schema_version": "1", "record_type": "governed-work", "stage": "design",
        "stage_steps": STAGE_STEPS["design"], "work_id": work_id, "predecessor_id": proposal_id,
        "scope": list(scope), "material_exclusions": list(material_exclusions or []),
        "candidate_result": deepcopy(candidate_result), "completion_conditions": list(completion_conditions),
        "disposition": "pending", "provenance": deepcopy(provenance),
        "bounded_authorization": deepcopy(bounded_authorization),
        "required_assurance_obligation_ids": list(required_assurance_obligation_ids or []),
        "initiating_proposal_id": proposal_id, "normative_delta": deepcopy(normative_delta),
    })

def create_plan(work_id, accepted_design, scope, candidate_result, completion_conditions,
                provenance, bounded_authorization, realization_intent, material_exclusions=None,
                required_assurance_obligation_ids=None):
    d = validate_work(dict(accepted_design))
    if d["stage"] != "design" or d["disposition"] != "accepted":
        raise GovernanceWorkError("Plan requires accepted Design")
    required = list(realization_intent.get("assurance_work", []) if required_assurance_obligation_ids is None else required_assurance_obligation_ids)
    return validate_work({
        "schema_version": "1", "record_type": "governed-work", "stage": "plan",
        "stage_steps": STAGE_STEPS["plan"], "work_id": work_id, "predecessor_id": d["work_id"],
        "scope": list(scope), "material_exclusions": list(material_exclusions or []),
        "candidate_result": deepcopy(candidate_result), "completion_conditions": list(completion_conditions),
        "disposition": "pending", "provenance": deepcopy(provenance),
        "bounded_authorization": deepcopy(bounded_authorization),
        "required_assurance_obligation_ids": required,
        "accepted_design_id": d["work_id"], "realization_intent": deepcopy(realization_intent),
    })

def create_build(work_id, accepted_plan, scope, candidate_result, completion_conditions,
                 provenance, bounded_authorization, evidence, material_exclusions=None,
                 required_assurance_obligation_ids=None):
    p = validate_work(dict(accepted_plan))
    if p["stage"] != "plan" or p["disposition"] != "accepted":
        raise GovernanceWorkError("Build requires accepted Plan")
    if not set(scope) <= set(p["realization_intent"]["build_scope"]):
        raise GovernanceWorkError("Build scope exceeds accepted Plan build_scope")
    required = list(p["required_assurance_obligation_ids"] if required_assurance_obligation_ids is None else required_assurance_obligation_ids)
    return validate_work({
        "schema_version": "1", "record_type": "governed-work", "stage": "build",
        "stage_steps": STAGE_STEPS["build"], "work_id": work_id, "predecessor_id": p["work_id"],
        "scope": list(scope), "material_exclusions": list(material_exclusions or []),
        "candidate_result": deepcopy(candidate_result), "completion_conditions": list(completion_conditions),
        "disposition": "pending", "provenance": deepcopy(provenance),
        "bounded_authorization": deepcopy(bounded_authorization),
        "required_assurance_obligation_ids": required,
        "accepted_plan_id": p["work_id"],
        "verification": {"evidence": list(evidence), "conformance_status": "pending"},
    })

def record_conformance(work, status):
    r = deepcopy(validate_work(dict(work)))
    if r["stage"] != "build" or status not in {"pass", "fail"}:
        raise GovernanceWorkError("Build Conformance status must be pass|fail")
    r["verification"]["conformance_status"] = status
    return validate_work(r)

def _case_status(case_id, findings):
    relevant = [x for x in findings if isinstance(x, dict) and x.get("case_id") == case_id]
    if not relevant:
        return "missing"
    seqs = [x.get("sequence") for x in relevant]
    if any(not isinstance(x, int) or x < 1 for x in seqs) or len(seqs) != len(set(seqs)):
        raise GovernanceWorkError("invalid finding sequence")
    latest = max(relevant, key=lambda x: x["sequence"])
    if latest.get("status") == "satisfied":
        return "resolved"
    if latest.get("status") in ADVERSE_FINDINGS:
        return "adverse"
    raise GovernanceWorkError("invalid finding status")

def assurance_gate(triggered_obligation_ids, cases, findings):
    grouped = {}
    for case in cases:
        if not isinstance(case, dict) or not _nonempty(case.get("review_obligation_id")) or not _nonempty(case.get("case_id")):
            raise GovernanceWorkError("invalid Assurance case")
        grouped.setdefault(case["review_obligation_id"], []).append(case)
    missing = [oid for oid in triggered_obligation_ids if len(grouped.get(oid, [])) != 1]
    if missing:
        return {"eligible": False, "reason": "missing-or-ambiguous-required-case", "obligation_ids": missing}
    adverse = []
    for oid in triggered_obligation_ids:
        if _case_status(grouped[oid][0]["case_id"], findings) != "resolved":
            adverse.append(oid)
    if adverse:
        return {"eligible": False, "reason": "unresolved-adverse-assurance", "obligation_ids": adverse}
    return {"eligible": True, "reason": "satisfied", "obligation_ids": []}

def acceptance_eligibility(
    work, triggered_obligation_ids, candidate_audit=None,
    candidate_conformance_status="pass",
):
    r = validate_work(dict(work))
    required = r["required_assurance_obligation_ids"]
    if sorted(set(triggered_obligation_ids)) != sorted(required):
        return {
            "eligible": False, "reason": "assurance-obligation-set-mismatch",
            "obligation_ids": sorted(set(required) ^ set(triggered_obligation_ids)),
        }
    if candidate_conformance_status != "pass":
        return {"eligible": False, "reason": "conformance-not-passing", "obligation_ids": []}
    if r["stage"] == "build" and r["verification"]["conformance_status"] == "fail":
        return {"eligible": False, "reason": "conformance-not-passing", "obligation_ids": []}
    if required:
        if (
            not isinstance(candidate_audit, dict)
            or candidate_audit.get("status") != "pass"
            or candidate_audit.get("basis") != "candidate-semantic-audit-receipt"
            or sorted(candidate_audit.get("required_obligation_ids", [])) != sorted(required)
        ):
            return {"eligible": False, "reason": "semantic-audit-not-satisfied", "obligation_ids": list(required)}
    return {
        "eligible": True, "reason": "eligible-for-authorized-merge",
        "obligation_ids": [], "semantic_audit_required": bool(required),
    }


def decide(work, disposition, triggered_obligation_ids, cases, findings):
    if disposition not in {"accepted", "rejected"}:
        raise GovernanceWorkError("decision must be accepted|rejected")
    r = deepcopy(validate_work(dict(work)))
    if r["disposition"] != "pending":
        raise GovernanceWorkError("work already decided")
    if disposition == "accepted":
        raise GovernanceWorkError("accepted disposition is established only by authorized governed PR merge")
    r["disposition"] = "rejected"
    return validate_work(r)


def apply_merge_acceptance(work, acceptance):
    r = deepcopy(validate_work(dict(work)))
    if r["disposition"] != "pending":
        raise GovernanceWorkError("work already decided")
    required = {
        "schema_version", "record_type", "status", "work_id", "issue_number",
        "candidate_head", "accepted_repository_predecessor",
        "resulting_accepted_revision", "actor", "eligibility",
    }
    if not isinstance(acceptance, dict) or not required <= set(acceptance):
        raise GovernanceWorkError("merge acceptance proof is incomplete")
    if (
        acceptance.get("schema_version") != "1"
        or acceptance.get("record_type") != "governed-pr-acceptance"
        or acceptance.get("status") != "accepted"
        or acceptance.get("work_id") != r["work_id"]
    ):
        raise GovernanceWorkError("merge acceptance proof does not match governed work")
    expected = r["bounded_authorization"]["acceptance_actor"]
    actor = acceptance.get("actor")
    if not _valid_actor(actor) or actor.get("id") != expected.get("id"):
        raise GovernanceWorkError("merge acceptance actor is not authorized")
    for key in ("candidate_head", "accepted_repository_predecessor", "resulting_accepted_revision"):
        value = acceptance.get(key)
        if not isinstance(value, str) or not SHA_RE.fullmatch(value):
            raise GovernanceWorkError(f"merge acceptance {key} must be exact Git SHA")
    eligibility = acceptance.get("eligibility")
    if not isinstance(eligibility, dict) or eligibility.get("status") != "pass":
        raise GovernanceWorkError("merge acceptance proof lacks passing eligibility")
    if not isinstance(eligibility.get("conformance"), dict) or eligibility["conformance"].get("status") != "pass":
        raise GovernanceWorkError("merge acceptance Conformance proof is not passing")
    assurance = eligibility.get("assurance")
    if (
        not isinstance(assurance, dict)
        or assurance.get("status") != "pass"
        or assurance.get("basis") != "authorized-pr-merge"
        or sorted(assurance.get("required_obligation_ids", [])) != sorted(r["required_assurance_obligation_ids"])
    ):
        raise GovernanceWorkError("merge acceptance Assurance disposition does not match governed work")
    if r["required_assurance_obligation_ids"]:
        audit = assurance.get("audit_receipt")
        if not isinstance(audit, dict) or audit.get("status") != "pass" or audit.get("basis") != "candidate-semantic-audit-receipt":
            raise GovernanceWorkError("merge acceptance lacks satisfactory candidate audit receipt")
    r["disposition"] = "accepted"
    return validate_work(r)


SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")

def validate_pr_candidate(work, candidate):
    r = validate_work(dict(work))
    required = {
        "schema_version", "record_type", "work_id", "issue_number",
        "head_sha", "accepted_repository_predecessor", "base_ref",
    }
    if not isinstance(candidate, dict) or set(candidate) != required:
        raise GovernanceWorkError("governed PR candidate fields mismatch")
    if candidate["schema_version"] != "1" or candidate["record_type"] != "governed-pr-candidate":
        raise GovernanceWorkError("invalid governed PR candidate envelope")
    if candidate["work_id"] != r["work_id"] or not isinstance(candidate["work_id"], str):
        raise GovernanceWorkError("PR must identify exactly one matching governed work item")
    issue = candidate["issue_number"]
    if isinstance(issue, bool) or not isinstance(issue, int) or issue < 1:
        raise GovernanceWorkError("PR issue_number must be a positive integer")
    for key in ("head_sha", "accepted_repository_predecessor"):
        value = candidate[key]
        if not isinstance(value, str) or not SHA_RE.fullmatch(value):
            raise GovernanceWorkError(f"{key} must be an exact Git commit SHA")
    if candidate["base_ref"] != "refs/heads/main":
        raise GovernanceWorkError("governed PR must target refs/heads/main")
    out = deepcopy(candidate)
    out["head_sha"] = out["head_sha"].lower()
    out["accepted_repository_predecessor"] = out["accepted_repository_predecessor"].lower()
    return out

def merge_acceptance(
    work, candidate, merge_event, triggered_obligation_ids,
    candidate_audit=None, candidate_conformance_status="pass",
):
    r = validate_work(dict(work))
    pr = validate_pr_candidate(r, candidate)
    gate = acceptance_eligibility(
        r, triggered_obligation_ids, candidate_audit=candidate_audit,
        candidate_conformance_status=candidate_conformance_status,
    )
    if not gate["eligible"]:
        raise GovernanceWorkError("merge acceptance blocked: " + gate["reason"])
    if not isinstance(merge_event, dict):
        raise GovernanceWorkError("merge event must be a record")
    required = {"merged", "actor", "head_sha", "base_sha", "resulting_revision"}
    if set(merge_event) != required or merge_event.get("merged") is not True:
        raise GovernanceWorkError("merge event is not an accepted merge")
    actor = merge_event.get("actor")
    expected = r["bounded_authorization"]["acceptance_actor"]
    if not _valid_actor(actor) or actor.get("id") != expected.get("id"):
        raise GovernanceWorkError("merge actor is not authorized acceptance_actor")
    for key in ("head_sha", "base_sha", "resulting_revision"):
        value = merge_event.get(key)
        if not isinstance(value, str) or not SHA_RE.fullmatch(value):
            raise GovernanceWorkError(f"merge event {key} must be an exact Git commit SHA")
    if merge_event["head_sha"].lower() != pr["head_sha"]:
        raise GovernanceWorkError("merged head does not equal evaluated PR head")
    if merge_event["base_sha"].lower() != pr["accepted_repository_predecessor"]:
        raise GovernanceWorkError("merged base does not equal accepted repository predecessor")
    assurance = {
        "status": "pass", "basis": "authorized-pr-merge",
        "required_obligation_ids": list(r["required_assurance_obligation_ids"]),
        "audit_receipt": candidate_audit,
    }
    return {
        "schema_version": "1", "record_type": "governed-pr-acceptance",
        "status": "accepted", "work_id": r["work_id"], "issue_number": pr["issue_number"],
        "candidate_head": pr["head_sha"],
        "accepted_repository_predecessor": pr["accepted_repository_predecessor"],
        "resulting_accepted_revision": merge_event["resulting_revision"].lower(),
        "actor": deepcopy(actor),
        "eligibility": {
            "status": "pass",
            "conformance": {"status": "pass", "candidate_sha": pr["head_sha"]},
            "assurance": assurance,
        },
    }
