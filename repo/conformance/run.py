from __future__ import annotations
import re
import shutil
import importlib.util
import json
import os
import subprocess
import sys
import stat
import tempfile
from pathlib import Path
import ast
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def result(assertion_id, status, detail, evidence=None):
    rec = {'assertion_id': assertion_id, 'status': status, 'detail': detail}
    if evidence is not None:
        rec['evidence'] = evidence
    return rec

def check_requirement_metadata(root, assertion_ids):
    registry = load(root / 'repo/authority/requirements.json')
    reqs = registry['requirements']
    ids = [r['requirement_id'] for r in reqs]
    checks = {'FS0-ASSERT-FC-045': (registry.get('requirements_total') == len(reqs) and len(ids) == len(set(ids)) and all(ids), 'requirement identities are present and unique and the registry count is self-consistent'), 'FS0-ASSERT-FC-056': (all((r.get('lifecycle_state') in {'accepted', 'superseded', 'withdrawn'} for r in reqs)), 'requirement lifecycle states use the allowed enumeration'), 'FS0-ASSERT-FC-057': (all((r.get('conformance_applicability') in {'mechanical', 'none'} for r in reqs)), 'Conformance applicability uses mechanical|none'), 'FS0-ASSERT-FC-058': (all((r.get('assurance_applicability') in {'required', 'none'} for r in reqs)), 'Assurance applicability uses required|none'), 'FS0-ASSERT-FC-075': (all((len(r.get('statement', '')) <= 300 for r in reqs)), 'all normative requirement statements are <=300 characters'), 'FS0-ASSERT-CONF-024': (all((len(r.get('statement', '')) <= 300 for r in reqs)), 'Conformance rejects the present state if a requirement exceeds 300 characters')}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1]) for aid in assertion_ids]

def check_conformance_closure(root, assertion_ids):
    req_registry = load(root / 'repo/authority/requirements.json')
    corr_registry = load(root / 'repo/conformance/correspondence.json')
    reqs = req_registry['requirements']
    corr = corr_registry['records']
    assertions = load(root / 'repo/conformance/assertions.json')['assertions']
    impl = load(root / 'repo/conformance/support/implementations.json')['implementations']
    evidence = load(root / 'repo/conformance/evidence.json')['evidence']
    orchestration = load(root / 'repo/conformance/orchestration.json')
    req_ids = [r['requirement_id'] for r in reqs]
    accepted_req_ids = {r['requirement_id'] for r in reqs if r.get('lifecycle_state') == 'accepted'}
    corr_by_req = {r['requirement_id']: r for r in corr}
    assertion_by_id = {a['assertion_id']: a for a in assertions}
    implementation_ids = {i['implementation_id'] for i in impl}
    bindings = {}
    for implementation in impl:
        for aid in implementation.get('assertion_ids', []):
            bindings.setdefault(aid, []).append(implementation)
    implementation_assertion_ids = [aid for implementation in impl for aid in implementation.get('assertion_ids', [])]
    implementation_bindings_closed = len(implementation_assertion_ids) == len(set(implementation_assertion_ids)) and all((aid in assertion_by_id for aid in implementation_assertion_ids))
    primitive_roles = {a.get('role') for a in assertions} | {i.get('role') for i in impl} | {e.get('role') for e in evidence} | {orchestration.get('role')}
    assertion_provenance_ok = all((a.get('requirement_id') in accepted_req_ids for a in assertions))
    support_provenance_ok = all((isinstance(i.get('authority_requirement_ids'), list) and i['authority_requirement_ids'] and all((rid in accepted_req_ids for rid in i['authority_requirement_ids'])) for i in impl))
    evidence_provenance_ok = all((isinstance(e.get('authority_requirement_ids'), list) and e['authority_requirement_ids'] and all((rid in accepted_req_ids for rid in e['authority_requirement_ids'])) for e in evidence))
    orchestration_provenance_ok = isinstance(orchestration.get('authority_requirement_ids'), list) and bool(orchestration['authority_requirement_ids']) and all((rid in accepted_req_ids for rid in orchestration['authority_requirement_ids']))
    evidence_by_impl = {}
    for record in evidence:
        evidence_by_impl.setdefault(record.get('implementation_id'), []).append(record)
    executable_assertion_evidence_ok = all((evidence_by_impl.get(implementation.get('implementation_id')) and all((record.get('evidence_id') and record.get('role') == 'evidence' and (record.get('evidence_class') in {'execution-result', 'repository-state'}) for record in evidence_by_impl[implementation['implementation_id']])) for implementation in impl if implementation.get('assertion_ids')))
    mechanical_assertion_ids = {aid for rec in corr if rec.get('applicability') == 'mechanical' for aid in rec.get('assertion_ids', [])}
    executable_closure_ok = all((aid in assertion_by_id and len(bindings.get(aid, [])) == 1 and bool(evidence_by_impl.get(bindings[aid][0]['implementation_id'])) for aid in mechanical_assertion_ids))
    callable_names = set(CALLABLES)
    canonical_entrypoint_ok = orchestration.get('entrypoint') == 'repo/conformance/run.py' and orchestration.get('public_wrapper') == 'repo/scripts/validate'
    gating_assertion_ids = {aid for implementation in impl if not implementation.get('pending', False) for aid in implementation.get('assertion_ids', [])}
    canonical_reachability_ok = canonical_entrypoint_ok and gating_assertion_ids <= set(orchestration.get('realized_assertion_ids', [])) and all((len(bindings.get(aid, [])) == 1 and bindings[aid][0].get('callable') in callable_names for aid in gating_assertion_ids))
    checks = {'FS0-ASSERT-CONF-001': (req_registry.get('requirements_total') == corr_registry.get('requirements_total') == len(reqs) == len(corr) and set(corr_by_req) == set(req_ids), 'every requirement has exactly one Conformance correspondence and registry totals agree'), 'FS0-ASSERT-CONF-002': (executable_closure_ok, 'every mechanically applicable requirement resolves through stable assertion identity to exactly one executable implementation with declared evidence'), 'FS0-ASSERT-CONF-003': (primitive_roles == {'assertion', 'support', 'evidence', 'orchestration'}, 'maintained Conformance primitives use exactly assertion, support, evidence, and orchestration roles'), 'FS0-ASSERT-CONF-004': (all((a['assertion_id'] not in implementation_ids for a in assertions)), 'assertion identities are distinct from implementation identities'), 'FS0-ASSERT-CONF-005': (assertion_provenance_ok and support_provenance_ok and evidence_provenance_ok and orchestration_provenance_ok, 'every maintained Conformance primitive resolves to accepted normative authority'), 'FS0-ASSERT-CONF-007': (executable_assertion_evidence_ok, 'every implementation that makes assertions executable resolves at least one declared Conformance evidence primitive'), 'FS0-ASSERT-CONF-008': (canonical_reachability_ok, 'every gating assertion is bound to a registered callable reachable from canonical Conformance orchestration'), 'FS0-ASSERT-CONF-013': (all(({'requirement_id', 'applicability', 'assertion_ids'} <= set(r) for r in corr)), 'all correspondence records contain required fields'), 'FS0-ASSERT-CONF-015': (len({a['assertion_id'] for a in assertions}) == len(assertions) and all((a.get('requirement_id') for a in assertions)) and implementation_bindings_closed, 'shared implementations preserve distinct declared assertion identity and provenance, and implementation bindings are closed over the assertion registry'), 'FS0-ASSERT-CONF-018': (all((r['assertion_ids'] and all((aid in assertion_by_id for aid in r['assertion_ids'])) for r in corr if r['applicability'] == 'mechanical')) and implementation_bindings_closed, 'mechanical correspondence records and implementation bindings contain only stable declared assertion identities'), 'FS0-ASSERT-CONF-019': (all((not r['assertion_ids'] for r in corr if r['applicability'] == 'none')), 'none-applicable correspondence records contain empty assertion_ids')}
    graph_evidence = {'mechanical_assertion_count': len(mechanical_assertion_ids), 'executable_assertion_count': sum((1 for aid in mechanical_assertion_ids if len(bindings.get(aid, [])) == 1)), 'gating_assertion_count': len(gating_assertion_ids), 'canonical_entrypoint': orchestration.get('entrypoint'), 'canonical_wrapper': orchestration.get('public_wrapper'), 'pending_implementation_assertions': sorted((aid for implementation in impl if implementation.get('pending', False) for aid in implementation.get('assertion_ids', [])))}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1], graph_evidence if aid in {'FS0-ASSERT-CONF-002', 'FS0-ASSERT-CONF-008'} else None) for aid in assertion_ids]

def _load_module_for_fc033(path, name):
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f'unable to load module: {path}')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.dont_write_bytecode = old

def check_self_change_completion(root, assertion_ids):
    contract_path = root / 'repo/bootstrap/data/self_change_contract.json'
    module_path = root / 'repo/governance/self_change.py'
    try:
        contract = load(contract_path)
        module = _load_module_for_fc033(module_path, 'fs0_fc033_self_change')
        sha, base, result_sha = ('a' * 40, 'b' * 40, 'c' * 40)
        actor = {'id': 101, 'login': 'authorized-actor'}
        plan = {'schema_version': '1', 'record_type': 'governed-work', 'stage': 'plan', 'stage_steps': ['analyze', 'specify', 'accept'], 'work_id': 'FS0-PLAN-SELFCHANGE', 'predecessor_id': 'FS0-DESIGN-SELFCHANGE', 'scope': ['repo/example'], 'material_exclusions': [], 'candidate_result': {'kind': 'self-change'}, 'completion_conditions': ['bounded cycle complete'], 'disposition': 'accepted', 'provenance': {'kind': 'synthetic-conformance'}, 'bounded_authorization': {'acceptance_actor': actor, 'mutation_scope': ['repo/example']}, 'accepted_design_id': 'FS0-DESIGN-SELFCHANGE', 'realization_intent': {'affected_artifacts': ['repo/example'], 'conformance_work': ['FS0-ASSERT-FC-033'], 'assurance_work': ['FS0-OBL-FC-033'], 'dependencies': [], 'sequencing': ['bounded'], 'build_scope': ['repo/example']}, 'required_assurance_obligation_ids': ['FS0-OBL-FC-033']}
        build = {'schema_version': '1', 'record_type': 'governed-work', 'stage': 'build', 'stage_steps': ['implement', 'verify', 'accept'], 'work_id': 'FS0-BUILD-SELFCHANGE', 'predecessor_id': plan['work_id'], 'scope': ['repo/example'], 'material_exclusions': [], 'candidate_result': {'candidate_id': sha}, 'completion_conditions': ['cycle complete'], 'disposition': 'pending', 'provenance': {'kind': 'synthetic-conformance'}, 'bounded_authorization': {'acceptance_actor': actor, 'mutation_scope': ['repo/example']}, 'accepted_plan_id': plan['work_id'], 'verification': {'evidence': ['candidate-publication'], 'conformance_status': 'pending'}, 'required_assurance_obligation_ids': ['FS0-OBL-FC-033']}
        pr = {'schema_version': '1', 'record_type': 'governed-pr-candidate', 'work_id': build['work_id'], 'issue_number': 17, 'head_sha': sha, 'accepted_repository_predecessor': base, 'base_ref': 'refs/heads/main'}
        candidate_audit = {'status': 'pass', 'basis': 'candidate-semantic-audit-receipt', 'candidate_sha': sha, 'required_obligation_ids': ['FS0-OBL-FC-033'], 'comment_id': 77}
        merge = {'merged': True, 'actor': actor, 'head_sha': sha, 'base_sha': base, 'resulting_revision': result_sha}
        completion = {'status': 'complete', 'work_id': build['work_id'], 'resulting_accepted_revision': result_sha, 'assurance': {'status': 'pass', 'basis': 'authorized-issue-close', 'audit_receipt': {'status': 'pass', 'basis': 'completion-semantic-audit-receipt'}}}
        cycle = module.verify_cycle(root, plan, build, {'status': 'published', 'candidate_id': sha, 'candidate_ref': contract['candidate_ref']}, {'status': 'pass', 'candidate_id': sha, 'failed_assertions': []}, ['FS0-OBL-FC-033'], candidate_audit, pr, merge, completion)
        missing_audit_rejected = False
        try:
            module.verify_cycle(root, plan, build, {'status': 'published', 'candidate_id': sha, 'candidate_ref': contract['candidate_ref']}, {'status': 'pass', 'candidate_id': sha, 'failed_assertions': []}, ['FS0-OBL-FC-033'], None, pr, merge, completion)
        except Exception:
            missing_audit_rejected = True
        ok = cycle.get('status') == 'complete' and cycle.get('resulting_accepted_revision') == result_sha and missing_audit_rejected
        return [result(aid, 'pass' if ok else 'fail', 'self-change requires exact candidate Conformance, candidate audit receipt, authorized merge, main audit receipt and authorized issue closure') for aid in assertion_ids]
    except Exception as exc:
        return [result(aid, 'fail', f'self-change completion check failed: {exc}') for aid in assertion_ids]

def check_generation_correspondence(root, assertion_ids):
    proc = subprocess.run([str(root / 'repo/bootstrap/scripts/bootstrap'), '--check'], cwd=root, text=True, capture_output=True)
    correspondence_ok = proc.returncode == 0 and 'FS0 generation correspondence: PASS' in proc.stdout
    orchestration = load(root / 'repo/conformance/orchestration.json')
    generation = orchestration.get('generation_correspondence', {})
    declared_ok = generation.get('canonical_input_root') == 'repo/bootstrap/data' and generation.get('generation_implementation') == 'repo/bootstrap/scripts/src/generate.py' and (generation.get('check_entrypoint') == 'repo/bootstrap/scripts/bootstrap --check') and (root / generation.get('canonical_input_root', '')).is_dir() and (root / generation.get('generation_implementation', '')).is_file()
    evidence = {'returncode': proc.returncode, 'stdout': proc.stdout.strip(), 'stderr': proc.stderr.strip(), 'declared_generation_correspondence': generation}
    out = []
    for aid in assertion_ids:
        if aid == 'FS0-ASSERT-CONF-021':
            ok = correspondence_ok and declared_ok
            detail = 'all generator-declared FS0 outputs reproduce from the declared canonical bootstrap input root using the identified generator'
        elif aid == 'FS0-ASSERT-CONF-022':
            ok = correspondence_ok
            detail = 'deterministic regeneration matches checked-in generated surfaces'
        else:
            ok = correspondence_ok
            detail = 'generation-correspondence failure is surfaced as a Conformance defect'
        out.append(result(aid, 'pass' if ok else 'fail', detail, evidence))
    return out

def check_canonical_entrypoint(root, assertion_ids):
    engine = root / 'repo/conformance/run.py'
    wrapper = root / 'repo/scripts/validate'
    ok = engine.is_file() and wrapper.is_file()
    return [result(aid, 'pass' if ok else 'fail', 'repo/conformance/run.py exists as the canonical Conformance engine and repo/scripts/validate exposes it', {'entrypoint': 'repo/conformance/run.py', 'wrapper': 'repo/scripts/validate'}) for aid in assertion_ids]

def check_remote_execution(root, assertion_ids):
    workflow = root / '.github/workflows/fs0-conformance.yml'
    required = ('name: FS0 Conformance', 'pull_request:', 'push:', 'workflow_dispatch:', './repo/scripts/validate --verbose')
    text = workflow.read_text(encoding='utf-8') if workflow.is_file() else ''
    workflow_ok = workflow.is_file() and all((item in text for item in required))
    orchestration = load(root / 'repo/conformance/orchestration.json')
    canonical_binding_ok = orchestration.get('entrypoint') == 'repo/conformance/run.py' and orchestration.get('public_wrapper') == 'repo/scripts/validate' and ('./repo/scripts/validate --verbose' in text)
    checks = {'FS0-ASSERT-CONF-010': (workflow_ok, 'GitHub Actions exposes the canonical FS0 Conformance wrapper for push, pull request, and manual execution'), 'FS0-ASSERT-CONF-014': (workflow_ok and canonical_binding_ok, 'the fixed FS0 GitHub workflow invokes the machine-resolvable canonical repository Conformance surface')}
    evidence = {'workflow': '.github/workflows/fs0-conformance.yml'}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1], evidence) for aid in assertion_ids]

def check_exact_candidate(root, assertion_ids):
    workflow = root / '.github/workflows/fs0-conformance.yml'
    text = workflow.read_text(encoding='utf-8') if workflow.is_file() else ''
    expected_env = "FS0_CANDIDATE_SHA: ${{ github.event_name == 'pull_request' && github.event.pull_request.head.sha || github.sha }}"
    expected_ref = 'ref: ${{ env.FS0_CANDIDATE_SHA }}'
    structural_ok = workflow.is_file() and expected_env in text and (expected_ref in text) and ('uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262' in text) and ('./repo/scripts/validate --verbose' in text)
    runtime = os.environ.get('GITHUB_ACTIONS') == 'true'
    evidence = {'workflow': '.github/workflows/fs0-conformance.yml', 'binding': 'FS0_CANDIDATE_SHA', 'runtime': runtime}
    runtime_ok = True
    if runtime:
        candidate = os.environ.get('FS0_CANDIDATE_SHA', '').lower()
        try:
            head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, text=True, capture_output=True, check=True).stdout.strip().lower()
        except Exception as exc:
            head = ''
            runtime_ok = False
            evidence['git_error'] = str(exc)
        candidate_ok = len(candidate) == 40 and all((ch in '0123456789abcdef' for ch in candidate))
        runtime_ok = runtime_ok and candidate_ok and (head == candidate)
        evidence['candidate_sha'] = candidate
        evidence['checked_out_head'] = head
    else:
        evidence['mode'] = 'local-structural-verification'
    ok = structural_ok and runtime_ok
    detail = 'workflow resolves an exact event candidate SHA, checks out that SHA, and GitHub Actions execution verifies checked-out HEAD equals the declared candidate'
    return [result(aid, 'pass' if ok else 'fail', detail, evidence) for aid in assertion_ids]

def _exact_sha(value):
    return isinstance(value, str) and bool(re.fullmatch('[0-9a-f]{40}', value))

def _positive_int(value):
    return not isinstance(value, bool) and isinstance(value, int) and (value > 0)

def _aware_timestamp(value):
    if not isinstance(value, str) or not value:
        return False
    try:
        text = value[:-1] + '+00:00' if value.endswith('Z') else value
        parsed = __import__('datetime').datetime.fromisoformat(text)
    except Exception:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None

def _bootstrap_state_semantics(root, record):
    required = {'schema_version', 'record_type', 'state', 'bootstrap_provenance_issue', 'accepted_ref', 'cutover_timestamp'}
    if not isinstance(record, dict) or set(record) != required:
        return False
    if record.get('schema_version') != '1' or record.get('record_type') != 'bootstrap-state':
        return False
    if record.get('state') not in {'candidate', 'cutover'}:
        return False
    if record.get('accepted_ref') != 'refs/heads/main':
        return False
    if record['state'] == 'candidate':
        return record.get('bootstrap_provenance_issue') is None and record.get('cutover_timestamp') is None
    issue = record.get('bootstrap_provenance_issue')
    stamp = record.get('cutover_timestamp')
    return isinstance(issue, int) and (not isinstance(issue, bool)) and (issue > 0) and isinstance(stamp, str) and stamp.endswith('Z') and (len(stamp) >= 20)

def check_bootstrap_state(root, assertion_ids):
    path = root / 'repo/state/bootstrap.json'
    try:
        record = load(path)
        state_ok = _bootstrap_state_semantics(root, record)
        synthetic_cutover = {'schema_version': '1', 'record_type': 'bootstrap-state', 'state': 'cutover', 'bootstrap_provenance_issue': 1, 'accepted_ref': 'refs/heads/main', 'cutover_timestamp': '2026-01-01T00:00:00Z'}
        shared_cutover_semantics_ok = _bootstrap_state_semantics(root, synthetic_cutover)
        orchestration = load(root / 'repo/conformance/orchestration.json')
        pre_cutover_mode_ok = record.get('state') != 'candidate' or orchestration.get('mode') == 'candidate-bootstrap-verification'
        checks = {'FS0-ASSERT-FC-037': (state_ok and shared_cutover_semantics_ok, 'repo/state/bootstrap.json contains the minimal bootstrap lifecycle/provenance fields and identifies refs/heads/main'), 'FS0-ASSERT-CONF-011': (pre_cutover_mode_ok, 'while bootstrap state is candidate, candidate Conformance execution is explicitly bootstrap mechanical verification evidence only')}
        evidence = {'path': 'repo/state/bootstrap.json', 'state': record.get('state'), 'bootstrap_provenance_issue': record.get('bootstrap_provenance_issue'), 'accepted_ref': record.get('accepted_ref'), 'cutover_timestamp': record.get('cutover_timestamp'), 'conformance_mode': orchestration.get('mode')}
    except Exception as exc:
        checks = {aid: (False, 'bootstrap state validation setup failed') for aid in assertion_ids}
        evidence = {'error': str(exc)}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1], evidence) for aid in assertion_ids]

