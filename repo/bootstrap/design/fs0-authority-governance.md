# FS0 Authority and Governance

## Status

Part of the non-authoritative FS0-Core Bootstrap Design Proposal.

Read `fs0-design.md` first. This chunk does not independently create authority.

---

# Accepted State and PR-Merge Acceptance

FS0 uses one GitHub acceptance model for governed repository changes.

A governed issue is the durable unit of work identity and bounded authorization. Each governed pull request SHALL identify exactly one governed issue. One governed issue MAY be realized through one or more pull requests, and each pull request MAY contain one or more commits.

The pull request is one candidate realization of its issue. Conformance applies to the complete current pull-request candidate, and required Assurance is performed as semantic audit of that same current candidate.

A required candidate semantic audit that passes SHALL be recorded as a structured JSON Assurance audit receipt in the pull-request discussion, bound to the exact current head and required review obligations, before merge. The issue's authorized acceptance actor then merges that exact conforming audited candidate. The authorized merge is simultaneously the candidate Assurance satisfaction disposition and explicit semantic acceptance; the audit receipt is evidence, not a separate approval.

Closing a pull request without merge does not accept it. A governed issue remains open after accepted pull requests until the resulting accepted `refs/heads/main` state has passed the governed-work completion semantic audit. That audit SHALL be recorded as a structured JSON Assurance audit receipt in the issue discussion, bound to the exact accepted revision and relevant accepted pull requests, before closure. Relevant accepted pull requests SHALL be linked to the issue through GitHub Development before completion. Authorized issue closure after that audit records completed-work Assurance satisfaction and completion; it does not create a second repository acceptance event.

If either semantic audit identifies a defect, corrective work SHALL remain within the existing issue's bounded scope or route through a separately authorized parallel governed issue when the correction exceeds that scope.

## Accepted Inputs and Resulting State

A merge candidate SHALL record the accepted predecessor state it depends on, including applicable accepted Design, accepted Plan, and accepted repository predecessor identities.

Those predecessor identities are known before merge and SHALL remain intact in the candidate. If an applicable predecessor changes before merge, the candidate SHALL be reevaluated.

The candidate SHALL NOT attempt to embed the Git SHA that its own merge will create.

For a successful governed merge:

```text
candidate identity = pull request + current head SHA
acceptance event = authorized merge
resulting accepted repository revision = refs/heads/main after merge
```

The GitHub merge record provides the attributable actor, time, pull-request identity, candidate head, and resulting repository revision.

`refs/heads/main` is the canonical accepted repository state after bootstrap cutover.

Conformance success or audit discussion does not independently create acceptance. Exact-candidate Conformance is the mechanical merge gate; authorized merge after semantic audit records candidate Assurance satisfaction and acceptance. Authorized governed-issue closure later records completed-work Assurance satisfaction without changing the accepted revision.

## Bootstrap

Initial bootstrap uses the same acceptance interaction.

The bootstrap provenance issue is the one-time work identity and authorization anchor. The bootstrap-cutover pull request is its candidate realization.

Bootstrap mechanical validation SHALL pass before that pull request is eligible for merge.

Because accepted FS0 Assurance does not yet exist, the authorized user's review and merge of the designated bootstrap-cutover pull request is both the required external semantic audit and explicit bootstrap acceptance.

After merge, the resulting `refs/heads/main` revision is the first accepted FS0 repository state.

No separate bootstrap acceptance comment, acceptance receipt, or `--accept-bootstrap` decision is required.

This bootstrap semantic-audit rule is one-time only; post-cutover governed work uses normal Conformance and Assurance eligibility before the same merge-acceptance action.

---

---

# FS0.1 — Authority Kernel

## Purpose

Provide the minimum accepted framework authority necessary to authorize and bound FS0 itself.

## Required Capabilities

FS0 shall establish:

- one machine-resolvable authoritative framework namespace whose concrete filesystem placement is configuration-defined;
- one foundational Framework Contract;
- Governance, Conformance, and Assurance as the only authority-bearing keystones;
- explicit delegation from the Framework Contract to each keystone;
- stable machine-resolvable identities for accepted normative authority;
- stable machine-resolvable identities for normative requirements;
- one controlling semantic owner for each independently governed semantic invariant;
- repository-wide default-deny filesystem authorization rooted at the repository root;
- exactly one canonical repository-structure configuration as the source of filesystem permission;
- positive authorization for every filesystem object beneath the repository root;
- directory authorization that does not authorize descendants unless complete-subtree authorization is explicit;
- explicitly governed structural extension semantics;
- prohibition of implicit authority;
- prohibition of normative authority arising from implementation, validation, review findings, generated artifacts, workflow convention, historical state, or product behavior;
- acyclic normative authority dependency; and
- resolvable provenance for maintained derived framework primitives.

