# FS0 Conformance and Assurance

## Status

Part of the non-authoritative FS0-Core Bootstrap Design Proposal.

Read `fs0-design.md` first. This chunk does not independently create authority.

---

# FS0.4 — Conformance Kernel

## Purpose

Provide closed mechanical enforcement of accepted normative authority.

## Canonical Relationship

For every accepted normative requirement:

```text
normative requirement
→ canonical Conformance correspondence
→ mechanical | none
```

If applicability is `mechanical`:

```text
normative requirement
→ assertion
→ implementation
→ evidence
→ canonical execution
```

## Required Primitive Classes

FS0 requires only these top-level primitive roles:

1. assertion;
2. support;
3. evidence; and
4. orchestration.

Additional primitive taxonomy is deferred.

## Assertion Identity

Assertion identity shall be distinct from implementation-callable identity.

One requirement may derive multiple assertions.

Multiple assertions may share implementation where identities and provenance remain distinct.

## Required Closure Properties

FS0 Conformance shall establish all required closures.

### Authority Closure

Every maintained Conformance primitive shall resolve to accepted normative authority.

### Coverage Closure

Every mechanically applicable requirement shall resolve to at least one executable assertion.

### Evidence Closure

Every executable assertion shall have the evidence required by FS0 Conformance authority.

### Execution Closure

Every gating assertion shall be reachable from authorized canonical Conformance execution.

### Repository-Structure Closure

Every filesystem object beneath the repository root shall resolve to applicable positive authorization in the canonical repository-structure configuration.

A filesystem object for which no authorization resolves shall cause Conformance failure.

A directory shall not authorize descendants unless its applicable authorization explicitly grants complete-subtree permission.

Every configuration entry that requires an object to exist shall resolve to a corresponding filesystem object.

Repository-structure Conformance shall evaluate the actual filesystem namespace rather than only version-controlled, maintained, generated, or otherwise preclassified objects.

Each observed filesystem object shall have a mechanically identified object type.

FS0 shall support ordinary files, directories, and symbolic links as explicit structural object types.

Any filesystem object type not supported by the canonical repository-structure configuration semantics shall be denied.

A symbolic link shall be evaluated as the link object itself.

Repository-structure traversal shall not follow a symbolic-link target to discover descendants, and a symbolic-link target outside the repository root shall not extend the structural governance boundary.

### Generation Correspondence Closure

Every generated FS0 read surface shall resolve through the canonical generation-source registry to a canonical bootstrap source definition.

Canonical Conformance shall mechanically verify generated read surfaces against deterministic regeneration from their declared source inputs.

A failed generation-correspondence check shall produce a Conformance defect.

Bootstrap source shall not replace the generated read surface as authority when correspondence fails.

## Minimum Evidence

FS0 shall support enough evidence to demonstrate:

- conforming state is accepted;
- targeted violating state is rejected; and
- required assertions actually execute.

The final evidence taxonomy is deferred.

## Canonical Execution

FS0 shall provide one canonical remotely runnable Conformance surface suitable for GitHub Actions.

Local execution may exist as an implementation convenience.

Before cutover, the candidate remote execution surface shall run in GitHub Actions as bootstrap mechanical verification evidence.

After cutover, that accepted execution surface becomes canonical FS0 Conformance execution unless later changed through Governance.

---

---

# FS0.5 — Assurance Kernel

## Purpose

Provide governed semantic review sufficient to prevent the bootstrap framework from accepting semantically defective authority or realization merely because Conformance passes.

## Canonical Relationship

For every accepted normative requirement:

```text
normative requirement
→ canonical Assurance correspondence
→ required | none
```

If Assurance is required:

```text
accepted authorizing authority
→ review obligation
→ governed issue / pull-request audit context
→ review subject + GitHub evidence/history
→ semantic audit
→ Governance disposition
```

For a pull-request candidate, successful Assurance disposition is the authorized merge of the exact conforming candidate after semantic audit. For completed governed work, successful Assurance disposition is authorized closure of the governed issue after semantic audit of the resulting accepted `refs/heads/main` state and Development linkage of the relevant accepted pull requests.

GitHub issue and pull-request discussion/history, review history, check history, Development relationships, merge history, and issue-closure history are the maintained Assurance provenance surfaces. FS0 does not require duplicate repository-tree case or finding artifacts.

A completed candidate semantic audit SHALL emit one structured JSON audit receipt in the pull-request discussion. The receipt SHALL identify the governed work, issue, pull request, exact candidate head, required obligation identities, outcome, evidence, material exclusions, and audit time. A changed candidate head makes an earlier candidate receipt inapplicable.

A completed governed-work semantic audit of `refs/heads/main` SHALL emit one structured JSON audit receipt in the governed issue discussion. The receipt SHALL identify the governed work, issue, exact accepted revision, relevant accepted pull requests, required obligation identities, outcome, evidence, material exclusions, and audit time.

For either disposition, only an applicable receipt created before the merge or issue closure may establish the audit prerequisite. When multiple receipts apply to the same exact subject, the latest applicable receipt controls; an adverse latest receipt requires further governed work. Receipt history is Assurance evidence. Merge and issue closure remain the Governance dispositions.

## Required Capabilities

FS0 Assurance shall support at least:

- requirement-quality review;
- ambiguity review;
- contradiction review;
- Design fidelity review;
- Plan fidelity review;
- Build realization-fidelity review;
- Conformance interpretation review; and
- evidence-sufficiency review.

## Minimum Audit Outcome Vocabulary

FS0 may use a minimal semantic-audit outcome vocabulary:

- `satisfied`;
- `defect`;
- `insufficient`; and
- `governance-required`.

Adverse outcomes require further governed work before the applicable merge or issue closure. The final finding taxonomy is deferred.

## Required Scope Rules

Every governed semantic-audit context shall make resolvable:

- authorizing authority;
- review obligation;
- reviewed subject;
- evidence/history;
- exclusions where material; and
- the applicable Governance disposition event.

The governed issue and its associated pull request provide the durable review identity and context. A review subject shall not authorize its own review.

## Required Boundary

Assurance audit conclusions are context-specific.

Audit discussion or conclusions shall not independently create, amend, supersede, or withdraw persistent normative authority.

Persistent semantic change shall route through Governance Design.

---