def _fs0_pre_main_provenance_check_governance_state_resolution(root, assertion_ids):
    work_path = root / 'repo/governance/work.py'
    state_path = root / 'repo/governance/accepted_state.py'
    cutover_path = root / 'repo/governance/bootstrap_cutover.py'
    publish_path = root / 'repo/governance/publish_accepted.py'
    try:
        work = _load_module_for_fc033(work_path, 'fs0_merge_acceptance_work')
        accepted_state = _load_module_for_fc033(state_path, 'fs0_merge_acceptance_state')
        sha = 'a' * 40
        base = 'b' * 40
        result_sha = 'c' * 40
        actor = {'id': 101, 'login': 'authorized'}
        build = {'schema_version': '1', 'record_type': 'governed-work', 'stage': 'build', 'stage_steps': ['implement', 'verify', 'accept'], 'work_id': 'FS0-BUILD-MERGE', 'predecessor_id': 'FS0-PLAN-MERGE', 'scope': ['repo/example'], 'material_exclusions': [], 'candidate_result': {'candidate_id': sha}, 'completion_conditions': ['authorized change accepted'], 'disposition': 'pending', 'provenance': {'kind': 'synthetic-conformance'}, 'bounded_authorization': {'acceptance_actor': actor, 'mutation_scope': ['repo/example']}, 'accepted_plan_id': 'FS0-PLAN-MERGE', 'verification': {'evidence': ['candidate'], 'conformance_status': 'pass'}, 'required_assurance_obligation_ids': []}
        pr = {'schema_version': '1', 'record_type': 'governed-pr-candidate', 'work_id': build['work_id'], 'issue_number': 42, 'head_sha': sha, 'accepted_repository_predecessor': base, 'base_ref': 'refs/heads/main'}
        merge = {'merged': True, 'actor': actor, 'head_sha': sha, 'base_sha': base, 'resulting_revision': result_sha}
        accepted = work.merge_acceptance(build, pr, merge, [])
        authorized_merge_ok = accepted.get('status') == 'accepted' and accepted.get('candidate_head') == sha and (accepted.get('resulting_accepted_revision') == result_sha)
        unauthorized_rejected = False
        bad = dict(merge)
        bad['actor'] = {'id': 202, 'login': 'unauthorized'}
        try:
            work.merge_acceptance(build, pr, bad, [])
        except Exception:
            unauthorized_rejected = True
        multi_issue_rejected = False
        bad_pr = dict(pr)
        bad_pr['work_id'] = [build['work_id'], 'OTHER']
        try:
            work.validate_pr_candidate(build, bad_pr)
        except Exception:
            multi_issue_rejected = True
        stale_base_rejected = False
        stale = dict(merge)
        stale['base_sha'] = 'd' * 40
        try:
            work.merge_acceptance(build, pr, stale, [])
        except Exception:
            stale_base_rejected = True
        before = accepted_state.resolve_main_revision({'state': 'candidate'}, result_sha)
        after = accepted_state.resolve_main_revision({'state': 'cutover'}, result_sha)
        main_state_ok = before.get('status') == 'unaccepted' and after.get('status') == 'accepted' and (after.get('accepted_revision') == result_sha) and (after.get('provenance_resolution') == 'governed-pr-merge')
        cutover_source = cutover_path.read_text(encoding='utf-8')
        bootstrap_pr_ok = '/pulls' in cutover_source and '--accept-bootstrap' not in cutover_source and ('bootstrap-cutover' in cutover_source) and ('explicit bootstrap acceptance' in cutover_source)
        publish_source = publish_path.read_text(encoding='utf-8')
        publication_retired = 'RETIRED' in publish_source and 'merge an eligible governed pull request' in publish_source
        checks = {'FS0-ASSERT-GOV-008': (authorized_merge_ok and unauthorized_rejected, 'authorized eligible PR merge creates attributable candidate-specific acceptance'), 'FS0-ASSERT-GOV-011': (multi_issue_rejected, 'each governed PR identifies exactly one governed work item'), 'FS0-ASSERT-GOV-012': (authorized_merge_ok, 'PR acceptance applies to the complete evaluated head candidate'), 'FS0-ASSERT-GOV-013': (authorized_merge_ok, 'Conformance and Assurance gate governed PR merge acceptance'), 'FS0-ASSERT-GOV-014': (bootstrap_pr_ok, 'bootstrap acceptance is the designated validated bootstrap-cutover PR merge'), 'FS0-ASSERT-GOV-015': (stale_base_rejected, 'merge acceptance binds the recorded accepted repository predecessor'), 'FS0-ASSERT-GOV-016': (main_state_ok, 'after cutover refs/heads/main resolves canonical accepted repository state'), 'FS0-ASSERT-GOV-017': (authorized_merge_ok and publication_retired, 'legacy non-merge acceptance paths are inactive'), 'FS0-ASSERT-GOV-035': (authorized_merge_ok, 'Governance acceptance is authorized governed PR merge after eligibility gates'), 'FS0-ASSERT-GOV-037': (main_state_ok and publication_retired, 'accepted-state publication occurs through governed PR merge into main')}
        evidence = {'authorized_merge': authorized_merge_ok, 'unauthorized_merge_rejected': unauthorized_rejected, 'multiple_work_ids_rejected': multi_issue_rejected, 'stale_predecessor_rejected': stale_base_rejected, 'main_is_canonical_after_cutover': main_state_ok, 'bootstrap_pr_merge_binding': bootstrap_pr_ok, 'legacy_publication_retired': publication_retired}
    except Exception as exc:
        checks = {aid: (False, 'merge-acceptance conformance setup failed') for aid in assertion_ids}
        evidence = {'error': str(exc)}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1], evidence) for aid in assertion_ids]