## Minimum Authority Representation

FS0 must be able to resolve at least:

```text
authority identity
requirement identity
authority owner
dependency/delegation relationship
lifecycle state
provenance relationship
```

The representation may be simple.

FS0 does not require the final manifest, schema, or taxonomy design.

## Deferred

FS0 shall defer:

- complete repository artifact taxonomy;
- complete manifest architecture;
- generalized product authority model;
- final extension registry model;
- final generated projection model;
- rich repository-structure policy languages beyond the minimum closed-repository authorization semantics;
- reusable structure profiles;
- conditional structural policy; and
- advanced pattern or inheritance systems.

---

---

# FS0.2 — Governance Kernel

## Purpose

Provide the complete minimum self-building lifecycle.

## Primary Lifecycle

FS0 Governance shall implement:

**Design Proposal**
→ **Design**
→ **Plan**
→ **Build**
→ **accepted repository state**

Design, Plan, and Build shall be distinct governed work.

## Stage Structure

FS0 shall preserve the common three-step stage structure:

| Stage | Analysis | Production | Decision |
| --- | --- | --- | --- |
| Design | Audit | Normalize | Accept |
| Plan | Analyze | Specify | Accept |
| Build | Implement | Verify | Accept |

## Required Governed-Work Properties

Each governed stage shall have:

- stable identity;
- explicit predecessor;
- explicit scope;
- explicit exclusions where material;
- candidate result;
- completion conditions;
- explicit acceptance or rejection;
- provenance; and
- bounded authorization.

## Design

Design shall own persistent normative semantics.

Design shall:

- consume a non-authoritative Design Proposal;
- audit accepted authority and relevant repository state;
- identify conflicts, duplication, missing authority, and unresolved semantics;
- normalize candidate semantics into identified normative requirements;
- identify created, amended, superseded, or withdrawn authority; and
- explicitly accept or reject the normative delta.

Design shall not define implementation detail unless that detail is intentionally normative.

## Plan

Plan shall own realization intent.

Plan shall:

- consume accepted Design authority;
- identify affected artifacts and required work;
- identify required Conformance work;
- identify required Assurance work;
- identify dependencies and sequencing;
- define bounded Build work; and
- explicitly accept or reject realization intent.

Plan shall not create or amend normative semantics.

## Build

Build shall own realization.

Build shall:

- consume the accepted Plan;
- implement only authorized Plan work;
- produce required evidence;
- invoke required Conformance;
- invoke required Assurance;
- verify completion; and
- explicitly accept or reject the resulting repository state.

Build shall not invent Design semantics or Plan intent.

## Required Routing

FS0 shall support:

```text
semantic defect → Design
realization-intent defect → Plan
realization defect → Build
```

## Required Acceptance Rules

Acceptance shall be:

- explicit;
- attributable;
- traceable;
- candidate-specific; and
- realized by authorized merge after exact-candidate Conformance passes and required candidate semantic audit is satisfactory; the merge itself records candidate Assurance satisfaction.

Governance acceptance shall depend only on authority accepted before the candidate acquires the authority produced by that acceptance.

## Bounded Authorization

A governed work item shall authorize only its explicit scope.

Completion or acceptance shall not independently authorize unrelated or successor work.

---

---

# FS0.3 — Normative Requirement Kernel

## Purpose

Provide the canonical addressable unit of accepted normative semantics.

## Required Capabilities

Each accepted normative obligation shall have:

- stable requirement identity;
- one controlling normative owner;
- normative statement;
- lifecycle state;
- historical lineage where superseded or withdrawn;
- Conformance applicability; and
- Assurance applicability.

Unidentified accepted normative prose is not sufficient.

## Minimum Quality Discipline

Each uniquely identified normative requirement shall express exactly one primary normative obligation.

Each normative requirement statement shall contain no more than 300 characters.

Material normative semantics shall not be omitted solely to satisfy the statement-length bound.

Design Normalize shall decompose materially compound obligations into separately identified requirements.

FS0 Design Normalize and Assurance shall be capable of identifying at least:

- materially compound obligations;
- ambiguity;
- contradiction;
- duplication;
- inappropriate implementation leakage; and
- missing semantic ownership.

FS0 does not need the final requirement-quality framework.

---