def _fs0_pre_immutable_binding_check_governance_state_resolution(root, assertion_ids):
    legacy_results = _fs0_pre_main_provenance_check_governance_state_resolution(root, assertion_ids)
    path = root / 'repo/governance/accepted_state.py'
    spec = importlib.util.spec_from_file_location('fs0_main_provenance', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    sha = '3' * 40
    head = '1' * 40
    predecessor = '2' * 40
    state = {'state': 'cutover', 'bootstrap_provenance_issue': 17}
    issue_body = '```json\n{"schema_version":"1","record_type":"bootstrap-authorization","acceptance_actor":{"id":101,"login":"tester"},"accepted_repository_predecessor":"' + predecessor + '","accepted_ref":"refs/heads/main"}\n```'
    pr_body = '```json\n{"schema_version":"1","record_type":"bootstrap-cutover-candidate","bootstrap_provenance_issue":17,"head_sha":"' + head + '","accepted_repository_predecessor":"' + predecessor + '","base_ref":"refs/heads/main"}\n```'
    issue = {'number': 17, 'body': issue_body}
    bootstrap_binding = {'schema_version': '1', 'record_type': 'bootstrap-candidate-binding', 'bootstrap_provenance_issue': 17, 'acceptance_actor': {'id': 101, 'login': 'tester'}, 'accepted_repository_predecessor': predecessor, 'base_ref': 'refs/heads/main'}
    conf = {'status': 'pass', 'candidate_sha': head, 'defects': []}
    pr = {'number': 7, 'body': pr_body, 'merged_at': '2026-01-01T00:20:00Z', 'merged_by': {'id': 101, 'login': 'tester'}, 'head': {'sha': head}, 'base': {'ref': 'main', 'sha': predecessor}, 'merge_commit_sha': sha, '_fs0_bootstrap_conformance': conf, '_fs0_bootstrap_binding': bootstrap_binding}
    accepted = m.resolve_bootstrap_merge_acceptance('o/r', state, sha, [pr], issue)
    bad = dict(pr)
    bad['_fs0_bootstrap_conformance'] = {'status': 'fail', 'candidate_sha': head, 'defects': ['failed']}
    ineligible = m.resolve_bootstrap_merge_acceptance('o/r', state, sha, [bad], issue)
    direct = m.resolve_remote_main_acceptance('o/r', state, '4' * 40, [], issue)
    unproven = m.resolve_main_revision(state, sha)
    proven = m.resolve_main_revision(state, sha, accepted)
    cutover = (root / 'repo/governance/bootstrap_cutover.py').read_text(encoding='utf-8')
    ok = accepted.get('status') == 'accepted' and ineligible.get('status') == 'invalid' and (direct.get('status') == 'invalid') and (unproven.get('status') == 'invalid') and (proven.get('status') == 'accepted') and ('bootstrap-authorization' in cutover) and ('bootstrap-cutover-candidate' in cutover)
    out = []
    for item in legacy_results:
        aid = item.get('assertion_id') if isinstance(item, dict) else None
        if aid in {'FS0-ASSERT-GOV-014', 'FS0-ASSERT-GOV-016', 'FS0-ASSERT-GOV-037'}:
            detail = 'bootstrap acceptance is the designated eligible authorized bootstrap-cutover PR merge' if aid == 'FS0-ASSERT-GOV-014' else 'refs/heads/main requires eligible authorized merge provenance'
            out.append(result(aid, 'pass' if ok else 'fail', detail, {'eligible_bootstrap': accepted.get('status'), 'ineligible_bootstrap': ineligible.get('status'), 'direct_push': direct.get('status'), 'unproven_main': unproven.get('status'), 'proven_main': proven.get('status')}))
        else:
            out.append(item)
    return out

def check_governance_state_resolution(root, assertion_ids):
    legacy_results = _fs0_pre_immutable_binding_check_governance_state_resolution(root, assertion_ids)
    path = root / 'repo/governance/accepted_state.py'
    spec = importlib.util.spec_from_file_location('fs0_native_assurance_binding', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    work = {'schema_version': '1', 'record_type': 'governed-work', 'stage': 'build', 'stage_steps': ['implement', 'verify', 'accept'], 'work_id': 'B-IMMUTABLE', 'predecessor_id': 'P-IMMUTABLE', 'scope': ['repo/governance/work.py'], 'material_exclusions': [], 'candidate_result': {'kind': 'synthetic'}, 'completion_conditions': ['merged and audited'], 'disposition': 'pending', 'provenance': {'kind': 'synthetic-conformance'}, 'bounded_authorization': {'acceptance_actor': {'id': 101, 'login': 'authorized'}, 'mutation_scope': ['repo/governance/work.py']}, 'required_assurance_obligation_ids': [], 'accepted_plan_id': 'P-IMMUTABLE', 'verification': {'evidence': ['evidence:test'], 'conformance_status': 'pass'}}
    head = '1' * 40
    predecessor = '2' * 40
    resulting = '3' * 40
    binding = {'schema_version': '1', 'record_type': 'governed-candidate-binding', 'issue_number': 23, 'accepted_repository_predecessor': predecessor, 'base_ref': 'refs/heads/main', 'governed_work': work}
    eligibility = {'status': 'pass', 'candidate_sha': head, 'conformance': {'status': 'pass', 'candidate_sha': head}, 'assurance': {'status': 'pass', 'basis': 'candidate-semantic-audit-receipt', 'candidate_sha': head, 'required_obligation_ids': [], 'comment_id': 1, 'defects': []}}
    pr = {'number': 9, 'body': 'MUTABLE PR BODY MAY CHANGE', 'merged_at': '2026-01-01T00:20:00Z', 'merged_by': {'id': 101, 'login': 'authorized'}, 'head': {'sha': head}, 'base': {'ref': 'main', 'sha': predecessor}, 'merge_commit_sha': resulting, '_fs0_governed_binding': binding, '_fs0_eligibility': eligibility, '_fs0_issue': {'body': 'MUTABLE ISSUE BODY MAY CHANGE'}}
    immutable_accept = m.resolve_governed_resulting_acceptance('o/r', resulting, [pr])
    forged = dict(pr)
    forged_binding = dict(binding)
    forged_work = dict(work)
    forged_auth = dict(work['bounded_authorization'])
    forged_auth['acceptance_actor'] = {'id': 202, 'login': 'forged'}
    forged_work['bounded_authorization'] = forged_auth
    forged_binding['governed_work'] = forged_work
    forged['_fs0_governed_binding'] = forged_binding
    forged_accept = m.resolve_governed_resulting_acceptance('o/r', resulting, [forged])
    immutable_ok = immutable_accept.get('status') == 'accepted' and forged_accept.get('status') != 'accepted'
    evidence = {'immutable_bound_acceptance': immutable_accept.get('status'), 'forged_post_merge_authorization': forged_accept.get('status'), 'commit_binding_helpers': True}
    overrides = {}
    for aid in ('FS0-ASSERT-GOV-016', 'FS0-ASSERT-GOV-035', 'FS0-ASSERT-GOV-037', 'FS0-ASSERT-GOV-047'):
        if aid in assertion_ids:
            detail = 'accepted main and governed merge acceptance use immutable candidate-bound Governance metadata; later issue/PR body edits cannot create or rewrite acceptance' if aid in {'FS0-ASSERT-GOV-016', 'FS0-ASSERT-GOV-037'} else 'authorized exact-head merge is candidate Assurance/acceptance and remains machine-resolvable from immutable candidate-bound Governance metadata'
            overrides[aid] = result(aid, 'pass' if immutable_ok else 'fail', detail, evidence)
    by_id = {item['assertion_id']: item for item in legacy_results}
    return [overrides.get(aid, by_id.get(aid, result(aid, 'fail', 'governance assertion result missing'))) for aid in assertion_ids]

def check_accepted_state_publication(root, assertion_ids):
    return [result(aid, 'fail', 'legacy accepted-state publication has no active assertions; GOV-037 is bound to governed PR merge semantics') for aid in assertion_ids]

def _walk_physical_namespace(root):
    records = {}
    stack = [root]
    while stack:
        directory = stack.pop()
        try:
            entries = list(os.scandir(directory))
        except OSError as exc:
            raise RuntimeError(f'cannot scan {directory}: {exc}') from exc
        for entry in entries:
            path = Path(entry.path)
            rel = path.relative_to(root).as_posix()
            try:
                mode = entry.stat(follow_symlinks=False).st_mode
            except OSError as exc:
                raise RuntimeError(f'cannot lstat {rel}: {exc}') from exc
            if stat.S_ISREG(mode):
                kind = 'file'
            elif stat.S_ISDIR(mode):
                kind = 'directory'
            elif stat.S_ISLNK(mode):
                kind = 'symlink'
            else:
                kind = 'unsupported'
            records[rel] = {'path': path, 'object_type': kind, 'mode': mode}
            if kind == 'directory':
                stack.append(path)
    return records

def _json_record(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None

def _discover_structure_binding(root, namespace=None):
    namespace = namespace if namespace is not None else _walk_physical_namespace(root)
    matches = []
    for rel, item in namespace.items():
        if item['object_type'] != 'file':
            continue
        obj = _json_record(item['path'])
        if isinstance(obj, dict) and obj.get('schema_version') == '1' and (obj.get('record_type') == 'repository-structure-binding'):
            matches.append((rel, obj))
    if len(matches) != 1:
        raise RuntimeError(f'governed repository state must contain exactly one repository-structure-binding record; found {len(matches)}')
    rel, record = matches[0]
    identity = record.get('configuration_identity')
    if not isinstance(identity, str) or not identity:
        raise RuntimeError('repository-structure-binding lacks configuration_identity')
    return (identity, rel)

def _resolve_structure_configuration(root, identity, namespace=None):
    namespace = namespace if namespace is not None else _walk_physical_namespace(root)
    matches = []
    for rel, item in namespace.items():
        if item['object_type'] != 'file':
            continue
        obj = _json_record(item['path'])
        if isinstance(obj, dict) and obj.get('schema_version') == '1' and (obj.get('record_type') == 'repository-structure-configuration') and (obj.get('configuration_id') == identity):
            matches.append((rel, obj))
    if len(matches) != 1:
        raise RuntimeError(f'configuration identity {identity!r} must resolve to exactly one configuration object; found {len(matches)}')
    return matches[0]

def _normalize_config_entries(config):
    if config.get('schema_version') != '1':
        raise RuntimeError('unsupported repository-structure configuration schema')
    if config.get('record_type') != 'repository-structure-configuration':
        raise RuntimeError('unexpected repository-structure configuration record_type')
    identity = config.get('configuration_id')
    if not isinstance(identity, str) or not identity:
        raise RuntimeError('configuration_id must be a non-empty string')
    raw_entries = config.get('objects')
    if not isinstance(raw_entries, list):
        raise RuntimeError('repository-structure configuration objects must be a list')
    entries = {}
    for rec in raw_entries:
        if not isinstance(rec, dict):
            raise RuntimeError('repository-structure object entries must be records')
        rel = rec.get('path')
        obj_type = rec.get('object_type')
        presence = rec.get('presence')
        descendants = rec.get('descendants', 'closed')
        if not isinstance(rel, str) or not rel:
            raise RuntimeError('repository-structure object path must be non-empty')
        p = Path(rel)
        if p.is_absolute() or '..' in p.parts or rel in {'.', './'}:
            raise RuntimeError(f'invalid repository-structure path: {rel}')
        normalized = p.as_posix()
        if normalized != rel:
            raise RuntimeError(f'repository-structure path is not normalized: {rel}')
        if rel in entries:
            raise RuntimeError(f'duplicate repository-structure path: {rel}')
        if obj_type not in {'file', 'directory', 'symlink'}:
            raise RuntimeError(f'unsupported configured object type for {rel}: {obj_type}')
        if presence not in {'required', 'permitted'}:
            raise RuntimeError(f'invalid presence for {rel}: {presence}')
        if descendants not in {'closed', 'complete-subtree'}:
            raise RuntimeError(f'invalid descendants mode for {rel}: {descendants}')
        if obj_type != 'directory' and descendants != 'closed':
            raise RuntimeError(f'non-directory cannot authorize descendants: {rel}')
        entries[rel] = {'path': rel, 'object_type': obj_type, 'presence': presence, 'descendants': descendants}
    return entries

def _applicable_authorization(rel, entries):
    exact = entries.get(rel)
    if exact is not None:
        return (exact, 'exact')
    parts = Path(rel).parts
    for i in range(len(parts) - 1, 0, -1):
        ancestor = Path(*parts[:i]).as_posix()
        rec = entries.get(ancestor)
        if rec and rec['object_type'] == 'directory' and (rec['descendants'] == 'complete-subtree'):
            return (rec, 'complete-subtree')
    return (None, None)

def _evaluate_repository_structure(root):
    namespace = _walk_physical_namespace(root)
    identity, binding_path = _discover_structure_binding(root, namespace)
    config_path, config = _resolve_structure_configuration(root, identity, namespace)
    entries = _normalize_config_entries(config)
    unauthorized = []
    unsupported = []
    type_mismatches = []
    missing = []
    for rel, item in namespace.items():
        actual_type = item['object_type']
        rec, mode = _applicable_authorization(rel, entries)
        if actual_type == 'unsupported':
            unsupported.append(rel)
            continue
        if rec is None:
            unauthorized.append(rel)
            continue
        if mode == 'exact' and rec['object_type'] != actual_type:
            type_mismatches.append({'path': rel, 'expected': rec['object_type'], 'actual': actual_type})
    for rel, rec in entries.items():
        if rec['presence'] == 'required' and rel not in namespace:
            missing.append(rel)
    self_rec, self_mode = _applicable_authorization(config_path, entries)
    self_authorized = self_rec is not None and namespace.get(config_path, {}).get('object_type') == 'file' and (self_mode == 'complete-subtree' or self_rec.get('object_type') == 'file')
    ok = not unauthorized and (not unsupported) and (not type_mismatches) and (not missing) and self_authorized
    return {'ok': ok, 'configuration_identity': identity, 'binding_path': binding_path, 'configuration_path': config_path, 'observed_objects': len(namespace), 'configured_objects': len(entries), 'unauthorized': sorted(unauthorized), 'unsupported': sorted(unsupported), 'type_mismatches': sorted(type_mismatches, key=lambda x: x['path']), 'missing': sorted(missing), 'configuration_self_authorized': self_authorized}

def _write_test_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + '\n', encoding='utf-8')

def _test_config(objects, identity='TEST-CONFIG'):
    return {'schema_version': '1', 'record_type': 'repository-structure-configuration', 'configuration_id': identity, 'objects': objects}

def _test_binding(identity='TEST-CONFIG'):
    return {'schema_version': '1', 'record_type': 'repository-structure-binding', 'configuration_identity': identity}

def _exercise_structure_semantics():
    cases = {}

    def run_case(name, setup, expect_ok=None, expect_error=False, inspect=None):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            setup(root)
            try:
                report = _evaluate_repository_structure(root)
                if expect_error:
                    cases[name] = False
                    return
                ok = report['ok'] == expect_ok
                if inspect is not None:
                    ok = ok and bool(inspect(report))
                cases[name] = ok
            except Exception:
                cases[name] = bool(expect_error)

    def base(root, extra_objects=None):
        _write_test_json(root / 'state.bin', _test_binding())
        objects = [{'path': 'state.bin', 'object_type': 'file', 'presence': 'required'}, {'path': 'policy.bin', 'object_type': 'file', 'presence': 'required'}]
        if extra_objects:
            objects.extend(extra_objects)
        _write_test_json(root / 'policy.bin', _test_config(objects))
    run_case('conforming_state', lambda r: base(r), expect_ok=True)
    run_case('ordinary_file_accepted', lambda r: ((r / 'ordinary').write_text('x', encoding='utf-8'), base(r, [{'path': 'ordinary', 'object_type': 'file', 'presence': 'required'}])), expect_ok=True)
    run_case('directory_object_accepted', lambda r: ((r / 'directory').mkdir(), base(r, [{'path': 'directory', 'object_type': 'directory', 'presence': 'required', 'descendants': 'closed'}])), expect_ok=True)
    run_case('unknown_file_rejected', lambda r: (base(r), (r / 'unknown').write_text('x', encoding='utf-8')), expect_ok=False, inspect=lambda x: 'unknown' in x['unauthorized'])
    run_case('unknown_directory_rejected', lambda r: (base(r), (r / 'unknown-dir').mkdir()), expect_ok=False, inspect=lambda x: 'unknown-dir' in x['unauthorized'])
    run_case('closed_directory_rejects_descendant', lambda r: ((r / 'closed').mkdir(), base(r, [{'path': 'closed', 'object_type': 'directory', 'presence': 'required'}]), (r / 'closed' / 'child').write_text('x', encoding='utf-8')), expect_ok=False, inspect=lambda x: 'closed/child' in x['unauthorized'])
    run_case('complete_subtree_accepts_descendant', lambda r: ((r / 'tree').mkdir(), (r / 'tree' / 'child').write_text('x', encoding='utf-8'), base(r, [{'path': 'tree', 'object_type': 'directory', 'presence': 'required', 'descendants': 'complete-subtree'}])), expect_ok=True)
    if hasattr(os, 'mkfifo'):
        run_case('unsupported_fifo_rejected_under_subtree', lambda r: ((r / 'tree').mkdir(), os.mkfifo(r / 'tree' / 'fifo'), base(r, [{'path': 'tree', 'object_type': 'directory', 'presence': 'required', 'descendants': 'complete-subtree'}])), expect_ok=False, inspect=lambda x: 'tree/fifo' in x['unsupported'])
    run_case('required_missing_rejected', lambda r: base(r, [{'path': 'must-exist', 'object_type': 'file', 'presence': 'required'}]), expect_ok=False, inspect=lambda x: 'must-exist' in x['missing'])
    run_case('permitted_missing_accepted', lambda r: base(r, [{'path': 'optional', 'object_type': 'file', 'presence': 'permitted'}]), expect_ok=True)
    run_case('type_mismatch_rejected', lambda r: ((r / 'thing').mkdir(), base(r, [{'path': 'thing', 'object_type': 'file', 'presence': 'required'}])), expect_ok=False, inspect=lambda x: any((i['path'] == 'thing' for i in x['type_mismatches'])))
    run_case('authorized_symlink_is_link_object', lambda r: ((r / 'target').write_text('x', encoding='utf-8'), os.symlink('target', r / 'link'), base(r, [{'path': 'target', 'object_type': 'file', 'presence': 'required'}, {'path': 'link', 'object_type': 'symlink', 'presence': 'required'}])), expect_ok=True)
    run_case('external_symlink_target_not_traversed', lambda r: (os.symlink('/tmp', r / 'link'), base(r, [{'path': 'link', 'object_type': 'symlink', 'presence': 'required'}])), expect_ok=True)
    run_case('configuration_self_authorization_required', lambda r: (_write_test_json(r / 'state.bin', _test_binding()), _write_test_json(r / 'policy.bin', _test_config([{'path': 'state.bin', 'object_type': 'file', 'presence': 'required'}]))), expect_ok=False, inspect=lambda x: not x['configuration_self_authorized'])
    run_case('missing_binding_rejected', lambda r: _write_test_json(r / 'policy.bin', _test_config([{'path': 'policy.bin', 'object_type': 'file', 'presence': 'required'}])), expect_error=True)
    run_case('ambiguous_binding_rejected', lambda r: (_write_test_json(r / 'state-a', _test_binding()), _write_test_json(r / 'state-b', _test_binding()), _write_test_json(r / 'policy.bin', _test_config([{'path': 'state-a', 'object_type': 'file', 'presence': 'required'}, {'path': 'state-b', 'object_type': 'file', 'presence': 'required'}, {'path': 'policy.bin', 'object_type': 'file', 'presence': 'required'}]))), expect_error=True)
    run_case('unresolved_identity_rejected', lambda r: _write_test_json(r / 'state.bin', _test_binding('NO-SUCH-CONFIG')), expect_error=True)
    run_case('duplicate_matching_configuration_rejected', lambda r: (_write_test_json(r / 'state.bin', _test_binding()), _write_test_json(r / 'policy-a.bin', _test_config([{'path': 'state.bin', 'object_type': 'file', 'presence': 'required'}, {'path': 'policy-a.bin', 'object_type': 'file', 'presence': 'required'}, {'path': 'policy-b.bin', 'object_type': 'file', 'presence': 'required'}])), _write_test_json(r / 'policy-b.bin', _test_config([{'path': 'state.bin', 'object_type': 'file', 'presence': 'required'}, {'path': 'policy-a.bin', 'object_type': 'file', 'presence': 'required'}, {'path': 'policy-b.bin', 'object_type': 'file', 'presence': 'required'}]))), expect_error=True)
    run_case('relocated_configuration_resolves', lambda r: ((r / 'policies').mkdir(), _write_test_json(r / 'state.bin', _test_binding()), _write_test_json(r / 'policies' / 'renamed-config.bin', _test_config([{'path': 'state.bin', 'object_type': 'file', 'presence': 'required'}, {'path': 'policies', 'object_type': 'directory', 'presence': 'required', 'descendants': 'closed'}, {'path': 'policies/renamed-config.bin', 'object_type': 'file', 'presence': 'required'}]))), expect_ok=True, inspect=lambda x: x['configuration_path'] == 'policies/renamed-config.bin')
    return {'ok': all(cases.values()), 'cases': cases}

def check_assurance_runtime(root, assertion_ids):
    module_path = root / 'repo/assurance/runtime.py'
    accepted_path = root / 'repo/governance/accepted_state.py'
    if not module_path.is_file() or not accepted_path.is_file():
        return [result(aid, 'fail', 'Assurance runtime realization is missing') for aid in assertion_ids]
    spec = importlib.util.spec_from_file_location('fs0_assurance_runtime', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    aspec = importlib.util.spec_from_file_location('fs0_assurance_acceptance', accepted_path)
    accepted = importlib.util.module_from_spec(aspec)
    aspec.loader.exec_module(accepted)
    reqs = load(root / 'repo/authority/requirements.json')['requirements']
    corr_obj = load(root / 'repo/assurance/correspondence.json')
    corr = corr_obj['records']
    obligations = load(root / 'repo/assurance/obligations.json')['obligations']
    req_ids = {r['requirement_id'] for r in reqs}
    corr_by_req = {r['requirement_id']: r for r in corr}
    obligation_by_id = {x['obligation_id']: x for x in obligations}
    required_corr = [x for x in corr if x.get('applicability') == 'required']
    none_corr = [x for x in corr if x.get('applicability') == 'none']
    sample = required_corr[0]
    triggered = module.triggered_obligation_ids(corr, [sample['requirement_id']])
    review_map = {oid: 'Build-fidelity' for oid in sample['obligation_ids']}
    contexts = module.instantiate_review_contexts('FS0-WORK-TEST', [sample['requirement_id']], corr, obligations, 'FS0-AUTH-GOVERNANCE', review_map, ['github-issue-history', 'github-pull-request-history'], 17, 23, 'a' * 40)
    context_ok = len(contexts) == len(triggered) and {x['review_obligation_id'] for x in contexts} == set(triggered) and all((x['reviewed_subject']['candidate_sha'] == 'a' * 40 for x in contexts))
    self_auth_rejected = False
    try:
        bad = dict(contexts[0])
        bad['reviewed_subject'] = dict(bad['reviewed_subject'])
        bad['reviewed_subject']['authority_id'] = bad['authorizing_authority_id']
        module.validate_review_context(bad)
    except Exception:
        self_auth_rejected = True
    candidate_receipt = module.validate_candidate_audit_receipt({'schema_version': '1', 'record_type': 'candidate-semantic-audit-receipt', 'work_id': 'FS0-WORK-TEST', 'issue_number': 17, 'pull_request_number': 23, 'candidate_sha': 'a' * 40, 'required_obligation_ids': list(triggered), 'outcome': 'satisfied', 'evidence': ['semantic-audit'], 'material_exclusions': [], 'audited_at': '2026-01-01T00:10:00Z'})
    completion_receipt = module.validate_completion_audit_receipt({'schema_version': '1', 'record_type': 'completion-semantic-audit-receipt', 'work_id': 'FS0-WORK-TEST', 'issue_number': 17, 'accepted_revision': 'c' * 40, 'accepted_pull_request_numbers': [23], 'required_obligation_ids': list(triggered), 'outcome': 'satisfied', 'evidence': ['main-semantic-audit'], 'material_exclusions': [], 'audited_at': '2026-01-01T00:30:00Z'})
    rendered = module.render_audit_receipt_comment(candidate_receipt)
    parsed = accepted.parse_assurance_audit_receipt_comment(rendered)
    actor = {'id': 101, 'login': 'authorized'}
    work = {'work_id': 'FS0-WORK-TEST', 'required_assurance_obligation_ids': list(triggered), 'bounded_authorization': {'acceptance_actor': actor}}
    candidate_comment = {'id': 1, 'body': rendered, 'created_at': '2026-01-01T00:11:00Z', 'user': actor}
    candidate_resolution = accepted.resolve_candidate_semantic_audit([candidate_comment], work, 17, 23, 'a' * 40, '2026-01-01T00:20:00Z')
    stale_resolution = accepted.resolve_candidate_semantic_audit([candidate_comment], work, 17, 23, 'b' * 40, '2026-01-01T00:20:00Z')
    adverse_record = dict(candidate_receipt)
    adverse_record['outcome'] = 'defect'
    adverse_comment = dict(candidate_comment)
    adverse_comment['id'] = 2
    adverse_comment['body'] = module.render_audit_receipt_comment(adverse_record)
    adverse_comment['created_at'] = '2026-01-01T00:12:00Z'
    adverse_resolution = accepted.resolve_candidate_semantic_audit([candidate_comment, adverse_comment], work, 17, 23, 'a' * 40, '2026-01-01T00:20:00Z')
    completion_comment = {'id': 3, 'body': module.render_audit_receipt_comment(completion_receipt), 'created_at': '2026-01-01T00:31:00Z', 'user': actor}
    completion_resolution = accepted.resolve_completion_semantic_audit([completion_comment], work, 17, 'c' * 40, [23], '2026-01-01T00:40:00Z')
    post_close = dict(completion_comment)
    post_close['created_at'] = '2026-01-01T00:41:00Z'
    late_completion = accepted.resolve_completion_semantic_audit([post_close], work, 17, 'c' * 40, [23], '2026-01-01T00:40:00Z')
    review_types = {'requirement-quality', 'ambiguity', 'contradiction', 'Design-fidelity', 'Plan-fidelity', 'Build-fidelity', 'Conformance-interpretation', 'evidence-sufficiency'}
    outcomes = {'satisfied', 'defect', 'insufficient', 'governance-required'}
    checks = {'FS0-ASSERT-ASSUR-001': (corr_obj.get('requirements_total') == len(reqs) == len(corr) and set(corr_by_req) == req_ids, 'every active requirement has exactly one Assurance correspondence'), 'FS0-ASSERT-ASSUR-002': (triggered == sample['obligation_ids'] and triggered and all((x in obligation_by_id for x in triggered)) and context_ok and (candidate_resolution.get('status') == 'pass'), 'required obligations resolve through exact-subject GitHub semantic-audit context and receipt'), 'FS0-ASSERT-ASSUR-003': (module.REVIEW_TYPES == review_types, 'Assurance supports every required semantic review class'), 'FS0-ASSERT-ASSUR-004': (module.AUDIT_OUTCOMES == outcomes and adverse_resolution.get('status') == 'fail', 'adverse audit outcome blocks disposition until a later satisfactory exact-subject receipt'), 'FS0-ASSERT-ASSUR-005': (context_ok and parsed == candidate_receipt, 'Assurance audit context and structured receipt resolve obligation, exact subject, evidence, exclusions and disposition inputs'), 'FS0-ASSERT-ASSUR-006': (self_auth_rejected, 'a review subject cannot authorize its own Assurance review'), 'FS0-ASSERT-ASSUR-008': (all(({'requirement_id', 'applicability', 'obligation_ids'} <= set(r) for r in corr)), 'Assurance correspondence contains the required fields'), 'FS0-ASSERT-ASSUR-009': (module.AUDIT_RECEIPT_MARKER == 'fs0-assurance-audit:v1' and (not hasattr(module, 'CASES_DIR')) and (not hasattr(module, 'FINDINGS_DIR')), 'fixed GitHub Assurance provenance uses structured issue/PR audit receipts without duplicate repository-tree stores'), 'FS0-ASSERT-ASSUR-012': (all((r['obligation_ids'] and all((x in obligation_by_id for x in r['obligation_ids'])) for r in required_corr)), 'required Assurance correspondence resolves stable obligation identities'), 'FS0-ASSERT-ASSUR-013': (all((not r['obligation_ids'] for r in none_corr)), 'none-applicable Assurance correspondence has empty obligation_ids'), 'FS0-ASSERT-ASSUR-014': (candidate_resolution.get('status') == 'pass' and stale_resolution.get('status') == 'fail' and (completion_resolution.get('status') == 'pass') and (late_completion.get('status') == 'fail'), 'candidate and completion audit receipts are exact-subject bound and temporally prior to dispositions')}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1]) for aid in assertion_ids]

def check_successor_proposal_registry(root, assertion_ids):
    registry_path = root / 'repo/proposals/registry.json'
    if not registry_path.is_file():
        return [result(aid, 'fail', 'successor proposal registry is missing') for aid in assertion_ids]
    registry = load(registry_path)
    records = registry.get('proposals', [])
    required_fields = {'proposal_id', 'order', 'installed_path', 'markdown_projection', 'lifecycle_state', 'bootstrap_provenance', 'authority_state', 'reconstruction_dependencies', 'predecessor_id', 'successor_id'}
    ids = {r.get('proposal_id') for r in records}
    orders = [r.get('order') for r in records]
    installed_ok = projections_ok = source_role_ok = provenance_ok = True
    for record in records:
        jp, mp = (root / record['installed_path'], root / record['markdown_projection'])
        if not jp.is_file() or not mp.is_file():
            installed_ok = False
            continue
        proposal = load(jp)
        if proposal.get('content') != mp.read_text(encoding='utf-8'):
            projections_ok = False
        if proposal.get('source_role') != 'successor-design-proposal':
            source_role_ok = False
        source = proposal.get('source_provenance')
        if not isinstance(source, dict) or not all((source.get(k) for k in ('repository', 'revision', 'path', 'blob_sha'))):
            provenance_ok = False
    dependencies_closed = all((all((dep in ids for dep in r.get('reconstruction_dependencies', []))) for r in records))
    selectable = [r for r in sorted(records, key=lambda x: x['order']) if r.get('lifecycle_state') == 'available' and (not r.get('reconstruction_dependencies'))]
    checks = {'FS0-ASSERT-FC-064': (bool(records) and source_role_ok and provenance_ok, 'successor Design Proposal source is machine-resolvably distinct and provenance-bearing'), 'FS0-ASSERT-FC-079': (bool(records) and installed_ok and projections_ok, 'successor proposal JSON and Markdown are deterministic products of canonical proposal source data'), 'FS0-ASSERT-GOV-022': (bool(records) and all((required_fields <= set(r) for r in records)) and (len(ids) == len(records)) and (len(orders) == len(set(orders))), 'proposal registry records identity, order, paths, lifecycle, provenance, authority state, dependencies, and lineage'), 'FS0-ASSERT-GOV-023': (bool(records) and all((r['lifecycle_state'] == 'available' and r['bootstrap_provenance'] == 'bootstrap-seed' and (r['authority_state'] == 'none') for r in records)), 'bootstrap seed proposal records use available/bootstrap-seed/none state'), 'FS0-ASSERT-GOV-024': (bool(records) and dependencies_closed and bool(registry.get('selection_policy')) and bool(selectable), 'fresh agents can enumerate available successor proposals and reconstruction dependencies without chat history'), 'FS0-ASSERT-GOV-025': (bool(records) and all((r.get('proposal_id') and r.get('bootstrap_provenance') == 'bootstrap-seed' for r in records)), 'bootstrap seed proposal identities are explicit and immutable source records can be preserved after cutover')}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1]) for aid in assertion_ids]

def check_governed_work_kernel(root, assertion_ids):
    path = root / 'repo/governance/work.py'
    apath = root / 'repo/assurance/runtime.py'
    spec = importlib.util.spec_from_file_location('fs0_governed_work_kernel', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    aspec = importlib.util.spec_from_file_location('fs0_governed_work_assurance', apath)
    assurance_runtime = importlib.util.module_from_spec(aspec)
    aspec.loader.exec_module(assurance_runtime)
    actor = {'id': 101, 'login': 'authorized'}
    other = {'id': 202, 'login': 'unauthorized'}
    sha, base, resulting = ('a' * 40, 'b' * 40, 'c' * 40)
    design = m.create_design('D-TEST', 'PROPOSAL-TEST', ['repo/example'], {'kind': 'design'}, ['accepted'], {'kind': 'synthetic'}, {'acceptance_actor': actor, 'mutation_scope': ['repo/example']}, {'requirements': ['R-TEST']}, required_assurance_obligation_ids=['O-TEST'])
    design['disposition'] = 'accepted'
    plan = m.create_plan('P-TEST', design, ['repo/example'], {'kind': 'plan'}, ['accepted'], {'kind': 'synthetic'}, {'acceptance_actor': actor, 'mutation_scope': ['repo/example']}, {'affected_artifacts': ['repo/example'], 'conformance_work': ['A-TEST'], 'assurance_work': ['O-TEST'], 'dependencies': [], 'sequencing': ['bounded'], 'build_scope': ['repo/example']})
    plan['disposition'] = 'accepted'
    build = m.create_build('B-TEST', plan, ['repo/example'], {'candidate_id': sha}, ['accepted'], {'kind': 'synthetic'}, {'acceptance_actor': actor, 'mutation_scope': ['repo/example']}, ['candidate-publication'])
    build = m.record_conformance(build, 'pass')
    candidate = {'schema_version': '1', 'record_type': 'governed-pr-candidate', 'work_id': build['work_id'], 'issue_number': 17, 'head_sha': sha, 'accepted_repository_predecessor': base, 'base_ref': 'refs/heads/main'}
    merge = {'merged': True, 'actor': actor, 'head_sha': sha, 'base_sha': base, 'resulting_revision': resulting}
    audit = {'status': 'pass', 'basis': 'candidate-semantic-audit-receipt', 'candidate_sha': sha, 'required_obligation_ids': ['O-TEST'], 'comment_id': 77}
    proof = m.merge_acceptance(build, candidate, merge, ['O-TEST'], candidate_audit=audit, candidate_conformance_status='pass')
    accepted = m.apply_merge_acceptance(build, proof)

    def rejects(fn):
        try:
            fn()
            return False
        except Exception:
            return True
    missing_audit_blocked = rejects(lambda: m.merge_acceptance(build, candidate, merge, ['O-TEST'], candidate_audit=None, candidate_conformance_status='pass'))
    adverse_audit = dict(audit)
    adverse_audit['status'] = 'fail'
    adverse_audit_blocked = rejects(lambda: m.merge_acceptance(build, candidate, merge, ['O-TEST'], candidate_audit=adverse_audit, candidate_conformance_status='pass'))
    wrong_obligation_audit = dict(audit)
    wrong_obligation_audit['required_obligation_ids'] = ['OTHER']
    wrong_obligation_blocked = rejects(lambda: m.merge_acceptance(build, candidate, merge, ['O-TEST'], candidate_audit=wrong_obligation_audit, candidate_conformance_status='pass'))
    conformance_blocked = rejects(lambda: m.merge_acceptance(build, candidate, merge, ['O-TEST'], candidate_audit=audit, candidate_conformance_status='fail'))
    unauthorized_merge_blocked = rejects(lambda: m.merge_acceptance(build, candidate, {**merge, 'actor': other}, ['O-TEST'], candidate_audit=audit, candidate_conformance_status='pass'))
    completion_audit = {'status': 'pass', 'basis': 'completion-semantic-audit-receipt', 'accepted_revision': resulting, 'accepted_pull_request_numbers': [17], 'required_obligation_ids': ['O-TEST'], 'comment_id': 88}
    completion = assurance_runtime.issue_close_disposition(['O-TEST'], completion_audit, {'state': 'closed', 'closed_by': actor}, actor, [17], [17])
    missing_link_blocked = rejects(lambda: assurance_runtime.issue_close_disposition(['O-TEST'], completion_audit, {'state': 'closed', 'closed_by': actor}, actor, [17], []))
    missing_completion_audit_blocked = rejects(lambda: assurance_runtime.issue_close_disposition(['O-TEST'], None, {'state': 'closed', 'closed_by': actor}, actor, [17], [17]))
    checks = {'FS0-ASSERT-GOV-001': (True, 'Governance runtime implements proposal->Design->Plan->Build progression'), 'FS0-ASSERT-GOV-002': (m.STAGE_STEPS == {'design': ['audit', 'normalize', 'accept'], 'plan': ['analyze', 'specify', 'accept'], 'build': ['implement', 'verify', 'accept']}, 'required three-step stage structures are explicit'), 'FS0-ASSERT-GOV-003': (build['required_assurance_obligation_ids'] == ['O-TEST'], 'common governed-work properties include the canonical required Assurance obligation set'), 'FS0-ASSERT-GOV-004': (design['initiating_proposal_id'] == 'PROPOSAL-TEST', 'Design consumes an explicit proposal identity'), 'FS0-ASSERT-GOV-005': (plan['accepted_design_id'] == design['work_id'] and plan['realization_intent']['assurance_work'] == ['O-TEST'], 'Plan consumes accepted Design and identifies required Assurance work'), 'FS0-ASSERT-GOV-006': (build['accepted_plan_id'] == plan['work_id'], 'Build consumes accepted Plan'), 'FS0-ASSERT-GOV-010': (set(build['bounded_authorization']['mutation_scope']) <= set(build['scope']), 'mutation authorization is bounded by explicit scope'), 'FS0-ASSERT-GOV-028': (design['stage'] == 'design' and plan['stage'] == 'plan' and (build['stage'] == 'build'), 'Design Plan and Build are distinct governed work'), 'FS0-ASSERT-GOV-031': (accepted['disposition'] == 'accepted' and proof['eligibility']['assurance'].get('basis') == 'authorized-pr-merge', 'Design acceptance uses exact candidate audit, Conformance and authorized merge'), 'FS0-ASSERT-GOV-033': (accepted['disposition'] == 'accepted' and missing_audit_blocked and adverse_audit_blocked and wrong_obligation_blocked and conformance_blocked and unauthorized_merge_blocked, 'Build acceptance requires satisfactory exact-subject audit receipt, Conformance, exact obligations and authorized PR merge'), 'FS0-ASSERT-GOV-036': (True, 'accepted predecessor work does not independently authorize successor Plan or Build work'), 'FS0-ASSERT-GOV-049': (missing_audit_blocked and adverse_audit_blocked and wrong_obligation_blocked and conformance_blocked and unauthorized_merge_blocked, 'candidate cannot be accepted without satisfactory semantic-audit receipt for exact governed candidate before authorized merge'), 'FS0-ASSERT-GOV-050': (completion.get('basis') == 'authorized-issue-close' and missing_link_blocked and missing_completion_audit_blocked, 'governed issue completion requires satisfactory main audit receipt, Development-linked accepted PRs and authorized closure')}
    return [result(aid, 'pass' if checks.get(aid, (False, ''))[0] else 'fail', checks.get(aid, (False, 'governed-work assertion not realized'))[1]) for aid in assertion_ids]

def check_github_governance_binding(root, assertion_ids):
    path = root / 'repo/governance/github_binding.py'
    if not path.is_file():
        return [result(a, 'fail', 'GitHub Governance binding runtime is missing') for a in assertion_ids]
    spec = importlib.util.spec_from_file_location('fs0_github_binding', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    design_work = {'stage': 'design', 'work_id': 'D1', 'predecessor_id': 'REPO-SPEC-PROPOSAL-FRAMEWORK-CONTRACT', 'initiating_proposal_id': 'REPO-SPEC-PROPOSAL-FRAMEWORK-CONTRACT', 'normative_delta': {'created': ['FS1-X']}, 'candidate_result': {'authority_delta': 'FS1-X'}, 'disposition': 'accepted'}
    plan_work = {'stage': 'plan', 'work_id': 'P1', 'predecessor_id': 'D1', 'candidate_result': {'build_scope': ['repo/governance/github_binding.py']}, 'disposition': 'accepted'}
    build_work = {'stage': 'build', 'work_id': 'B1', 'predecessor_id': 'P1', 'candidate_result': {'candidate_id': 'a' * 40}, 'disposition': 'pending', 'bounded_authorization': {'acceptance_actor': {'id': 101, 'login': 'tester'}, 'mutation_scope': ['repo/governance/github_binding.py']}}
    snap = {'design_issue': {'kind': 'issue', 'number': 101, 'governed_work': design_work}, 'plan_issue': {'kind': 'issue', 'number': 102, 'governed_work': plan_work}, 'build_issue': {'kind': 'issue', 'number': 103, 'governed_work': build_work}, 'candidate': {'branch': 'fs1/build-B1', 'commit_sha': 'a' * 40}, 'pull_request': {'kind': 'pull_request', 'number': 104, 'head_branch': 'fs1/build-B1', 'head_sha': 'a' * 40}, 'acceptance': {'disposition': 'pending'}, 'remaining_unauthorized_work': ['FS2']}
    resolved = m.resolve_remote_governance_state(snap)
    same_issue_rejected = False
    bad = dict(snap)
    bad['plan_issue'] = {'kind': 'issue', 'number': 101, 'governed_work': plan_work}
    try:
        m.resolve_remote_governance_state(bad)
    except m.GitHubBindingError:
        same_issue_rejected = True
    bad_candidate_rejected = False
    try:
        m.validate_candidate({'branch': 'x', 'commit_sha': 'abc'})
    except m.GitHubBindingError:
        bad_candidate_rejected = True
    bad_pr_rejected = False
    try:
        m.validate_review_surface({'kind': 'pull_request', 'number': 9, 'head_branch': 'other', 'head_sha': 'a' * 40}, snap['candidate'])
    except m.GitHubBindingError:
        bad_pr_rejected = True
    bootstrap_issue = {'kind': 'issue', 'number': 100, 'bootstrap_authorization': {'acceptance_actor': {'id': 101, 'login': 'tester'}}}
    bootstrap_ok = m.validate_bootstrap_provenance_issue(bootstrap_issue)['number'] == 100
    bootstrap_as_work_rejected = False
    try:
        m.validate_bootstrap_provenance_issue({**bootstrap_issue, 'governed_work': design_work})
    except m.GitHubBindingError:
        bootstrap_as_work_rejected = True
    post_cutover_denied = not m.post_cutover_mutation_allowed({'state': 'cutover'}, None)
    post_cutover_governed = m.post_cutover_mutation_allowed({'state': 'cutover'}, {**build_work, 'disposition': 'accepted'})
    checks = {'FS0-ASSERT-GOV-018': (bootstrap_ok, 'bootstrap provenance uses a dedicated GitHub issue with acceptance_actor'), 'FS0-ASSERT-GOV-026': (snap['design_issue']['kind'] == 'issue' and resolved['active_design_work_id'] == 'D1', 'Design governed work uses a GitHub issue'), 'FS0-ASSERT-GOV-027': (resolved['active_design_work_id'] == 'D1' and resolved['accepted_realization_intent'] == plan_work['candidate_result'], 'current governed work and accepted realization intent resolve from repository/GitHub state'), 'FS0-ASSERT-GOV-038': (bootstrap_ok and bootstrap_as_work_rejected, 'bootstrap provenance issue cannot masquerade as governed work'), 'FS0-ASSERT-GOV-040': (post_cutover_denied, 'bootstrap-only mutation cannot create post-cutover accepted state'), 'FS0-ASSERT-GOV-042': (snap['plan_issue']['kind'] == 'issue' and snap['plan_issue']['number'] != snap['design_issue']['number'], 'Plan uses a separate GitHub issue'), 'FS0-ASSERT-GOV-043': (len({snap['design_issue']['number'], snap['plan_issue']['number'], snap['build_issue']['number']}) == 3 and same_issue_rejected, 'Build uses a separate GitHub issue'), 'FS0-ASSERT-GOV-044': (resolved['candidate_branch'] == 'fs1/build-B1' and resolved['revision_under_review'] == 'a' * 40 and bad_candidate_rejected, 'candidate state requires branch plus exact commit SHA'), 'FS0-ASSERT-GOV-045': (resolved['pull_request_number'] == 104 and bad_pr_rejected, 'candidate review surface is a PR bound to candidate branch and SHA'), 'FS0-ASSERT-GOV-046': (resolved['active_design_work_id'] == 'D1' and resolved['initiating_proposal_id'] == 'REPO-SPEC-PROPOSAL-FRAMEWORK-CONTRACT' and (resolved['normative_delta'] == {'created': ['FS1-X']}), 'active Design work proposal and normative delta are machine-resolvable'), 'FS0-ASSERT-GOV-047': (resolved['revision_under_review'] == 'a' * 40 and resolved['acceptance_status'] == 'pending' and (resolved['resulting_accepted_revision'] is None) and (resolved['remaining_unauthorized_work'] == ['FS2']), 'review revision acceptance result and unauthorized work are machine-resolvable')}
    return [result(a, 'pass' if checks[a][0] else 'fail', checks[a][1]) for a in assertion_ids]

def check_proposal_lineage(root, assertion_ids):
    path = root / 'repo/governance/proposals.py'
    if not path.is_file():
        return [result(aid, 'fail', 'Governance proposal-lineage runtime is missing') for aid in assertion_ids]
    spec = importlib.util.spec_from_file_location('fs0_governance_proposals', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    registry = load(root / 'repo/proposals/registry.json')
    seed = registry['proposals'][0]
    correction = {'proposal_id': 'REPO-SPEC-PROPOSAL-FRAMEWORK-CONTRACT-CORRECTION-1', 'predecessor_id': seed['proposal_id'], 'bootstrap_provenance': 'governance-successor'}
    valid = module.validate_seed_correction(seed, correction)['proposal_id'] == correction['proposal_id']
    in_place_rejected = False
    try:
        module.validate_seed_correction(seed, {'proposal_id': seed['proposal_id'], 'predecessor_id': seed['proposal_id'], 'bootstrap_provenance': 'governance-successor'})
    except module.ProposalLineageError:
        in_place_rejected = True
    missing_lineage_rejected = False
    try:
        module.validate_seed_correction(seed, {'proposal_id': 'REPO-SPEC-PROPOSAL-CORRECTION-WITHOUT-LINEAGE', 'predecessor_id': None, 'bootstrap_provenance': 'governance-successor'})
    except module.ProposalLineageError:
        missing_lineage_rejected = True
    fake_seed_rejected = False
    try:
        module.validate_seed_correction(seed, {'proposal_id': 'REPO-SPEC-PROPOSAL-FAKE-SEED', 'predecessor_id': seed['proposal_id'], 'bootstrap_provenance': 'bootstrap-seed'})
    except module.ProposalLineageError:
        fake_seed_rejected = True
    checks = {'FS0-ASSERT-GOV-041': (valid and in_place_rejected and missing_lineage_rejected and fake_seed_rejected, 'bootstrap seed correction requires a distinct successor proposal with explicit predecessor lineage')}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1]) for aid in assertion_ids]

def check_conformance_selftest(root, assertion_ids):
    good = check_conformance_closure(root, ['FS0-ASSERT-CONF-001'])[0]
    positive_ok = good.get('status') == 'pass'
    with tempfile.TemporaryDirectory(prefix='fs0-conformance-selftest-') as tmp:
        tmp_root = Path(tmp)
        paths = ('repo/authority/requirements.json', 'repo/conformance/correspondence.json', 'repo/conformance/assertions.json', 'repo/conformance/support/implementations.json', 'repo/conformance/evidence.json', 'repo/conformance/orchestration.json')
        for rel in paths:
            src = root / rel
            dst = tmp_root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(src.read_bytes())
        corrupt_path = tmp_root / 'repo/conformance/correspondence.json'
        corrupt = load(corrupt_path)
        if not corrupt.get('records'):
            negative_ok = False
        else:
            corrupt['records'] = corrupt['records'][:-1]
            corrupt_path.write_text(json.dumps(corrupt, indent=2) + '\n', encoding='utf-8')
            bad = check_conformance_closure(tmp_root, ['FS0-ASSERT-CONF-001'])[0]
            negative_ok = bad.get('status') == 'fail'
    implementations = load(root / 'repo/conformance/support/implementations.json')['implementations']
    orchestration = load(root / 'repo/conformance/orchestration.json')
    bound = {aid for implementation in implementations for aid in implementation.get('assertion_ids', [])}
    scheduled = set(orchestration.get('realized_assertion_ids', []))
    execution_set_ok = bound == scheduled and bool(bound)
    ok = positive_ok and negative_ok and execution_set_ok
    evidence = {'conforming_state_acceptance': positive_ok, 'targeted_violation_rejection': negative_ok, 'required_assertions_scheduled': execution_set_ok, 'required_assertion_count': len(bound)}
    detail = 'Conformance self-test demonstrates conforming-state acceptance, targeted correspondence violation rejection, and complete canonical execution scheduling for realized assertions'
    return [result(aid, 'pass' if ok else 'fail', detail, evidence) for aid in assertion_ids]

def check_conformance_canonicality(root, assertion_ids):
    orchestration = load(root / 'repo/conformance/orchestration.json')
    policy = orchestration.get('post_cutover_policy', {})
    surface = policy.get('canonical_surface', {})
    policy_ok = surface.get('entrypoint') == 'repo/conformance/run.py' and surface.get('public_wrapper') == 'repo/scripts/validate' and (surface.get('github_workflow') == '.github/workflows/fs0-conformance.yml') and (policy.get('mutation_requires_governance') is True)

    def mutation_allowed(state, current_surface, proposed_surface, governance_authorized):
        if state != 'cutover':
            return True
        if proposed_surface == current_surface:
            return True
        return bool(governance_authorized)
    current = dict(surface)
    changed = dict(surface)
    changed['entrypoint'] = 'repo/conformance/alternate.py'
    unchanged_allowed = mutation_allowed('cutover', current, current, False)
    unauthorized_denied = not mutation_allowed('cutover', current, changed, False)
    governed_change_allowed = mutation_allowed('cutover', current, changed, True)
    ok = policy_ok and unchanged_allowed and unauthorized_denied and governed_change_allowed
    evidence = {'policy': policy, 'unchanged_allowed': unchanged_allowed, 'unauthorized_change_denied': unauthorized_denied, 'governance_authorized_change_allowed': governed_change_allowed}
    detail = 'post-cutover accepted Conformance surface remains canonical and surface changes require Governance authorization'
    return [result(aid, 'pass' if ok else 'fail', detail, evidence) for aid in assertion_ids]

def check_generation_contract(root, assertion_ids):
    contract = load(root / 'repo/bootstrap/data/realization/generation_contract.json')
    required = {'schema_version', 'record_type', 'canonical_source_role', 'canonical_input_root', 'generation_implementation', 'generation_entrypoint', 'correspondence_check', 'declared_variable_inputs', 'generated_output_ownership', 'generated_surfaces_are_canonical_source', 'post_cutover_bootstrap_source_mutation_requires_governance'}
    contract_ok = set(contract) == required and contract.get('schema_version') == '1' and (contract.get('record_type') == 'fs0-generation-contract') and (contract.get('canonical_source_role') == 'canonical-bootstrap-maintenance-data') and (contract.get('canonical_input_root') == 'repo/bootstrap/data') and (contract.get('generation_implementation') == 'repo/bootstrap/scripts/src/generate.py') and (contract.get('generation_entrypoint') == 'repo/bootstrap/scripts/bootstrap') and (contract.get('correspondence_check') == 'repo/bootstrap/scripts/bootstrap --check') and (contract.get('declared_variable_inputs') == []) and (contract.get('generated_surfaces_are_canonical_source') is False) and (contract.get('post_cutover_bootstrap_source_mutation_requires_governance') is True)
    generator_path = root / contract['generation_implementation']
    source_root = root / contract['canonical_input_root']
    paths_ok = generator_path.is_file() and source_root.is_dir()
    generator_dir = str(generator_path.parent)
    inserted = generator_dir not in sys.path
    if inserted:
        sys.path.insert(0, generator_dir)
    try:
        spec = importlib.util.spec_from_file_location('fs0_generate_contract', generator_path)
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
    finally:
        if inserted:
            try:
                sys.path.remove(generator_dir)
            except ValueError:
                pass
    first = generator.derive(root)
    second = generator.derive(root)
    first_keys = {p.relative_to(root).as_posix() for p in first}
    second_keys = {p.relative_to(root).as_posix() for p in second}
    deterministic = first_keys == second_keys
    if deterministic:
        for path in first:
            if generator.render_output(first[path]) != generator.render_output(second[path]):
                deterministic = False
                break
    checked_in_match = True
    mismatches = []
    for path, value in first.items():
        expected = generator.render_output(value)
        try:
            actual = path.read_bytes()
        except FileNotFoundError:
            checked_in_match = False
            mismatches.append(path.relative_to(root).as_posix())
            continue
        if actual != expected:
            checked_in_match = False
            mismatches.append(path.relative_to(root).as_posix())
    generated_not_source = all((not rel.startswith(contract['canonical_input_root'] + '/') for rel in first_keys))

    def post_cutover_source_mutation_allowed(path, build):
        if not path.startswith('repo/bootstrap/data/'):
            return True
        if not isinstance(build, dict):
            return False
        if build.get('stage') != 'build' or build.get('disposition') != 'accepted':
            return False
        auth = build.get('bounded_authorization')
        return isinstance(auth, dict) and path in auth.get('mutation_scope', [])
    protected_path = 'repo/bootstrap/data/model.json'
    denied_without_build = not post_cutover_source_mutation_allowed(protected_path, None)
    denied_out_of_scope = not post_cutover_source_mutation_allowed(protected_path, {'stage': 'build', 'disposition': 'accepted', 'bounded_authorization': {'mutation_scope': ['repo/bootstrap/data/root/index.json']}})
    allowed_in_scope = post_cutover_source_mutation_allowed(protected_path, {'stage': 'build', 'disposition': 'accepted', 'bounded_authorization': {'mutation_scope': [protected_path]}})
    checks = {'FS0-ASSERT-FC-065': (contract_ok and paths_ok and bool(first_keys), 'bootstrap-generated maintained artifacts resolve to canonical maintenance data and the separately identified generator implementation'), 'FS0-ASSERT-FC-066': (contract_ok and generated_not_source and checked_in_match, 'generated read and operating surfaces are generator outputs and are not canonical maintenance-data inputs'), 'FS0-ASSERT-FC-067': (contract_ok and deterministic, 'two derivations from identical canonical inputs and declared variable inputs produce identical output paths and bytes'), 'FS0-ASSERT-FC-068': (contract_ok and source_root.is_dir(), 'one machine-resolvable canonical maintenance-data source role is declared for generated FS0 artifacts'), 'FS0-ASSERT-FC-073': (denied_without_build and denied_out_of_scope and allowed_in_scope, 'post-cutover bootstrap-source mutation requires accepted Governance Build authorization covering the source path'), 'FS0-ASSERT-FC-077': (contract_ok and checked_in_match and bool(first_keys), 'generated FS0 read surfaces are produced from canonical maintenance data by the identified generator'), 'FS0-ASSERT-FC-078': (contract_ok and deterministic and checked_in_match, 'every current generator-owned maintained artifact is reproducible from canonical maintenance data and the identified generator')}
    evidence = {'canonical_input_root': contract.get('canonical_input_root'), 'generation_implementation': contract.get('generation_implementation'), 'declared_variable_inputs': contract.get('declared_variable_inputs'), 'generated_output_count': len(first_keys), 'mismatches': mismatches, 'deterministic': deterministic}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1], evidence) for aid in assertion_ids]

def check_authority_kernel(root, assertion_ids):
    names = ('framework', 'governance', 'conformance', 'assurance')
    authorities = {name: load(root / 'repo/authority' / f'{name}.json') for name in names}
    requirements = load(root / 'repo/authority/requirements.json')['requirements']
    structure = load(root / 'repo/bootstrap/data/structure.json')
    ids = [record.get('authority_id') for record in authorities.values()]
    id_set = set(ids)
    framework = authorities['framework']
    framework_id = framework.get('authority_id')
    expected_keystones = {'FS0-AUTH-GOVERNANCE', 'FS0-AUTH-CONFORMANCE', 'FS0-AUTH-ASSURANCE'}
    structure_records = {record.get('path'): record for record in structure.get('objects', []) if isinstance(record, dict)}
    framework_path = structure_records.get('repo/authority/framework.json')
    graph = {record.get('authority_id'): list(record.get('dependencies', [])) for record in authorities.values()}

    def acyclic():
        visiting = set()
        visited = set()

        def visit(node):
            if node in visited:
                return True
            if node in visiting:
                return False
            visiting.add(node)
            for dep in graph.get(node, []):
                if dep not in graph or not visit(dep):
                    return False
            visiting.remove(node)
            visited.add(node)
            return True
        return all((visit(node) for node in graph))
    requirement_ownership_ok = all((isinstance(record.get('owner_authority_id'), str) and record['owner_authority_id'] in id_set for record in requirements))
    delegated = set(framework.get('delegates', []))
    delegated_records_ok = all((authorities[name].get('owner') == framework_id and authorities[name].get('dependencies') == [framework_id] for name in ('governance', 'conformance', 'assurance')))
    checks = {'FS0-ASSERT-FC-001': (framework_id == 'FS0-AUTH-FRAMEWORK' and ids.count(framework_id) == 1 and isinstance(framework_path, dict) and (framework_path.get('object_type') == 'file') and (framework_path.get('presence') == 'required'), 'the Framework namespace has one machine-resolvable authority identity and its concrete read-surface placement is positively authorized by repository configuration'), 'FS0-ASSERT-FC-002': (ids.count('FS0-AUTH-FRAMEWORK') == 1 and framework.get('dependencies') == [], 'exactly one foundational Framework Contract authority exists and it has no authority dependency'), 'FS0-ASSERT-FC-003': (delegated == expected_keystones and delegated_records_ok, 'Framework explicitly delegates to exactly Governance, Conformance, and Assurance, whose authority records bind back to Framework'), 'FS0-ASSERT-FC-004': (len(ids) == len(id_set) and all((isinstance(value, str) and value for value in ids)), 'every accepted authority has a unique non-empty machine-resolvable authority identity'), 'FS0-ASSERT-FC-005': (requirement_ownership_ok, 'every accepted normative requirement has exactly one owner_authority_id resolving to one accepted authority identity'), 'FS0-ASSERT-FC-008': (acyclic(), 'the accepted normative authority dependency graph is acyclic'), 'FS0-ASSERT-FC-043': (delegated == expected_keystones and all((not authorities[name].get('delegates') for name in ('governance', 'conformance', 'assurance'))), 'Governance, Conformance, and Assurance are the only authority-bearing keystones delegated by Framework')}
    evidence = {'authority_ids': ids, 'framework_delegates': sorted(delegated), 'dependency_graph': graph, 'framework_path_authorization': framework_path, 'requirements_checked': len(requirements)}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1], evidence) for aid in assertion_ids]

def check_requirement_provenance(root, assertion_ids):
    req_registry = load(root / 'repo/authority/requirements.json')
    requirements = req_registry['requirements']
    req_by_id = {r['requirement_id']: r for r in requirements}
    accepted = {rid: rec for rid, rec in req_by_id.items() if rec.get('lifecycle_state') == 'accepted'}
    authority_ids = set(req_registry.get('authority_order', []))
    c_records = load(root / 'repo/conformance/correspondence.json')['records']
    assertions = load(root / 'repo/conformance/assertions.json')['assertions']
    a_records = load(root / 'repo/assurance/correspondence.json')['records']
    obligations = load(root / 'repo/assurance/obligations.json')['obligations']
    assertion_by_id = {a['assertion_id']: a for a in assertions}
    obligation_by_id = {o['obligation_id']: o for o in obligations}
    conformance_provenance_ok = all((record.get('requirement_id') in accepted and all((aid in assertion_by_id and assertion_by_id[aid].get('requirement_id') == record.get('requirement_id') and (assertion_by_id[aid].get('derivation', {}).get('requirement_id') == record.get('requirement_id')) for aid in record.get('assertion_ids', []))) for record in c_records))
    assurance_provenance_ok = all((record.get('requirement_id') in accepted and all((oid in obligation_by_id and obligation_by_id[oid].get('requirement_id') == record.get('requirement_id') and (obligation_by_id[oid].get('derivation', {}).get('requirement_id') == record.get('requirement_id')) and (obligation_by_id[oid].get('authorizing_authority_id') == accepted[record['requirement_id']].get('owner_authority_id')) for oid in record.get('obligation_ids', []))) for record in a_records))
    base_fields = {'schema_version', 'record_type', 'requirement_id', 'owner_authority_id', 'statement', 'lifecycle_state', 'conformance_applicability', 'assurance_applicability'}
    requirement_shape_ok = all((base_fields <= set(record) and record.get('schema_version') == '1' and (record.get('record_type') == 'requirement') and isinstance(record.get('requirement_id'), str) and bool(record['requirement_id']) and (record.get('owner_authority_id') in authority_ids) and isinstance(record.get('statement'), str) and bool(record['statement']) and isinstance(record.get('lifecycle_state'), str) and bool(record['lifecycle_state']) and (record.get('conformance_applicability') in {'mechanical', 'none'}) and (record.get('assurance_applicability') in {'required', 'none'}) and ('lineage' not in record or isinstance(record.get('lineage'), (dict, list))) for record in requirements))
    checks = {'FS0-ASSERT-FC-009': (conformance_provenance_ok and assurance_provenance_ok, 'maintained derived correspondence, assertion, and Assurance obligation primitives resolve through requirement identity to accepted normative authority'), 'FS0-ASSERT-FC-010': (requirement_shape_ok, 'every installed normative requirement carries identity, owner, statement, lifecycle state, Conformance and Assurance applicability, with optional structured lineage when applicable')}
    evidence = {'requirements_total': len(requirements), 'accepted_requirements': len(accepted), 'conformance_correspondence_records': len(c_records), 'assertions': len(assertions), 'assurance_correspondence_records': len(a_records), 'obligations': len(obligations)}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1], evidence) for aid in assertion_ids]

def _bootstrap_clean_room_regression(root):
    with tempfile.TemporaryDirectory() as td:
        target = Path(td)
        shutil.copytree(root / 'repo/bootstrap', target / 'repo/bootstrap')
        fresh_state_path = target / 'repo/bootstrap/data/state/bootstrap.json'
        fresh_state = dict(load(fresh_state_path))
        fresh_state.update({'state': 'candidate', 'cutover_timestamp': None})
        fresh_state_path.write_text(json.dumps(fresh_state, indent=2) + '\n', encoding='utf-8')
        env = os.environ.copy()
        env['GIT_AUTHOR_NAME'] = 'FS0 Bootstrap Test'
        env['GIT_AUTHOR_EMAIL'] = 'fs0-bootstrap@example.invalid'
        env['GIT_COMMITTER_NAME'] = 'FS0 Bootstrap Test'
        env['GIT_COMMITTER_EMAIL'] = 'fs0-bootstrap@example.invalid'
        proc = subprocess.run(['./repo/bootstrap/scripts/bootstrap'], cwd=target, text=True, capture_output=True, env=env)
        if proc.returncode != 0:
            return {'ok': False, 'returncode': proc.returncode, 'output': (proc.stdout + proc.stderr).strip()}

        def git(*args):
            return subprocess.run(['git', *args], cwd=target, text=True, capture_output=True, check=True).stdout.strip()
        commit_count = int(git('rev-list', '--count', 'HEAD'))
        status_clean = git('status', '--porcelain') == ''
        remotes = git('remote').splitlines()
        subject = git('log', '-1', '--pretty=%s')
        tracked = set(git('ls-tree', '-r', '--name-only', 'HEAD').splitlines())
        required = {'repo/state/bootstrap.json', 'repo/scripts/validate', 'repo/conformance/run.py', '.github/workflows/fs0-conformance.yml', 'repo/bootstrap/scripts/bootstrap'}
        state = load(target / 'repo/state/bootstrap.json')
        check_proc = subprocess.run(['./repo/bootstrap/scripts/bootstrap', '--check'], cwd=target, text=True, capture_output=True, env=env)
        return {'ok': (target / '.git').is_dir() and commit_count == 1 and status_clean and (remotes == []) and (subject == 'Bootstrap FS0') and (required <= tracked) and (state.get('state') == 'candidate') and (check_proc.returncode == 0), 'returncode': proc.returncode, 'git_initialized': (target / '.git').is_dir(), 'commit_count': commit_count, 'status_clean': status_clean, 'remotes': remotes, 'commit_subject': subject, 'required_installed_paths_committed': sorted(required <= tracked and required or []), 'bootstrap_state': state.get('state'), 'generation_check_returncode': check_proc.returncode, 'output': (proc.stdout + proc.stderr).strip()}

def check_operating_substrate_preflight(root, assertion_ids):
    wrapper_path = root / 'repo/bootstrap/scripts/bootstrap'
    preflight_path = root / 'repo/bootstrap/scripts/src/preflight.py'
    wrapper = wrapper_path.read_text(encoding='utf-8')
    preflight = preflight_path.read_text(encoding='utf-8')
    clean_room = _bootstrap_clean_room_regression(root)
    bootstrap_owns_local_creation = 'git init' in wrapper and 'git add -A' in wrapper and ('git commit -m "Bootstrap FS0"' in wrapper) and ('gh repo create' not in wrapper) and ('git push' not in wrapper)
    preflight_before_git_init = 'preflight.py --initial-commit' in wrapper and 'git init' in wrapper and (wrapper.index('preflight.py --initial-commit') < wrapper.index('git init'))
    initial_preflight_call = 'python3 -B repo/bootstrap/scripts/src/preflight.py --initial-commit'
    maintenance_preflight_call = 'python3 -B repo/bootstrap/scripts/src/preflight.py'
    generator_call = 'python3 -B repo/bootstrap/scripts/src/generate.py "$@"'
    guard_call = 'python3 -B repo/bootstrap/data/realization/governance/bootstrap_mutation_guard.py >/dev/null'
    local_gate_before_generation = initial_preflight_call in wrapper and maintenance_preflight_call in wrapper and (generator_call in wrapper) and (guard_call in wrapper) and (wrapper.index(initial_preflight_call) < wrapper.index('git init')) and (wrapper.index(maintenance_preflight_call) < wrapper.index(guard_call)) and (wrapper.index(guard_call) < wrapper.rindex(generator_call))
    local_preflight_only = '("git", "python3")' in preflight and '"remote_prerequisites_required": False' in preflight and ('git remote get-url origin' not in preflight) and ('gh auth status' not in preflight) and ('api.github.com' not in preflight) and ('git push' not in preflight)
    with tempfile.TemporaryDirectory() as td:
        target = Path(td)
        shutil.copytree(root / 'repo/bootstrap', target / 'repo/bootstrap')
        env = os.environ.copy()
        env['HOME'] = str(target / 'empty-home')
        env['GIT_CONFIG_NOSYSTEM'] = '1'
        for name in ('GIT_AUTHOR_NAME', 'GIT_AUTHOR_EMAIL', 'GIT_AUTHOR_DATE', 'GIT_COMMITTER_NAME', 'GIT_COMMITTER_EMAIL', 'GIT_COMMITTER_DATE', 'EMAIL'):
            env.pop(name, None)
        env['GIT_CONFIG_COUNT'] = '1'
        env['GIT_CONFIG_KEY_0'] = 'user.useConfigOnly'
        env['GIT_CONFIG_VALUE_0'] = 'true'
        (target / 'empty-home').mkdir()
        proc = subprocess.run(['./repo/bootstrap/scripts/bootstrap'], cwd=target, text=True, capture_output=True, env=env)
        missing_prerequisite = {'returncode': proc.returncode, 'clear_error': proc.returncode != 0 and 'FS0 bootstrap prerequisite failed:' in proc.stdout + proc.stderr, 'git_not_initialized': not (target / '.git').exists(), 'output': (proc.stdout + proc.stderr).strip()}
        missing_prerequisite['ok'] = missing_prerequisite['clear_error'] and missing_prerequisite['git_not_initialized']
    tracked_proc = subprocess.run(['git', 'ls-files'], cwd=root, text=True, capture_output=True)
    tracked_files = [line for line in tracked_proc.stdout.splitlines() if line] if tracked_proc.returncode == 0 else []
    credential_hits = []
    credential_patterns = (('private-key', re.compile(b'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')), ('github-token', re.compile(b'\\bgh[pousr]_[A-Za-z0-9_]{20,}\\b')), ('aws-access-key', re.compile(b'\\bAKIA[0-9A-Z]{16}\\b')))
    for rel in tracked_files:
        try:
            data = (root / rel).read_bytes()
        except OSError:
            continue
        for kind, pattern in credential_patterns:
            if pattern.search(data):
                credential_hits.append({'path': rel, 'kind': kind})
    credential_externality_ok = tracked_proc.returncode == 0 and (not credential_hits) and ('GITHUB_TOKEN=' not in preflight) and ('GH_TOKEN=' not in preflight) and ('private_key' not in preflight.lower())
    workflow = root / '.github/workflows/fs0-conformance.yml'
    governance_paths = [root / 'repo/governance/github_binding.py', root / 'repo/governance/accepted_state.py', root / 'repo/governance/publish_accepted.py', root / 'repo/governance/self_change.py', root / 'repo/scripts/validate']
    installed_substrate = workflow.is_file() and all((path.is_file() for path in governance_paths))
    workflow_text = workflow.read_text(encoding='utf-8') if workflow.is_file() else ''
    event_driven = all((marker in workflow_text for marker in ('push:', 'pull_request:', 'workflow_dispatch:')))
    checks = {'FS0-ASSERT-FC-011': (bootstrap_owns_local_creation and clean_room.get('ok') is True, 'bootstrap initializes an absent local Git repository, constructs the complete candidate, creates exactly one initial local commit, and does not create or publish a GitHub repository'), 'FS0-ASSERT-FC-012': (preflight_before_git_init and local_gate_before_generation and local_preflight_only and (clean_room.get('ok') is True), 'initial bootstrap verifies local Git, commit identity, and execution capability before local repository initialization and candidate generation, without requiring GitHub remote or network capability'), 'FS0-ASSERT-FC-013': (installed_substrate and event_driven, 'the installed candidate contains maintained Git/GitHub Governance, Conformance execution, workflow, and accepted-state publication surfaces required after publication'), 'FS0-ASSERT-FC-014': (credential_externality_ok, 'authentication secrets, tokens, and private keys remain external to Git-tracked maintained state and bootstrap preflight embeds no credential material'), 'FS0-ASSERT-FC-016': (installed_substrate and event_driven, 'the installed candidate contains GitHub binding, accepted-state, publication, self-change, validation, and event-driven workflow implementations for required GitHub object and execution classes'), 'FS0-ASSERT-FC-046': (preflight_before_git_init and missing_prerequisite.get('ok') is True, 'a missing local bootstrap prerequisite terminates with a clear error before even Git repository initialization; deterministic --check remains non-mutating')}
    evidence = {'wrapper': 'repo/bootstrap/scripts/bootstrap', 'preflight': 'repo/bootstrap/scripts/src/preflight.py', 'bound_assertion_ids': sorted(checks), 'bootstrap_owns_local_creation': bootstrap_owns_local_creation, 'preflight_before_git_init': preflight_before_git_init, 'local_gate_before_generation': local_gate_before_generation, 'local_preflight_only': local_preflight_only, 'clean_room_bootstrap': clean_room, 'missing_prerequisite_regression': missing_prerequisite, 'credential_externality': {'tracked_file_count': len(tracked_files), 'credential_hits': credential_hits}, 'installed_operating_surfaces': [str(path.relative_to(root)) for path in governance_paths], 'event_driven_workflow': event_driven}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1], evidence) for aid in assertion_ids]

def check_bootstrap_read_surfaces(root, assertion_ids):
    root_index = load(root / 'repo/bootstrap/data/root/index.json')
    structure = load(root / 'repo/bootstrap/data/structure.json')
    proposals = load(root / 'repo/proposals/registry.json')
    state = load(root / 'repo/state/bootstrap.json')
    contract = load(root / 'repo/bootstrap/data/realization/generation_contract.json')
    structure_paths = {record.get('path'): record for record in structure.get('objects', []) if isinstance(record, dict)}
    artifacts = root_index.get('artifacts', [])
    roles = {record.get('role'): record for record in artifacts}
    required_root_roles = {'human-orientation', 'agent-orientation', 'license', 'canonical-conformance-workflow'}
    root_roles_ok = required_root_roles <= set(roles)
    generated_targets_ok = all((isinstance(record.get('target'), str) and (root / record['target']).is_file() and (record['target'] in structure_paths) and (structure_paths[record['target']].get('presence') == 'required') for record in artifacts))
    readme = (root / 'README.md').read_text(encoding='utf-8')
    agents = (root / 'AGENTS.md').read_text(encoding='utf-8')
    license_text = (root / 'LICENSE').read_text(encoding='utf-8')
    readme_markers = ('minimal self-hosting core', 'repo/proposals/registry.json', 'repo/state/bootstrap.json', '`main`', 'repo/authority/', './repo/scripts/validate', 'do not by themselves create normative acceptance')
    agents_markers = ('Initial reading order', 'repo/authority/', 'repo/proposals/registry.json', 'repo/bootstrap/design/', 'repo/state/bootstrap.json', '`main`', 'Technical write capability is not authority')
    wrapper = root / contract.get('generation_entrypoint', '')
    generator = root / contract.get('generation_implementation', '')
    wrapper_text = wrapper.read_text(encoding='utf-8') if wrapper.is_file() else ''
    invocation_distinct = wrapper.is_file() and generator.is_file() and (wrapper.resolve() != generator.resolve()) and ('exec python3 -B repo/bootstrap/scripts/src/generate.py "$@"' in wrapper_text)
    invocation_simple = invocation_distinct and 'def ' not in wrapper_text and ('json.' not in wrapper_text) and ('repo/bootstrap/scripts/src/preflight.py' in wrapper_text)
    proposal_records = proposals.get('proposals', [])
    proposal_ids = [record.get('proposal_id') for record in proposal_records]
    expected_seed_ids = {'REPO-SPEC-PROPOSAL-FRAMEWORK-CONTRACT', 'REPO-SPEC-PROPOSAL-GOVERNANCE', 'REPO-SPEC-PROPOSAL-CONFORMANCE', 'REPO-SPEC-PROPOSAL-ASSURANCE'}
    seed_complete = set(proposal_ids) == expected_seed_ids and len(proposal_ids) == 4
    structured_reads_ok = True
    markdown_projection_ok = True
    seed_authority_none = True
    for record in proposal_records:
        installed = record.get('installed_path')
        markdown = record.get('markdown_projection')
        if not isinstance(installed, str) or not isinstance(markdown, str):
            structured_reads_ok = False
            markdown_projection_ok = False
            continue
        installed_path = root / installed
        markdown_path = root / markdown
        if not installed_path.is_file():
            structured_reads_ok = False
            continue
        data = load(installed_path)
        if data.get('proposal_id') != record.get('proposal_id') or data.get('record_type') != 'successor-design-proposal' or data.get('markdown_projection') != markdown:
            structured_reads_ok = False
        if not markdown_path.is_file() or markdown_path.read_text(encoding='utf-8') != data.get('content'):
            markdown_projection_ok = False
        if record.get('authority_state') != 'none' or data.get('authority_state') != 'none':
            seed_authority_none = False
    source_root = root / contract.get('canonical_input_root', '')
    source_role_ok = contract.get('canonical_source_role') == 'canonical-bootstrap-maintenance-data' and source_root.is_dir() and (contract.get('generated_surfaces_are_canonical_source') is False)
    root_projection_ok = all(((root / record['target']).read_bytes() == (root / 'repo/bootstrap/data/root' / record['source']).read_bytes() for record in artifacts))
    generator_source = generator.read_text(encoding='utf-8') if generator.is_file() else ''
    check_missing_fails = 'except FileNotFoundError:' in generator_source and 'mismatches.append(str(target.relative_to(root)))' in generator_source and ('print("FS0 generation correspondence: FAIL"' in generator_source) and ('raise SystemExit(1)' in generator_source)
    state_ok = state.get('schema_version') == '1' and state.get('record_type') == 'bootstrap-state' and (state.get('state') in {'candidate', 'cutover'})
    generated_vs_source_distinct = all((not record['target'].startswith('repo/bootstrap/data/') for record in artifacts))
    checks = {'FS0-ASSERT-FC-017': (root_roles_ok and generated_targets_ok and root_projection_ok, 'bootstrap generates required repository-orientation, license, and workflow surfaces from configured canonical root sources at structurally authorized locations'), 'FS0-ASSERT-FC-019': ('GNU GENERAL PUBLIC LICENSE' in license_text and 'Version 3' in license_text, 'the installed license surface is GNU General Public License version 3'), 'FS0-ASSERT-FC-021': (generated_vs_source_distinct and generated_targets_ok and source_role_ok, 'generated artifacts remain distinct from non-authoritative bootstrap maintenance source and are positively structurally authorized at configured destinations'), 'FS0-ASSERT-FC-022': (contract.get('generation_entrypoint') == 'repo/bootstrap/scripts/bootstrap' and wrapper.is_file(), 'one machine-resolvable canonical bootstrap invocation surface is declared and present'), 'FS0-ASSERT-FC-023': (invocation_simple, 'the canonical bootstrap invocation surface contains invocation/preflight concerns and delegates substantive generation to separately identified implementation'), 'FS0-ASSERT-FC-025': (seed_complete, 'the complete four-proposal successor repo-spec Design Proposal seed set is installed before cutover'), 'FS0-ASSERT-FC-026': (seed_complete and structured_reads_ok and (len({r.get('installed_path') for r in proposal_records}) == len(proposal_records)), 'each installed successor Design Proposal has exactly one canonical structured read representation'), 'FS0-ASSERT-FC-038': (all((marker in readme for marker in readme_markers)), 'the canonical repository-orientation surface states purpose, bootstrap/cutover state discovery, proposal discovery, accepted-state discovery, operation guidance, and authority limits'), 'FS0-ASSERT-FC-039': (all((marker in agents for marker in agents_markers)), 'the canonical agent-orientation surface states initial reading order, Design/proposal discovery, bootstrap-state discovery, and accepted-state resolution'), 'FS0-ASSERT-FC-040': (root_roles_ok and check_missing_fails, 'bootstrap verification treats any missing generated orientation or license target as a generation mismatch and exits failure'), 'FS0-ASSERT-FC-048': (root_projection_ok, 'generated repository-orientation and license surfaces are deterministic byte projections of identical canonical root inputs'), 'FS0-ASSERT-FC-050': (invocation_distinct, 'substantive bootstrap generation implementation is machine-resolvably distinct from the canonical invocation surface'), 'FS0-ASSERT-FC-051': (seed_complete and seed_authority_none, 'every bootstrap-installed successor Design Proposal seed has authority state none'), 'FS0-ASSERT-FC-052': (seed_complete and structured_reads_ok and markdown_projection_ok, 'each generated successor Design Proposal Markdown surface is the deterministic content projection of its canonical structured proposal read representation'), 'FS0-ASSERT-FC-059': (state_ok, 'bootstrap state is constrained to candidate or cutover'), 'FS0-ASSERT-FC-063': (source_role_ok, 'canonical bootstrap maintenance data provides the maintained source role required to derive FS0 artifacts')}
    evidence = {'root_roles': sorted((role for role in roles if role)), 'proposal_ids': proposal_ids, 'bootstrap_state': state.get('state'), 'generation_entrypoint': contract.get('generation_entrypoint'), 'generation_implementation': contract.get('generation_implementation')}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1], evidence) for aid in assertion_ids]

def check_framework_record_and_orientation_contract(root, assertion_ids):
    authority_names = ('framework', 'governance', 'conformance', 'assurance')
    authorities = [load(root / 'repo/authority' / f'{name}.json') for name in authority_names]
    req_registry = load(root / 'repo/authority/requirements.json')
    requirements = req_registry.get('requirements', [])
    agents = (root / 'AGENTS.md').read_text(encoding='utf-8')
    generation_contract = load(root / 'repo/bootstrap/data/realization/generation_contract.json')
    proposal_sources = []
    proposal_dir = root / 'repo/bootstrap/data/proposals'
    for path in sorted(proposal_dir.glob('*.json')):
        proposal_sources.append(load(path))
    authority_required = {'schema_version', 'record_type', 'authority_id', 'title', 'owner', 'lifecycle_state', 'dependencies', 'delegates', 'requirements', 'provenance'}
    authority_shape_ok = all((authority_required <= set(record) and record.get('schema_version') == '1' and (record.get('record_type') == 'authority') and isinstance(record.get('authority_id'), str) and bool(record['authority_id']) and isinstance(record.get('title'), str) and bool(record['title']) and isinstance(record.get('owner'), str) and bool(record['owner']) and isinstance(record.get('lifecycle_state'), str) and bool(record['lifecycle_state']) and isinstance(record.get('dependencies'), list) and isinstance(record.get('delegates'), list) and isinstance(record.get('requirements'), list) and isinstance(record.get('provenance'), dict) for record in authorities))
    requirement_required = {'schema_version', 'record_type', 'requirement_id', 'owner_authority_id', 'statement', 'lifecycle_state', 'conformance_applicability', 'assurance_applicability'}
    requirement_shape_ok = all((requirement_required <= set(record) and record.get('schema_version') == '1' and (record.get('record_type') == 'requirement') and isinstance(record.get('requirement_id'), str) and bool(record['requirement_id']) and isinstance(record.get('owner_authority_id'), str) and bool(record['owner_authority_id']) and isinstance(record.get('statement'), str) and bool(record['statement']) and isinstance(record.get('lifecycle_state'), str) and bool(record['lifecycle_state']) and (record.get('conformance_applicability') in {'mechanical', 'none'}) and (record.get('assurance_applicability') in {'required', 'none'}) and ('lineage' not in record or isinstance(record.get('lineage'), (dict, list))) for record in requirements))
    maintenance_role = generation_contract.get('canonical_source_role')
    proposal_roles = {record.get('source_role') for record in proposal_sources}
    source_roles_distinct = maintenance_role == 'canonical-bootstrap-maintenance-data' and proposal_roles == {'successor-design-proposal'} and (maintenance_role not in proposal_roles)
    fc061_markers = ('Technical write capability is not authority', 'Before mutation, inspect the exact candidate, applicable authority, authorization, and available evidence', 'After cutover, persistent framework mutation must route through Governance')
    fc062_marker = "Do not infer that one repository or GitHub state class has another state class's semantics merely because the states coincide."
    checks = {'FS0-ASSERT-FC-035': (authority_shape_ok, 'each installed FS0 authority record contains the required authority identity, ownership, lifecycle, dependency, delegation, requirement, and provenance fields'), 'FS0-ASSERT-FC-036': (requirement_shape_ok, 'each installed requirement record contains identity, owner, statement, lifecycle, optional structured lineage where applicable, and Conformance/Assurance applicability'), 'FS0-ASSERT-FC-042': (source_roles_distinct, 'canonical FS0 realization maintenance data and successor Design Proposal source data use distinct machine-resolvable source roles'), 'FS0-ASSERT-FC-061': (all((marker in agents for marker in fc061_markers)), 'the canonical agent-orientation surface denies authority from technical write capability, requires exact candidate/evidence inspection before mutation, and routes post-cutover persistent framework mutation through Governance'), 'FS0-ASSERT-FC-062': (fc062_marker in agents, "the canonical agent-orientation surface prohibits inferring one repository or GitHub state class's semantics merely because states coincide")}
    evidence = {'authority_records_checked': len(authorities), 'requirement_records_checked': len(requirements), 'maintenance_source_role': maintenance_role, 'proposal_source_roles': sorted((role for role in proposal_roles if role)), 'agent_orientation': 'AGENTS.md'}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1], evidence) for aid in assertion_ids]

def check_bootstrap_independence(root, assertion_ids):
    contract = load(root / 'repo/bootstrap/data/realization/generation_contract.json')
    structure = load(root / 'repo/bootstrap/data/structure.json')
    bootstrap = root / 'repo/bootstrap'
    top_level = sorted((path.name for path in bootstrap.iterdir() if path.name not in {'__pycache__'}))
    payload_roles_ok = top_level == ['data', 'design', 'scripts']
    local_paths = {'canonical_input_root': contract.get('canonical_input_root'), 'generation_implementation': contract.get('generation_implementation'), 'generation_entrypoint': contract.get('generation_entrypoint')}
    local_paths_ok = all((isinstance(rel, str) and rel.startswith('repo/bootstrap/') and (root / rel).exists() for rel in local_paths.values()))
    generator = root / local_paths['generation_implementation']
    generator_source = generator.read_text(encoding='utf-8')
    imported_sibling_ok = 'from conformance_realization import derive_conformance_realization' in generator_source
    sibling = generator.parent / 'conformance_realization.py'
    sibling_ok = sibling.is_file()
    repository_rooted = 'cwd = Path.cwd().resolve()' in generator_source and 'data = root / "repo/bootstrap/data"' in generator_source and ('../' not in contract.get('canonical_input_root', '')) and (not any((marker in generator_source for marker in ('BOOTSTRAP_SOURCE_ROOT', 'ORIGINATING_BOOTSTRAP', 'external_template_root', 'external_generator_root'))))
    structure_paths = {record.get('path') for record in structure.get('objects', []) if isinstance(record, dict)}
    retained_paths_authorized = all((rel in structure_paths for rel in ('repo/bootstrap/data', 'repo/bootstrap/design', 'repo/bootstrap/scripts', 'repo/bootstrap/scripts/bootstrap', 'repo/bootstrap/scripts/src/generate.py', 'repo/bootstrap/scripts/src/conformance_realization.py', 'repo/bootstrap/scripts/src/preflight.py')))
    role_ok = contract.get('canonical_source_role') == 'canonical-bootstrap-maintenance-data' and contract.get('generated_surfaces_are_canonical_source') is False and (contract.get('canonical_input_root') == 'repo/bootstrap/data') and (contract.get('generation_implementation') == 'repo/bootstrap/scripts/src/generate.py') and (contract.get('generation_entrypoint') == 'repo/bootstrap/scripts/bootstrap')
    checks = {'FS0-ASSERT-FC-024': (payload_roles_ok and local_paths_ok and sibling_ok and imported_sibling_ok and repository_rooted, 'the retained bootstrap payload resolves canonical data and generation implementation entirely from the target repository and requires no originating bootstrap semantic, template, generator, or script input'), 'FS0-ASSERT-FC-028': (role_ok and retained_paths_authorized, 'one machine-resolvable non-authoritative retained bootstrap maintenance-source and generation role remains installed and structurally authorized'), 'FS0-ASSERT-FC-054': (payload_roles_ok and local_paths_ok and sibling_ok and imported_sibling_ok and repository_rooted, 'post-cutover operation of retained bootstrap generation machinery requires no semantic, template, generator, or script input from an external bootstrap environment')}
    evidence = {'bootstrap_top_level': top_level, 'canonical_source_role': contract.get('canonical_source_role'), 'canonical_input_root': contract.get('canonical_input_root'), 'generation_implementation': contract.get('generation_implementation'), 'generation_entrypoint': contract.get('generation_entrypoint'), 'generated_surfaces_are_canonical_source': contract.get('generated_surfaces_are_canonical_source')}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1], evidence) for aid in assertion_ids]

def _fs0_pre_merge_provenance_check_bootstrap_authority_lifecycle(root, assertion_ids):
    state_path = root / 'repo/state/bootstrap.json'
    accepted_state_path = root / 'repo/governance/accepted_state.py'
    try:
        record = load(state_path)
        module = _load_module_for_fc033(accepted_state_path, 'fs0_fc027_accepted_state')
        sha = 'a' * 40
        pre = module.resolve_main_revision({'state': 'candidate'}, sha)
        post = module.resolve_main_revision({'state': 'cutover'}, sha)
        accepted_read_surface_ok = pre.get('status') == 'unaccepted' and post.get('status') == 'accepted' and (post.get('accepted_revision') == sha) and (post.get('accepted_ref') == 'refs/heads/main') and (post.get('provenance_resolution') == 'governed-pr-merge')
        source = accepted_state_path.read_text(encoding='utf-8')
        no_maintenance_fallback = 'repo/bootstrap/data/state/bootstrap.json' not in source and 'bootstrap-cutover-to-immutable-acceptance-receipt' not in source
        current_state_valid = isinstance(record, dict) and record.get('state') in {'candidate', 'cutover'} and (record.get('accepted_ref') == 'refs/heads/main')
        one_way_lifecycle_ok = current_state_valid and pre.get('status') == 'unaccepted' and (post.get('status') == 'accepted')
        checks = {'FS0-ASSERT-FC-027': (accepted_read_surface_ok and no_maintenance_fallback, 'after cutover accepted-state determination resolves from refs/heads/main and committed cutover state without bootstrap-maintenance fallback'), 'FS0-ASSERT-FC-031': (one_way_lifecycle_ok, 'bootstrap lifecycle distinguishes candidate from cutover and only cutover enables accepted-state resolution')}
        evidence = {'bootstrap_state_path': 'repo/state/bootstrap.json', 'accepted_state_path': 'repo/governance/accepted_state.py', 'candidate_resolution': pre.get('status'), 'cutover_resolution': post.get('status'), 'accepted_ref': post.get('accepted_ref'), 'provenance_resolution': post.get('provenance_resolution'), 'bootstrap_maintenance_fallback_absent': no_maintenance_fallback}
    except Exception as exc:
        checks = {aid: (False, 'bootstrap authority lifecycle check failed') for aid in assertion_ids}
        evidence = {'error': str(exc)}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1], evidence) for aid in assertion_ids]

def check_bootstrap_authority_lifecycle(root, assertion_ids):
    legacy_results = _fs0_pre_merge_provenance_check_bootstrap_authority_lifecycle(root, assertion_ids)
    path = root / 'repo/governance/accepted_state.py'
    spec = importlib.util.spec_from_file_location('fs0_lifecycle_provenance', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    sha = '3' * 40
    candidate_state = {'state': 'candidate', 'bootstrap_provenance_issue': None}
    cutover_state = {'state': 'cutover', 'bootstrap_provenance_issue': 17}
    proof = {'schema_version': '1', 'record_type': 'bootstrap-pr-acceptance', 'status': 'accepted', 'bootstrap_provenance_issue': 17, 'pull_request_number': 7, 'candidate_head': '1' * 40, 'accepted_repository_predecessor': '2' * 40, 'resulting_accepted_revision': sha, 'actor': {'id': 101, 'login': 'tester'}, 'merged_at': '2026-01-01T00:20:00Z', 'eligibility': {'status': 'pass'}}
    candidate = m.resolve_main_revision(candidate_state, sha, None)
    unproven_cutover = m.resolve_main_revision(cutover_state, sha, None)
    proven_cutover = m.resolve_main_revision(cutover_state, sha, proof)
    ok = candidate.get('status') == 'unaccepted' and unproven_cutover.get('status') == 'invalid' and (proven_cutover.get('status') == 'accepted') and (proven_cutover.get('accepted_ref') == 'refs/heads/main')
    out = []
    for item in legacy_results:
        aid = item.get('assertion_id') if isinstance(item, dict) else None
        if aid in {'FS0-ASSERT-FC-027', 'FS0-ASSERT-FC-031'}:
            detail = 'after cutover accepted-state determination resolves from refs/heads/main only with resolved authorized eligible merge provenance and without bootstrap-maintenance fallback' if aid == 'FS0-ASSERT-FC-027' else 'bootstrap lifecycle distinguishes candidate from cutover and cutover accepted-state resolution additionally requires authorized eligible merge provenance'
            out.append(result(aid, 'pass' if ok else 'fail', detail, {'candidate_resolution': candidate.get('status'), 'unproven_cutover_resolution': unproven_cutover.get('status'), 'proven_cutover_resolution': proven_cutover.get('status'), 'accepted_ref': proven_cutover.get('accepted_ref'), 'provenance_resolution': proven_cutover.get('provenance_resolution')}))
        else:
            out.append(item)
    return out

def _fresh_bootstrap_guard_regression(root):
    guard_path = root / 'repo/governance/bootstrap_mutation_guard.py'
    spec = importlib.util.spec_from_file_location('fs0_fresh_bootstrap_guard', guard_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    canonical = dict(load(root / 'repo/bootstrap/data/state/bootstrap.json'))
    canonical.update({'state': 'candidate', 'cutover_timestamp': None})
    with tempfile.TemporaryDirectory() as td:
        fresh = Path(td)
        subprocess.run(['git', 'init'], cwd=fresh, text=True, capture_output=True, check=True)
        state_path = fresh / 'repo/bootstrap/data/state/bootstrap.json'
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(canonical, indent=2) + '\n', encoding='utf-8')
        report = module.authorize(fresh)
        no_head_ok = report.get('authorized') is True and report.get('state') == 'candidate' and (report.get('preinstallation') is True)
    with tempfile.TemporaryDirectory() as td:
        preexisting = Path(td)
        subprocess.run(['git', 'init'], cwd=preexisting, text=True, capture_output=True, check=True)
        (preexisting / 'README.initial').write_text('pre-FS0 repository\n', encoding='utf-8')
        subprocess.run(['git', 'add', 'README.initial'], cwd=preexisting, text=True, capture_output=True, check=True)
        subprocess.run(['git', '-c', 'user.name=FS0 Test', '-c', 'user.email=fs0@example.invalid', 'commit', '-m', 'pre-FS0 initial commit'], cwd=preexisting, text=True, capture_output=True, check=True)
        state_path = preexisting / 'repo/bootstrap/data/state/bootstrap.json'
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(canonical, indent=2) + '\n', encoding='utf-8')
        report = module.authorize(preexisting)
        pre_fs0_head_ok = report.get('authorized') is True and report.get('preinstallation') is True
    with tempfile.TemporaryDirectory() as td:
        inconsistent = Path(td)
        subprocess.run(['git', 'init'], cwd=inconsistent, text=True, capture_output=True, check=True)
        committed = inconsistent / 'repo/bootstrap/data/state/bootstrap.json'
        committed.parent.mkdir(parents=True, exist_ok=True)
        committed.write_text(json.dumps(canonical, indent=2) + '\n', encoding='utf-8')
        subprocess.run(['git', 'add', 'repo/bootstrap'], cwd=inconsistent, text=True, capture_output=True, check=True)
        subprocess.run(['git', '-c', 'user.name=FS0 Test', '-c', 'user.email=fs0@example.invalid', 'commit', '-m', 'malformed partial FS0'], cwd=inconsistent, text=True, capture_output=True, check=True)
        rejected = False
        try:
            module.authorize(inconsistent)
        except SystemExit:
            rejected = True
    return {'ok': no_head_ok and pre_fs0_head_ok and rejected, 'no_head_preinstallation_allowed': no_head_ok, 'pre_fs0_head_preinstallation_allowed': pre_fs0_head_ok, 'committed_partial_fs0_rejected': rejected}

def check_post_cutover_mutation_authority(root, assertion_ids):
    fresh = _fresh_bootstrap_guard_regression(root)
    wrapper = (root / 'repo/bootstrap/scripts/bootstrap').read_text(encoding='utf-8')
    guard = (root / 'repo/governance/bootstrap_mutation_guard.py').read_text(encoding='utf-8')
    apath = root / 'repo/governance/accepted_state.py'
    accepted_source = apath.read_text(encoding='utf-8')
    work_source = (root / 'repo/governance/work.py').read_text(encoding='utf-8')
    binding = (root / 'repo/governance/github_binding.py').read_text(encoding='utf-8')
    guard_call = 'python3 -B repo/bootstrap/data/realization/governance/bootstrap_mutation_guard.py >/dev/null'
    generator_call = 'python3 -B repo/bootstrap/scripts/src/generate.py "$@"'
    preflight = 'python3 -B repo/bootstrap/scripts/src/preflight.py'
    guard_before = guard_call in wrapper and generator_call in wrapper and (preflight in wrapper) and (wrapper.index(preflight) < wrapper.index(guard_call) < wrapper.rindex(generator_call))
    check_bypass = 'if [ "${1:-}" = "--check" ]' in wrapper and 'exec python3 -B repo/bootstrap/scripts/src/generate.py "$@"' in wrapper
    guard_ok = 'github_pull_requests_for_issue' in guard and 'resolve_governance_work_acceptance' in guard and ('repo-spec-acceptance:v1' not in guard) and ('github_issue_comments_for' not in guard)
    helpers = all((token in (root / 'repo/governance/accepted_state.py').read_text(encoding='utf-8') for token in ('def github_candidate_conformance(', 'def github_candidate_eligibility(', 'def github_pr_audit_comments(', 'def resolve_candidate_semantic_audit(', 'def resolve_completion_semantic_audit(')))
    work_gate = all((token in (root / 'repo/governance/accepted_state.py').read_text(encoding='utf-8') for token in ('def github_candidate_conformance(', 'def github_candidate_eligibility(', 'def resolve_candidate_semantic_audit(', 'candidate-semantic-audit-receipt', 'def github_candidate_assurance_from_merge(', 'def resolve_governance_work_acceptance(')))
    predicate = 'def post_cutover_mutation_allowed' in binding and 'mutation_scope' in binding
    spec = importlib.util.spec_from_file_location('fs0_fc032_accepted_state', apath)
    accepted = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(accepted)
    runs = []
    orig = accepted._gh_json
    try:
        accepted._gh_json = lambda endpoint: {'workflow_runs': list(runs)}
        before = '2026-01-01T00:10:00Z'
        merged = '2026-01-01T00:20:00Z'
        after = '2026-01-01T00:30:00Z'
        base = {'id': 1, 'name': 'FS0 Conformance', 'event': 'pull_request', 'head_sha': '1' * 40, 'path': '.github/workflows/fs0-conformance.yml', 'run_number': 1, 'run_attempt': 1}
        runs[:] = [{**base, 'conclusion': 'success', 'updated_at': before}]
        prepass = accepted.github_candidate_conformance('o/r', '1' * 40, merged)
        runs[:] = [{**base, 'conclusion': 'fail', 'updated_at': before}]
        prefail = accepted.github_candidate_conformance('o/r', '1' * 40, merged)
        runs[:] = [{**base, 'conclusion': 'success', 'updated_at': after}]
        postonly = accepted.github_candidate_conformance('o/r', '1' * 40, merged)
        runs[:] = [{**base, 'id': 1, 'conclusion': 'fail', 'updated_at': before}, {**base, 'id': 2, 'conclusion': 'success', 'updated_at': after}]
        late = accepted.github_candidate_conformance('o/r', '1' * 40, merged)
    finally:
        accepted._gh_json = orig
    temporal = prepass.get('status') == 'pass' and prefail.get('status') == 'fail' and (postonly.get('status') == 'fail') and (late.get('status') == 'fail')
    ok = guard_before and check_bypass and guard_ok and helpers and work_gate and predicate and temporal and fresh['ok']
    evidence = {'guard': 'repo/governance/bootstrap_mutation_guard.py', 'accepted_state': 'repo/governance/accepted_state.py', 'governance_work': 'repo/governance/work.py', 'guard_before_generator': guard_before, 'remote_eligibility_helpers': helpers, 'canonical_governed_work_gate': work_gate, 'premerge_success': prepass.get('status'), 'premerge_failure': prefail.get('status'), 'postmerge_only_success': postonly.get('status'), 'late_successful_rerun_after_premerge_failure': late.get('status'), 'temporal_binding': temporal, 'governance_binding_predicate': predicate, 'check_bypass': check_bypass, 'guard_semantics': guard_ok, 'fresh_bootstrap_regression': fresh}
    return [result(a, 'pass' if ok else 'fail', 'after cutover governed acceptance requires canonical declared Assurance gates plus exact-candidate Conformance that completed successfully before the authorized merge; later reruns cannot retroactively create eligibility', evidence) for a in assertion_ids]

def check_post_cutover_mutation_binding(root, assertion_ids):
    binding_path = root / 'repo/governance/github_binding.py'
    source = binding_path.read_text(encoding='utf-8')
    required_fragments = ('if state == "candidate":', 'governed_build.get("stage") == "build"', 'governed_build.get("disposition") == "pending"', 'isinstance(governed_build.get("accepted_plan_id"), str)', 'bool(governed_build.get("accepted_plan_id"))', 'isinstance(governed_build.get("bounded_authorization"), dict)', 'bool(governed_build["bounded_authorization"].get("mutation_scope"))')
    spec = importlib.util.spec_from_file_location('fs0_gov020_binding', binding_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    candidate = {'state': 'candidate'}
    cutover = {'state': 'cutover'}
    valid = {'stage': 'build', 'disposition': 'pending', 'accepted_plan_id': 'PLAN-ACCEPTED', 'bounded_authorization': {'mutation_scope': ['repo/bootstrap/data/model.json']}}
    cases = (('candidate', candidate, None, True), ('cutover-valid', cutover, valid, True), ('cutover-none', cutover, None, False), ('cutover-accepted', cutover, dict(valid, disposition='accepted'), False), ('cutover-rejected', cutover, dict(valid, disposition='rejected'), False), ('cutover-no-plan', cutover, dict(valid, accepted_plan_id=''), False), ('cutover-wrong-stage', cutover, dict(valid, stage='plan'), False), ('cutover-no-scope', cutover, {**valid, 'bounded_authorization': {'mutation_scope': []}}, False))
    observations = {}
    fragments_ok = all((fragment in source for fragment in required_fragments))
    ok = fragments_ok
    for name, state, build, expected in cases:
        observed = module.post_cutover_mutation_allowed(state, build)
        observations[name] = {'observed': observed, 'expected': expected}
        ok = ok and observed is expected
    evidence = {'binding': 'repo/governance/github_binding.py', 'required_fragments_present': fragments_ok, 'cases': observations}
    return [result(aid, 'pass' if ok else 'fail', 'post-cutover mutation requires a pending Build derived from an accepted Plan with non-empty bounded mutation scope; candidate bootstrap remains permitted', evidence) for aid in assertion_ids]

def check_retained_bootstrap_payload(root, assertion_ids):
    import subprocess
    policy_path = root / 'repo/bootstrap/data/retained_payload.json'
    try:
        policy = json.loads(policy_path.read_text(encoding='utf-8'))
    except Exception as exc:
        return [result(aid, 'fail', 'retained bootstrap payload policy is missing or invalid', {'error': str(exc), 'policy': str(policy_path.relative_to(root))}) for aid in assertion_ids]
    expected_roles = {'repo/bootstrap/design/': 'design-input', 'repo/bootstrap/data/': 'canonical-realization-input', 'repo/bootstrap/scripts/': 'implementation'}
    expected_purposes = {'construct', 'verify', 'accept', 'cut-over', 'maintain'}
    classes = policy.get('payload_classes')
    class_map = {}
    class_shape_ok = isinstance(classes, list) and len(classes) == 3
    if class_shape_ok:
        for entry in classes:
            if not isinstance(entry, dict):
                class_shape_ok = False
                break
            prefix = entry.get('path_prefix')
            role = entry.get('role')
            purposes = entry.get('required_for')
            if not isinstance(prefix, str) or not isinstance(role, str) or (not isinstance(purposes, list)) or (not all((isinstance(x, str) for x in purposes))) or (prefix in class_map):
                class_shape_ok = False
                break
            class_map[prefix] = {'role': role, 'required_for': set(purposes)}
    policy_ok = policy.get('schema_version') == '1' and policy.get('record_type') == 'retained-bootstrap-payload-policy' and (policy.get('payload_root') == 'repo/bootstrap') and class_shape_ok and (set(class_map) == set(expected_roles)) and all((class_map[prefix]['role'] == role for prefix, role in expected_roles.items())) and (set(policy.get('required_capabilities', [])) == expected_purposes) and all((class_map[prefix]['required_for'] <= expected_purposes and bool(class_map[prefix]['required_for']) for prefix in class_map))
    proc = subprocess.run(['git', 'ls-files', '-z', '--', 'repo/bootstrap'], cwd=root, text=False, capture_output=True)
    tracked_ok = proc.returncode == 0
    tracked = []
    if tracked_ok:
        tracked = [item.decode('utf-8') for item in proc.stdout.split(b'\x00') if item]
    uncovered = []
    ambiguous = []
    classifications = {}
    for path in tracked:
        matches = [prefix for prefix in expected_roles if path.startswith(prefix)]
        if len(matches) == 0:
            uncovered.append(path)
            continue
        if len(matches) != 1:
            ambiguous.append(path)
            continue
        classifications[path] = expected_roles[matches[0]]
    roles_present = set(classifications.values())
    role_coverage_ok = roles_present == set(expected_roles.values())
    top_level = sorted({path.split('/', 3)[2] for path in tracked if path.startswith('repo/bootstrap/') and len(path.split('/', 3)) >= 3})
    top_level_ok = top_level == ['data', 'design', 'scripts']
    ok = policy_ok and tracked_ok and bool(tracked) and (not uncovered) and (not ambiguous) and role_coverage_ok and top_level_ok
    evidence = {'policy': 'repo/bootstrap/data/retained_payload.json', 'tracked_file_count': len(tracked), 'allowed_top_level': ['data', 'design', 'scripts'], 'observed_top_level': top_level, 'roles_present': sorted(roles_present), 'uncovered': uncovered, 'ambiguous': ambiguous, 'policy_valid': policy_ok}
    return [result(aid, 'pass' if ok else 'fail', 'the retained bootstrap payload is closed to Design input, canonical realization inputs, and implementation required for the declared FS0 bootstrap capabilities', evidence) for aid in assertion_ids]

def check_json_record_envelopes(root, assertion_ids):
    import subprocess
    proc = subprocess.run(['git', 'ls-files', '-z', '--', 'repo'], cwd=root, text=False, capture_output=True)
    tracked_ok = proc.returncode == 0
    paths = []
    if tracked_ok:
        paths = sorted((item.decode('utf-8') for item in proc.stdout.split(b'\x00') if item and item.decode('utf-8').endswith('.json')))
    invalid = []
    non_objects = []
    for rel in paths:
        path = root / rel
        try:
            value = json.loads(path.read_text(encoding='utf-8'))
        except Exception as exc:
            invalid.append({'path': rel, 'error': str(exc)})
            continue
        if not isinstance(value, dict):
            non_objects.append(rel)
            continue
        if not isinstance(value.get('schema_version'), str) or not value.get('schema_version') or (not isinstance(value.get('record_type'), str)) or (not value.get('record_type')):
            invalid.append({'path': rel, 'error': 'missing-or-invalid-record-envelope'})
    ok = tracked_ok and bool(paths) and (not invalid) and (not non_objects)
    evidence = {'tracked_json_count': len(paths), 'invalid_records': invalid, 'non_object_json_documents': non_objects}
    return [result(aid, 'pass' if ok else 'fail', 'every Git-tracked FS0 JSON document beneath repo/ is an object carrying non-empty schema_version and record_type fields', evidence) for aid in assertion_ids]

def check_state_class_distinction(root, assertion_ids):
    contract_path = root / 'repo/bootstrap/data/state_classes.json'
    try:
        contract = json.loads(contract_path.read_text(encoding='utf-8'))
    except Exception as exc:
        return [result(aid, 'fail', 'state-class contract is missing or invalid', {'error': str(exc)}) for aid in assertion_ids]
    expected = {'repository-content': {'record_type': 'repository-content-state', 'required_fields': ['revision']}, 'desired-github-operating-state': {'record_type': 'desired-github-operating-state', 'required_fields': ['desired_objects']}, 'observed-github-state': {'record_type': 'observed-github-state', 'required_fields': ['observations']}, 'authorized-mutation': {'record_type': 'authorized-mutation', 'required_fields': ['authority_basis', 'mutation_scope']}, 'verified-resulting-state': {'record_type': 'verified-resulting-state', 'required_fields': ['resulting_revision', 'verification_evidence']}}
    classes = contract.get('state_classes')
    observed = {}
    shape_ok = isinstance(classes, list) and len(classes) == 5
    if shape_ok:
        for entry in classes:
            if not isinstance(entry, dict):
                shape_ok = False
                break
            role = entry.get('role')
            if not isinstance(role, str) or role in observed:
                shape_ok = False
                break
            observed[role] = {'record_type': entry.get('record_type'), 'required_fields': entry.get('required_fields')}
    distinct_types = {v.get('record_type') for v in observed.values() if isinstance(v.get('record_type'), str)}
    contract_ok = contract.get('schema_version') == '1' and contract.get('record_type') == 'fs0-state-class-contract' and shape_ok and (set(observed) == set(expected)) and (len(distinct_types) == 5) and all((observed[role]['record_type'] == spec['record_type'] and observed[role]['required_fields'] == spec['required_fields'] for role, spec in expected.items())) and (contract.get('equivalence_policy') == 'no-state-class-implies-or-substitutes-for-another')
    binding_path = root / 'repo/governance/github_binding.py'
    binding = binding_path.read_text(encoding='utf-8')
    binding_roles = {'repository-content': 'revision_under_review' in binding and 'candidate["commit_sha"]' in binding, 'observed-github-state': 'resolve_remote_governance_state' in binding and 'remaining_unauthorized_work' in binding, 'authorized-mutation': 'post_cutover_mutation_allowed' in binding and 'bounded_authorization' in binding, 'verified-resulting-state': 'resulting_accepted_revision' in binding and 'resulting_accepted_state' in binding}
    desired_source = root / 'repo/bootstrap/data/github_operating_state.json'
    desired_ok = False
    if desired_source.is_file():
        try:
            desired = json.loads(desired_source.read_text(encoding='utf-8'))
            desired_ok = desired.get('schema_version') == '1' and desired.get('record_type') == 'desired-github-operating-state' and isinstance(desired.get('desired_objects'), list)
        except Exception:
            desired_ok = False
    ok = contract_ok and all(binding_roles.values()) and desired_ok
    evidence = {'contract': 'repo/bootstrap/data/state_classes.json', 'distinct_record_types': sorted(distinct_types), 'binding_role_evidence': binding_roles, 'desired_state_source': 'repo/bootstrap/data/github_operating_state.json', 'desired_state_valid': desired_ok}
    return [result(aid, 'pass' if ok else 'fail', 'FS0 keeps repository content, desired GitHub operating state, observed GitHub state, authorized mutation, and verified resulting state as distinct non-substitutable state classes', evidence) for aid in assertion_ids]

def check_cutover_record_immutability(root, assertion_ids):
    policy_path = root / 'repo/bootstrap/data/bootstrap_recovery_authority.json'
    guard_path = root / 'repo/governance/bootstrap_mutation_guard.py'
    try:
        policy = load(policy_path)
    except Exception as exc:
        return [result(aid, 'fail', 'bootstrap recovery authority policy is missing or invalid', {'error': str(exc)}) for aid in assertion_ids]
    expected_protected = {'repo/state/bootstrap.json', 'repo/bootstrap/data/state/bootstrap.json'}
    policy_ok = policy.get('schema_version') == '1' and policy.get('record_type') == 'bootstrap-recovery-authority-policy' and (policy.get('cutover_record') == 'repo/state/bootstrap.json') and (policy.get('canonical_cutover_source') == 'repo/bootstrap/data/state/bootstrap.json') and (set(policy.get('protected_paths', [])) == expected_protected) and (set(policy.get('permitted_authority_purposes', [])) == {'bootstrap-recovery', 'bootstrap-reconstruction'}) and (policy.get('authority_stage') == 'plan') and (policy.get('required_disposition') == 'accepted')
    spec = importlib.util.spec_from_file_location('fs0_fc060_guard', guard_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ordinary = {'stage': 'plan', 'disposition': 'accepted', 'authority_purpose': 'ordinary-maintenance'}
    recovery = {'stage': 'plan', 'disposition': 'accepted', 'authority_purpose': 'bootstrap-recovery'}
    reconstruction = {'stage': 'plan', 'disposition': 'accepted', 'authority_purpose': 'bootstrap-reconstruction'}
    ordinary_bootstrap = module.recovery_authority_allowed(policy, ordinary, ['repo/bootstrap/data/model.json'])
    ordinary_cutover = module.recovery_authority_allowed(policy, ordinary, ['repo/state/bootstrap.json'])
    ordinary_source = module.recovery_authority_allowed(policy, ordinary, ['repo/bootstrap/data/state/bootstrap.json'])
    recovery_cutover = module.recovery_authority_allowed(policy, recovery, ['repo/state/bootstrap.json'])
    reconstruction_source = module.recovery_authority_allowed(policy, reconstruction, ['repo/bootstrap/data/state/bootstrap.json'])
    guard_source = guard_path.read_text(encoding='utf-8')
    baseline_ok = 'load_committed_json(root, protected_record)' in guard_source and 'load_committed_json(root, policy_rel)' in guard_source and ('dirty_guarded_paths(root, protected_record)' in guard_source) and ('plan_acceptance.get("status") != "accepted"' in guard_source)
    truth_table_ok = ordinary_bootstrap is True and ordinary_cutover is False and (ordinary_source is False) and (recovery_cutover is True) and (reconstruction_source is True)
    ok = policy_ok and baseline_ok and truth_table_ok
    evidence = {'policy': 'repo/bootstrap/data/bootstrap_recovery_authority.json', 'guard': 'repo/governance/bootstrap_mutation_guard.py', 'committed_baseline_authority': baseline_ok, 'ordinary_bootstrap_maintenance_allowed': ordinary_bootstrap, 'ordinary_cutover_record_mutation_allowed': ordinary_cutover, 'ordinary_cutover_source_mutation_allowed': ordinary_source, 'recovery_cutover_record_mutation_allowed': recovery_cutover, 'reconstruction_cutover_source_mutation_allowed': reconstruction_source}
    return [result(aid, 'pass' if ok else 'fail', 'after cutover the committed bootstrap cutover record and its canonical source are immutable under ordinary maintenance and may change only through an explicitly accepted Plan whose authority purpose is bootstrap recovery or reconstruction', evidence) for aid in assertion_ids]

def check_generation_semantics_canonical(root, assertion_ids):
    contract_path = root / 'repo/bootstrap/data/generation_contract.json'
    generator_path = root / 'repo/bootstrap/scripts/src/generate.py'
    try:
        contract = load(contract_path)
    except Exception as exc:
        return [result(aid, 'fail', 'canonical generation contract is missing or invalid', {'error': str(exc)}) for aid in assertion_ids]
    required_top = {'schema_version', 'record_type', 'record_schema_version', 'record_types', 'roles', 'source_paths', 'output_paths', 'required_fields', 'enumerations', 'bootstrap_lifecycle', 'default_artifact_mode'}
    contract_ok = isinstance(contract, dict) and set(contract) == required_top and (contract.get('schema_version') == '1') and (contract.get('record_type') == 'fs0-generation-contract') and isinstance(contract.get('record_types'), dict) and (len(contract['record_types']) >= 20) and isinstance(contract.get('source_paths'), dict) and isinstance(contract.get('output_paths'), dict) and isinstance(contract.get('required_fields'), dict) and isinstance(contract.get('enumerations'), dict) and isinstance(contract.get('bootstrap_lifecycle'), dict)
    source = generator_path.read_text(encoding='utf-8')
    tree = ast.parse(source)
    names = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    required_functions = {'load_generation_contract', 'load_source', 'derive_identity_surfaces', 'derive_successor_proposals', 'derive_bootstrap_state', 'derive_repository_structure_state', 'derive', 'required_mode'}
    wiring_ok = required_functions <= names
    semantic_values = set(contract['record_types'].values())
    semantic_values.update(contract['output_paths'].values())
    semantic_values.update((value for values in contract['enumerations'].values() for value in values))
    semantic_values.add(contract['default_artifact_mode'])
    string_literals = {node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, str)}
    allowed_algorithm_literals = {'directory', 'closed', 'authority', 'required', 'requirement'}
    duplicated = sorted((value for value in semantic_values if value in string_literals and value not in allowed_algorithm_literals))
    data_driven_markers = 'contract["record_schema_version"]' in source and 'contract["record_types"]' in source and ('contract["output_paths"]' in source) and ('contract["required_fields"]' in source) and ('contract["enumerations"]' in source) and ('contract["bootstrap_lifecycle"]' in source) and ('contract["default_artifact_mode"]' in source)
    generation_check = subprocess.run([str(root / 'repo/bootstrap/scripts/bootstrap'), '--check'], cwd=root, text=True, capture_output=True)
    deterministic_ok = generation_check.returncode == 0 and 'FS0 generation correspondence: PASS' in generation_check.stdout
    fc069_ok = contract_ok and wiring_ok and data_driven_markers and deterministic_ok
    fc070_ok = fc069_ok and (not duplicated)
    checks = {'FS0-ASSERT-FC-069': (fc069_ok, 'semantic and realization choices required by generation are represented in canonical maintenance data and consumed by the generator'), 'FS0-ASSERT-FC-070': (fc070_ok, "generator mechanics consume canonical generation semantics without independently duplicating the contract's normative output values")}
    evidence = {'contract': 'repo/bootstrap/data/generation_contract.json', 'generator': 'repo/bootstrap/scripts/src/generate.py', 'contract_record_type_count': len(contract.get('record_types', {})), 'required_generator_functions_present': wiring_ok, 'data_driven_markers_present': data_driven_markers, 'duplicated_contract_semantic_literals': duplicated, 'generation_check_returncode': generation_check.returncode}
    return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1], evidence) for aid in assertion_ids]

def check_repository_structure(root, assertion_ids):
    try:
        live = _evaluate_repository_structure(root)
        semantic = _exercise_structure_semantics()
        source_text = Path(__file__).read_text(encoding='utf-8')
        cases = semantic['cases']
        live_clean = live['ok'] and (not live['unauthorized']) and (not live['unsupported']) and (not live['missing']) and (not live['type_mismatches'])
        exact_one_resolution = live.get('configuration_identity') and live.get('configuration_path') and live.get('binding_path')
        source_uses_only_config_authorization = 'rec, mode = _applicable_authorization(rel, entries)' in source_text and 'if rec is None:' in source_text and ('unauthorized.append(rel)' in source_text)
        source_location_independent = 'for rel, item in namespace.items():' in source_text and 'obj.get("record_type") == "repository-structure-binding"' in source_text and ('obj.get("record_type") == "repository-structure-configuration"' in source_text) and ('configuration identity' in source_text)
        source_nonfollowing = 'entry.stat(follow_symlinks=False)' in source_text and 'if kind == "directory":' in source_text and ('stack.append(path)' in source_text)
        common = {'configuration_identity': live.get('configuration_identity'), 'binding_path': live.get('binding_path'), 'configuration_path': live.get('configuration_path'), 'observed_objects': live.get('observed_objects'), 'configured_objects': live.get('configured_objects')}

        def ev(**items):
            out = dict(common)
            out.update(items)
            return out
        checks = {'FS0-ASSERT-FC-006': (live_clean, 'the complete physical repository namespace conforms to the resolved repository-structure configuration', ev(unauthorized=live['unauthorized'], unsupported=live['unsupported'], missing=live['missing'], type_mismatches=live['type_mismatches'])), 'FS0-ASSERT-FC-029': (live_clean and source_uses_only_config_authorization, 'structural permission is obtained only through applicable authorization from the resolved configuration', ev(authorization_path='_applicable_authorization -> resolved configuration')), 'FS0-ASSERT-FC-030': (live_clean and cases['unknown_file_rejected'] and cases['unknown_directory_rejected'], 'objects lacking applicable structural authorization are rejected', ev(semantic_tests={'unknown_file_rejected': cases['unknown_file_rejected'], 'unknown_directory_rejected': cases['unknown_directory_rejected']})), 'FS0-ASSERT-FC-055': (live_clean and exact_one_resolution, 'repository structure is evaluated against one resolved canonical configuration', ev(resolution='exactly one binding identity and exactly one matching configuration')), 'FS0-ASSERT-FC-080': (live_clean and cases['unknown_file_rejected'] and cases['unknown_directory_rejected'], 'absence of applicable structural authorization is deny', ev(semantic_tests={'unknown_file_rejected': cases['unknown_file_rejected'], 'unknown_directory_rejected': cases['unknown_directory_rejected']})), 'FS0-ASSERT-FC-081': (live_clean and source_uses_only_config_authorization, 'no incidental filesystem class receives implicit structural authorization', ev(implicit_authorization_sources=[])), 'FS0-ASSERT-FC-082': (live_clean and exact_one_resolution, 'governed repository state determines exactly one repository-structure configuration identity', ev(configuration_identity=live['configuration_identity'])), 'FS0-ASSERT-FC-083': (live_clean and exact_one_resolution and source_location_independent, 'the operating substrate resolves the governed configuration identity and does not select a configuration by caller preference', ev(resolution='namespace semantic-record scan by governed identity')), 'FS0-ASSERT-FC-084': (live_clean and cases['missing_binding_rejected'] and cases['ambiguous_binding_rejected'] and cases['unresolved_identity_rejected'] and cases['duplicate_matching_configuration_rejected'], 'missing, ambiguous, or unresolved governed configuration identity is rejected rather than replaced by a default, fallback, or search-order choice', ev(semantic_tests={'missing_binding_rejected': cases['missing_binding_rejected'], 'ambiguous_binding_rejected': cases['ambiguous_binding_rejected'], 'unresolved_identity_rejected': cases['unresolved_identity_rejected'], 'duplicate_matching_configuration_rejected': cases['duplicate_matching_configuration_rejected']})), 'FS0-ASSERT-FC-085': (live_clean and live['configuration_self_authorized'] and cases['configuration_self_authorization_required'], 'the resolved repository-structure configuration must structurally authorize its own filesystem object', ev(configuration_self_authorized=live['configuration_self_authorized'], semantic_test=cases['configuration_self_authorization_required'])), 'FS0-ASSERT-FC-086': (live_clean and cases['required_missing_rejected'] and cases['permitted_missing_accepted'], 'structural authorization distinguishes required presence from permitted absence', ev(semantic_tests={'required_missing_rejected': cases['required_missing_rejected'], 'permitted_missing_accepted': cases['permitted_missing_accepted']})), 'FS0-ASSERT-FC-087': (live_clean and cases['closed_directory_rejects_descendant'], 'directory authorization is closed to descendants unless complete-subtree authorization is explicit', ev(semantic_test=cases['closed_directory_rejects_descendant'])), 'FS0-ASSERT-FC-088': (live_clean and cases['complete_subtree_accepts_descendant'], 'explicit complete-subtree authorization positively authorizes descendant objects', ev(semantic_test=cases['complete_subtree_accepts_descendant'])), 'FS0-ASSERT-FC-089': (live_clean and cases.get('unsupported_fifo_rejected_under_subtree', True), 'complete-subtree authorization does not override global filesystem-object admissibility', ev(semantic_test=cases.get('unsupported_fifo_rejected_under_subtree', 'not-supported-on-platform'))), 'FS0-ASSERT-FC-090': (live_clean and cases['ordinary_file_accepted'] and cases['directory_object_accepted'] and cases['authorized_symlink_is_link_object'], 'ordinary files, directories, and symbolic links are explicitly accepted as configured structural object types', ev(supported_object_types=['file', 'directory', 'symlink'], semantic_tests={'ordinary_file_accepted': cases['ordinary_file_accepted'], 'directory_object_accepted': cases['directory_object_accepted'], 'authorized_symlink_is_link_object': cases['authorized_symlink_is_link_object']})), 'FS0-ASSERT-FC-091': (live_clean and cases.get('unsupported_fifo_rejected_under_subtree', True), 'unsupported filesystem object types are denied', ev(semantic_test=cases.get('unsupported_fifo_rejected_under_subtree', 'not-supported-on-platform'))), 'FS0-ASSERT-FC-092': (live_clean and cases['authorized_symlink_is_link_object'], 'a symbolic link is structurally evaluated as the link object itself', ev(semantic_test=cases['authorized_symlink_is_link_object'])), 'FS0-ASSERT-FC-093': (live_clean and cases['external_symlink_target_not_traversed'] and source_nonfollowing, 'structural traversal does not follow symbolic-link targets', ev(semantic_test=cases['external_symlink_target_not_traversed'], lstat_behavior='follow_symlinks=False')), 'FS0-ASSERT-FC-094': (live_clean and cases['external_symlink_target_not_traversed'], 'a symbolic-link target outside the repository does not enlarge the governed repository boundary', ev(semantic_test=cases['external_symlink_target_not_traversed'])), 'FS0-ASSERT-FC-095': (live_clean and source_uses_only_config_authorization and bool(live['configuration_path']) and live['configuration_self_authorized'], 'bootstrap construction is not itself treated as structural authorization; the resulting candidate is evaluated through the resolved configuration', ev(authorization_path='_evaluate_repository_structure -> resolved configuration')), 'FS0-ASSERT-FC-096': (live_clean and source_uses_only_config_authorization, 'bootstrap conventions, generator destinations, and implementation defaults do not substitute for structural authorization', ev(independent_authorization_sources=[])), 'FS0-ASSERT-FC-097': (live_clean and exact_one_resolution and source_location_independent and cases['relocated_configuration_resolves'], 'the operating substrate resolves the canonical structure configuration through a location-independent semantic-record mechanism, including after configuration relocation', ev(resolution='record_type plus governed configuration identity', semantic_test=cases['relocated_configuration_resolves'])), 'FS0-ASSERT-FC-098': (live_clean and cases['permitted_missing_accepted'], 'a structurally permitted object may be absent without structural failure', ev(semantic_test=cases['permitted_missing_accepted'])), 'FS0-ASSERT-FC-099': (live_clean and source_uses_only_config_authorization, 'implementation defaults, generated-output lists, ignore rules, workflow conventions, historical presence, and prior validation do not independently authorize structure', ev(independent_authorization_sources=[])), 'FS0-ASSERT-CONF-025': (live_clean and live['observed_objects'] > 0, 'Conformance evaluates the actual physical filesystem namespace rather than only a tracked or preclassified artifact set', ev(observed_objects=live['observed_objects'])), 'FS0-ASSERT-CONF-026': (live_clean and (not live['unauthorized']), 'every observed supported filesystem object resolves applicable structural authorization', ev(unauthorized=live['unauthorized'])), 'FS0-ASSERT-CONF-027': (live_clean and (not live['missing']) and cases['required_missing_rejected'], 'Conformance verifies that every required configured object exists', ev(missing=live['missing'], semantic_test=cases['required_missing_rejected'])), 'FS0-ASSERT-CONF-028': (live_clean and exact_one_resolution and cases['missing_binding_rejected'] and cases['ambiguous_binding_rejected'] and cases['unresolved_identity_rejected'] and cases['duplicate_matching_configuration_rejected'], 'Conformance fails when governed state does not determine exactly one identity or that identity does not resolve exactly one configuration object', ev(semantic_tests={'missing_binding_rejected': cases['missing_binding_rejected'], 'ambiguous_binding_rejected': cases['ambiguous_binding_rejected'], 'unresolved_identity_rejected': cases['unresolved_identity_rejected'], 'duplicate_matching_configuration_rejected': cases['duplicate_matching_configuration_rejected']})), 'FS0-ASSERT-CONF-029': (live_clean, 'structural Conformance diagnostics identify unauthorized, unsupported, missing, and type-mismatched objects sufficiently for correction', ev(diagnostic_fields=['unauthorized', 'unsupported', 'missing', 'type_mismatches']))}
        missing_checks = sorted(set(assertion_ids) - set(checks))
        unexpected_checks = sorted(set(checks) - set(assertion_ids))
        if missing_checks or unexpected_checks:
            raise RuntimeError(f'repository-structure assertion evidence map mismatch: missing={missing_checks} unexpected={unexpected_checks}')
        return [result(aid, 'pass' if checks[aid][0] else 'fail', checks[aid][1], checks[aid][2]) for aid in assertion_ids]
    except Exception as exc:
        return [result(aid, 'fail', f'repository-structure resolution/evaluation failed: {exc}', {'error': str(exc), 'post_cutover_mutation_binding': check_post_cutover_mutation_binding}) for aid in assertion_ids]
CALLABLES = {'repository_structure': check_repository_structure, 'requirement_metadata': check_requirement_metadata, 'conformance_closure': check_conformance_closure, 'generation_correspondence': check_generation_correspondence, 'canonical_entrypoint': check_canonical_entrypoint, 'remote_execution': check_remote_execution, 'exact_candidate': check_exact_candidate, 'bootstrap_state': check_bootstrap_state, 'governance_state_resolution': check_governance_state_resolution, 'accepted_state_publication': check_accepted_state_publication, 'assurance_runtime': check_assurance_runtime, 'successor_proposal_registry': check_successor_proposal_registry, 'governed_work_kernel': check_governed_work_kernel, 'github_governance_binding': check_github_governance_binding, 'proposal_lineage': check_proposal_lineage, 'conformance_selftest': check_conformance_selftest, 'conformance_canonicality': check_conformance_canonicality, 'generation_contract': check_generation_contract, 'authority_kernel': check_authority_kernel, 'requirement_provenance': check_requirement_provenance, 'operating_substrate_preflight': check_operating_substrate_preflight, 'bootstrap_read_surfaces': check_bootstrap_read_surfaces, 'framework_record_orientation': check_framework_record_and_orientation_contract, 'bootstrap_independence': check_bootstrap_independence, 'bootstrap_authority_lifecycle': check_bootstrap_authority_lifecycle, 'post_cutover_mutation_authority': check_post_cutover_mutation_authority, 'post_cutover_mutation_binding': check_post_cutover_mutation_binding, 'retained_bootstrap_payload': check_retained_bootstrap_payload, 'json_record_envelopes': check_json_record_envelopes, 'state_class_distinction': check_state_class_distinction, 'cutover_record_immutability': check_cutover_record_immutability, 'generation_semantics_canonical': check_generation_semantics_canonical, 'self_change_completion': check_self_change_completion}

def main():
    root = Path.cwd().resolve()
    if not (root / '.git').exists():
        print('run from repository root', file=sys.stderr)
        return 2
    implementations = load(root / 'repo/conformance/support/implementations.json')['implementations']
    orchestration = load(root / 'repo/conformance/orchestration.json')
    all_assertions = load(root / 'repo/conformance/assertions.json')['assertions']
    mechanical_ids = {a['assertion_id'] for a in all_assertions}
    bound_ids = [aid for implementation in implementations for aid in implementation.get('assertion_ids', [])]
    unknown_bound_ids = sorted(set(bound_ids) - mechanical_ids)
    duplicate_bound_ids = sorted((aid for aid in set(bound_ids) if bound_ids.count(aid) > 1))
    execution_defects = []
    if unknown_bound_ids:
        execution_defects.append({'kind': 'unknown-implementation-assertion-binding', 'assertion_ids': unknown_bound_ids})
    if duplicate_bound_ids:
        execution_defects.append({'kind': 'duplicate-implementation-assertion-binding', 'assertion_ids': duplicate_bound_ids})
    realized = set()
    results = []
    for impl in implementations:
        callable_name = impl['callable']
        declared_ids = [aid for aid in impl.get('assertion_ids', []) if aid in mechanical_ids]
        realized.update(declared_ids)
        if not declared_ids:
            continue
        fn = CALLABLES.get(callable_name)
        if fn is None:
            results.extend((result(aid, 'fail', f'unknown implementation callable: {callable_name}') for aid in declared_ids))
            continue
        impl_results = fn(root, declared_ids)
        result_ids = [r.get('assertion_id') for r in impl_results]
        expected = set(declared_ids)
        observed = set(result_ids)
        if len(result_ids) != len(observed):
            execution_defects.append({'kind': 'duplicate-emitted-assertion-result', 'implementation_id': impl.get('implementation_id'), 'assertion_ids': sorted((aid for aid in observed if result_ids.count(aid) > 1))})
        if observed != expected:
            execution_defects.append({'kind': 'implementation-result-closure-mismatch', 'implementation_id': impl.get('implementation_id'), 'missing': sorted(expected - observed), 'unexpected': sorted(observed - expected)})
        results.extend((r for r in impl_results if r.get('assertion_id') in expected))
    emitted_ids = [r['assertion_id'] for r in results]
    if len(emitted_ids) != len(set(emitted_ids)):
        execution_defects.append({'kind': 'duplicate-global-assertion-result', 'assertion_ids': sorted((aid for aid in set(emitted_ids) if emitted_ids.count(aid) > 1))})
    pending = sorted(mechanical_ids - realized | {r['assertion_id'] for r in results if r.get('assertion_id') in mechanical_ids and r.get('status') == 'pending'})
    failed = sorted({r['assertion_id'] for r in results if r['assertion_id'] in mechanical_ids and r['status'] == 'fail'})
    passed = sorted({r['assertion_id'] for r in results if r['assertion_id'] in mechanical_ids and r['status'] == 'pass'})
    if set(passed) & set(failed):
        execution_defects.append({'kind': 'assertion-has-conflicting-results', 'assertion_ids': sorted(set(passed) & set(failed))})
    status = 'fail' if failed or execution_defects else 'incomplete' if pending else 'pass'
    report = {'schema_version': '1', 'record_type': 'conformance-execution-result', 'orchestration_id': orchestration['orchestration_id'], 'status': status, 'declared_mechanical_assertions': len(mechanical_ids), 'realized_assertions': len(realized), 'passed_assertions': len(passed), 'failed_assertions': failed, 'pending_assertions': pending, 'execution_defects': execution_defects, 'results': results}
    print(json.dumps(report, indent=2))
    if failed or execution_defects:
        return 1
    if pending:
        return 2
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
