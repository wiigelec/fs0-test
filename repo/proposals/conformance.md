# Conformance Architecture Proposal

## Status

Design proposal for audit against the current repository.

This document is non-authoritative.

Its purpose is to define a candidate Conformance architecture subordinate to the Framework Contract and compatible with the proposed Governance lifecycle.

Conformance is responsible for mechanical enforcement of accepted normative authority.

This proposal supersedes the narrower task-centric validation-package model as the architectural direction for mechanical enforcement.

The existing validation proposal remains useful historical design input, but its correspondence model is too coarse to establish provenance closure across every maintained validation primitive.

This proposal does not define persistent normative change or semantic review. Those responsibilities belong to Governance and Assurance.

## Framework Contract Basis

This proposal assumes the candidate Framework Contract requirements:

- FC-01 — Framework Authority Location
- FC-02 — Framework Contract Role
- FC-03 — Keystone Set
- FC-04 — Delegated Authority
- FC-05 — Governance Exclusivity
- FC-06 — Conformance Exclusivity
- FC-07 — Assurance Exclusivity
- FC-08 — Assurance Persistence Boundary
- FC-09 — Keystone Separation
- FC-10 — Derived Provenance
- FC-11 — No Implicit Authority
- FC-12 — Product Subordination
- FC-13 — Authority Identity
- FC-14 — Delegation Resolution

Conformance shall not assume authority beyond that delegated by the Framework Contract.

## Governance Basis

This proposal assumes the candidate Governance lifecycle:

**Design Proposal**  
→ **Design**  
→ **Plan**  
→ **Build**

Design establishes accepted normative semantics.

Plan establishes accepted realization intent.

Build realizes accepted Plan authority.

Conformance may provide mechanical findings and evidence to Governance.

Conformance shall not create Governance authority or constitute Governance acceptance.

## Objective

Conformance shall provide one closed mechanical-enforcement architecture in which:

- every maintained Conformance primitive derives from accepted normative authority;
- every mechanically applicable accepted requirement resolves to executable enforcement;
- every executable assertion has required evidence;
- every gating assertion participates in authorized canonical execution; and
- no Conformance primitive or finding independently creates normative semantics.

The primary relationship is:

**accepted normative requirement**  
↔ **canonical Conformance correspondence**  
↔ **Conformance primitive graph**  
↔ **mechanical findings and evidence**

The architecture shall establish four closure properties:

1. authority closure;
2. coverage closure;
3. evidence closure; and
4. execution closure.

## Conformance Boundary

Conformance owns mechanical evaluation of objectively decidable obligations derived from accepted normative authority.

Conformance may:

- inspect observable state;
- evaluate mechanical predicates;
- reject mechanically nonconforming state;
- produce mechanical findings;
- produce deterministic evidence;
- maintain canonical Conformance correspondence;
- maintain Conformance primitives;
- maintain canonical execution surfaces;
- mechanically verify its own closure properties; and
- expose subordinate generated views.

Conformance shall not:

- create normative requirements;
- amend normative requirements;
- extend accepted normative semantics;
- choose among materially ambiguous interpretations;
- convert implementation preference into normative enforcement;
- infer normative authority from historical behavior;
- treat implementation as normative authority;
- perform semantic adjudication reserved to Assurance; or
- establish Governance acceptance.

## Conformance Terminology

### Normative Requirement

An identified accepted normative obligation.

The normative requirement is the semantic authority.

Conformance references the requirement but shall not independently restate, replace, or extend its semantics.

### Conformance Correspondence

The governed relationship between one accepted normative requirement and the Conformance responsibility derived from that requirement.

Correspondence records:

- requirement identity;
- Conformance applicability; and
- direct assertion relationships where applicable.

Correspondence does not independently own normative semantics.

### Conformance Primitive

A maintained executable, declarative, evidentiary, supporting, or orchestration element whose purpose participates in normative mechanical enforcement.

### Assertion

A Conformance primitive representing one independently identifiable mechanically decidable predicate derived from accepted normative authority.

An assertion is the primary executable unit of mechanical enforcement correspondence.

### Evidence Primitive

A Conformance primitive whose purpose is to demonstrate the behavior of an assertion or enforcement path.

### Supporting Primitive

A Conformance primitive that supports enforcement without itself representing a complete normative predicate.

### Orchestration Primitive

A Conformance primitive responsible for composing, discovering, dispatching, loading, or executing other Conformance primitives.

## Closed Conformance Hierarchy

Normative mechanical enforcement shall occur only through the governed Conformance hierarchy.

A maintained artifact whose purpose is normative mechanical enforcement shall participate in that hierarchy.

Applicable artifacts include:

- assertions;
- schemas;
- helpers;
- adapters;
- fixtures;
- tests;
- runners;
- dispatchers;
- loaders;
- registries;
- generators; and
- other enforcement-supporting artifacts.

An artifact outside the governed Conformance hierarchy shall not independently impose normative mechanical enforcement.

Conformance may consume general implementation outside the hierarchy.

Such implementation does not become normative authority merely because Conformance depends on it.

## Purpose of the Closed Hierarchy

The closed hierarchy is an authority-control mechanism rather than merely a directory convention.

It prevents:

- ad hoc validation;
- hidden enforcement in unrelated implementation;
- ungoverned AI-generated validators;
- orphan tests;
- orphan fixtures;
- helpers that silently introduce constraints;
- schemas that become de facto semantic authorities;
- duplicate requirement-to-validator registries; and
- enforcement derived from historical implementation rather than accepted authority.

When mechanical enforcement is required, the governed relationship is:

**accepted normative requirement**  
→ **canonical Conformance correspondence**  
→ **assertion**  
→ **supporting and evidence primitives**  
→ **canonical execution**

If no accepted normative requirement authorizes an enforcement behavior, Conformance shall not invent that behavior.

## Primitive Classes

Conformance shall distinguish at least four functional primitive classes:

1. assertions;
2. supporting primitives;
3. evidence primitives; and
4. orchestration primitives.

A subordinate controlled taxonomy may further distinguish:

- helper;
- adapter;
- schema;
- fixture;
- positive case;
- rejection case;
- boundary case;
- regression case;
- mutation case;
- unit test;
- integration test;
- self-test;
- runner;
- dispatcher;
- loader;
- registry; and
- generator.

Primitive class identifies Conformance role.

Primitive class does not grant normative authority.

## Assertion Model

An assertion represents one independently identifiable mechanically decidable predicate.

Assertion identity shall be distinct from implementation-callable identity.

One normative requirement may derive multiple assertions.

Multiple assertions may share one callable where their identities and provenance remain distinguishable.

For example:

**Requirement R**  
→ **Assertion A1**  
→ callable X

**Requirement R**  
→ **Assertion A2**  
→ callable X

The callable is implementation.

A1 and A2 are independently identifiable enforcement predicates.

This permits precise correspondence without requiring one trivial implementation function per assertion.

## Assertion Ownership

Each assertion shall directly resolve to exactly one accepted normative requirement.

If one implementation callable checks predicates derived from multiple requirements, separate assertion identities shall represent those predicates.

This preserves deterministic semantic ownership while permitting shared implementation.

## Supporting Primitive Sharing

Supporting primitives may serve multiple assertions.

A shared primitive does not require one direct normative owner when its transitive provenance remains resolvable.

Examples include:

- helper libraries;
- parsers;
- adapters;
- shared fixtures;
- common runners; and
- common infrastructure.

Shared support shall not be duplicated merely to create artificial one-requirement-per-function correspondence.

## Direct and Transitive Provenance

Conformance shall distinguish direct provenance from transitive provenance.

### Direct Provenance

A primitive directly corresponds to a requirement-derived enforcement or evidence obligation.

Typical examples include:

- assertion;
- requirement-specific rejection case;
- requirement-specific boundary case; and
- requirement-specific fixture.

### Transitive Provenance

A primitive supports another Conformance primitive that ultimately resolves to accepted normative authority.

Typical examples include:

- shared helper;
- parser;
- adapter;
- runner;
- loader; and
- common fixture.

Both relationships shall be mechanically resolvable.

## Authority Closure

Every maintained Conformance primitive shall resolve through governed provenance to at least one accepted normative requirement.

Conceptually:

**∀ maintained primitive P: ∃ accepted requirement R such that R →* P**

No orphan Conformance primitive is permitted.

An orphan primitive is a Conformance defect.

Normative provenance shall not be inferred solely from:

- file location;
- naming;
- nearby tests;
- implementation behavior;
- historical use; or
- apparent usefulness.

## Canonical Correspondence

Each active normative requirement shall have exactly one canonical Conformance correspondence record.

The correspondence record shall identify:

- the normative requirement;
- its canonical Conformance applicability; and
- its direct assertion relationships where applicable.

If Conformance applicability is `none`, the correspondence shall identify the governed rationale for that determination.

Correspondence shall not duplicate normative requirement text as independent semantic authority.

## Conformance Applicability

Each active normative requirement shall have exactly one canonical Conformance applicability determination.

The candidate vocabulary is:

### `mechanical`

The requirement has mechanically enforceable responsibility within Conformance scope.

A mechanically applicable requirement shall resolve to executable assertion coverage.

### `none`

The requirement has no meaningful mechanical enforcement responsibility within Conformance scope.

A governed rationale is required.

Conformance applicability describes only Conformance responsibility.

It shall not encode Assurance responsibility.

Terms such as:

- `partial`; and
- `semantic-review`

shall therefore not be primary Conformance dispositions.

A requirement may independently have:

- mechanical Conformance responsibility; and
- Assurance responsibility.

Cross-keystone conditions should be derived from those separate relationships.

## Requirement Quality and Mechanical Decomposition

Conformance shall not silently decompose ambiguous normative authority into invented normative predicates.

If an accepted requirement contains multiple independently governed obligations, Design should normalize those obligations where appropriate.

If an assertion requires choosing among materially different semantic interpretations, Conformance shall not make that choice independently.

The issue shall route through Governance and, where semantic judgment is required, Assurance.

Conformance shall not alter normative meaning merely to make enforcement easier to implement.

## Coverage Closure

Each accepted normative requirement with mechanical Conformance applicability shall resolve to at least one executable assertion.

Conceptually:

**∀ mechanical requirement R: ∃ executable assertion A such that R → A**

A mechanical applicability determination with zero executable assertions is incomplete Conformance.

Correspondence metadata alone does not satisfy coverage closure.

## Evidence Model

Executable enforcement requires governed evidence demonstrating that enforcement behaves correctly.

Evidence classes may include:

- rejection evidence;
- positive evidence;
- boundary evidence;
- regression evidence;
- mutation evidence;
- unit evidence;
- integration evidence; and
- self-test evidence.

The exact evidence obligations applicable to an assertion belong in subordinate Conformance authority.

## Evidence Closure

Each executable assertion shall satisfy the governed evidence obligations applicable to that assertion.

Conceptually:

**∀ executable assertion A: required evidence obligations(A) are satisfied**

Evidence should be sufficient to demonstrate that the assertion behaves as intended as mechanical enforcement.

An assertion shall not be considered adequately evidenced merely because its implementation executes successfully.

## Rejection Evidence

Rejection evidence demonstrates that representative violating state is rejected.

Rejection evidence is the expected baseline for most enforcement assertions because it demonstrates that the targeted violation changes the Conformance result.

The exact exceptions and required rejection-evidence rules belong in subordinate Conformance authority.

## Positive Evidence

Positive evidence demonstrates that representative conforming state is accepted.

It primarily protects against over-enforcement.

Positive evidence is especially useful for:

- permitted alternatives;
- optional structures;
- extension points;
- valid namespace locations; and
- permitted lifecycle transitions.

## Boundary Evidence

Boundary evidence demonstrates behavior at transitions between permitted and prohibited state.

It is especially useful for:

- cardinality;
- path roots;
- namespaces;
- lifecycle transitions;
- exact sets;
- optional versus required structures; and
- minimum or maximum values.

## Regression Evidence

Regression evidence demonstrates continued protection against a previously observed defect.

Historical issue, defect, or revision references may accompany regression evidence.

Historical provenance remains evidence only.

It does not become normative authority.

## Mutation Evidence

Mutation evidence intentionally alters otherwise conforming state to create a targeted violation.

Mutation evidence may demonstrate that:

- an assertion is actually executed;
- a targeted violation changes the result;
- canonical execution does not silently skip enforcement; and
- an evidence fixture meaningfully exercises the intended predicate.

Detailed mutation policy belongs in subordinate Conformance authority.

## Schemas

A schema used for normative mechanical enforcement is a Conformance primitive.

Its normative provenance follows the same rule as every other Conformance primitive.

A schema does not become normative authority merely because validators consume it.

Schema behavior imposing constraints absent from accepted normative authority is over-enforcement.

Schema behavior omitting mechanically required constraints is under-enforcement.

## Fixtures

A maintained fixture used by Conformance is a Conformance primitive.

Its provenance shall resolve directly or transitively to the enforcement or evidence responsibility it serves.

Fixture meaning shall not depend solely on file naming or directory placement.

Where fixture role affects Conformance behavior, that role should be mechanically resolvable.

## Unit Tests

A maintained unit test of Conformance implementation is a Conformance primitive.

It shall resolve to the primitive or responsibility whose behavior it verifies.

Through that relationship it shall resolve to accepted normative authority.

Unit tests demonstrate implementation behavior.

They do not by themselves satisfy coverage closure unless they also represent identified executable assertions.

## Integration Tests

An integration test is a Conformance evidence primitive that verifies behavior through maintained execution boundaries.

It may verify:

- runner composition;
- dispatch;
- public validation surfaces;
- failure propagation; and
- repository-wide execution.

Integration evidence remains subordinate to accepted normative authority.

## Self-Tests

Conformance self-tests verify the Conformance architecture and implementation itself.

Self-tests may verify:

- provenance closure;
- correspondence integrity;
- assertion execution;
- evidence relationships;
- canonical execution;
- schema behavior;
- runner behavior;
- generated projections; and
- failure propagation.

Self-tests are themselves Conformance primitives.

They shall satisfy the same provenance obligations as other maintained Conformance primitives.

Conformance shall not exempt its own infrastructure from its authority model.

## Orchestration Primitives

Runners, dispatchers, loaders, registries, and similar orchestration mechanisms are Conformance primitives.

Their provenance may be transitive through the assertions and Conformance responsibilities they serve.

They do not need to claim direct ownership of every normative requirement whose enforcement they orchestrate.

## Canonical Execution

Conformance shall define authorized canonical execution surfaces.

Each gating assertion shall be reachable from an authorized canonical Conformance execution surface.

Canonical execution may be hierarchical.

For example:

**repository Conformance runner**  
→ **framework Conformance runner**  
→ **product Conformance runner**

The exact orchestration model belongs in subordinate design.

## Execution Closure

Each gating assertion shall participate in authorized canonical execution.

Conceptually:

**∀ gating assertion A: canonical execution →* A**

An assertion may have correct authority, correspondence, and evidence while still failing to provide actual enforcement if it is not executed through the required gating path.

Execution closure prevents that condition.

## The Four Closure Properties

The architecture centers on four closure properties.

### Authority Closure

**accepted normative authority → every maintained Conformance primitive**

No orphan Conformance behavior.

### Coverage Closure

**mechanically applicable requirement → executable assertion**

No mechanically applicable requirement without enforcement.

### Evidence Closure

**executable assertion → required evidence**

No unsupported enforcement predicate.

### Execution Closure

**authorized canonical execution → every gating assertion**

No required enforcement silently omitted from execution.

Together:

**Authority explains why enforcement exists.**

**Coverage establishes that required enforcement exists.**

**Evidence demonstrates that enforcement behaves correctly.**

**Execution establishes that required enforcement actually runs.**

## Bidirectional Correspondence

Canonical Conformance correspondence and primitive provenance shall support mechanically resolvable forward and reverse navigation.

Forward:

**normative requirement**  
→ **canonical correspondence**  
→ **assertion**  
→ **evidence/supporting/orchestration primitives**

Reverse:

**Conformance primitive**  
→ **provenance path**  
→ **accepted normative requirement**

Reverse provenance may be:

- direct for assertions;
- direct or transitive for evidence;
- transitive for shared infrastructure.

## Primitive Identity

Each Conformance primitive requiring independent correspondence shall have an identity appropriate to its governed role.

Assertion identities shall be stable and unique.

Other primitive identities shall be stable where required by correspondence, provenance, evidence, or historical resolution.

Primitive identity should remain distinct from mutable implementation coordinates where practical.

A stable primitive identity may survive:

- source movement;
- function renaming;
- helper extraction;
- runner reorganization; and
- implementation refactoring

when its governed Conformance role remains unchanged.

A Conformance primitive identity shall not be reused for unrelated behavior.

## Single Correspondence Authority

Conformance shall define one canonical authority for requirement-to-Conformance correspondence.

Independently maintained mappings shall not be allowed to silently diverge.

Requirement relationships shall not be separately redefined without verification in:

- correspondence records;
- source annotations;
- registries;
- runner lists;
- test manifests;
- schemas;
- generated documentation; or
- dispatch logic.

Where multiple operational representations are required, they shall be:

- generated from canonical correspondence; or
- mechanically verified against it.

## Correspondence Package Evolution

The current validation-package concept may remain as the canonical requirement-level correspondence container.

Its role should change from a flat validation-task registry to an entry point into the Conformance graph.

A conceptual package may resemble:

{
  "normative_requirement_id": "REPO-VAL-021",
  "conformance_applicability": "mechanical",
  "assertions": [
    "CONF-ASSERT-0041",
    "CONF-ASSERT-0042"
  ]
}

The exact representation remains subject to detailed design.

The architectural requirement is one canonical correspondence authority, not one particular file format.

## Correspondence Integrity

Canonical Conformance correspondence shall remain mechanically consistent with the maintained primitive graph.

Conformance shall detect stale or contradictory relationships such as:

- correspondence referencing nonexistent assertions;
- assertions whose direct requirement ownership disagrees with correspondence;
- removed primitives still referenced by canonical correspondence; and
- duplicate operational mappings that diverge from canonical correspondence.

## Findings

A Conformance finding is a mechanical result produced through governed Conformance execution.

A violation finding shall identify:

- the assertion from which it derives; and
- the accepted normative requirement owning that assertion.

A finding should additionally identify:

- the observed subject;
- the mechanical outcome; and
- sufficient diagnostic context.

Findings shall be suitable for machine resolution and human remediation.

A finding shall not create, amend, or extend normative semantics.

## Finding Classes

Conformance may distinguish findings such as:

- pass;
- violation;
- Conformance-system defect; and
- mechanically undecidable.

`Mechanically undecidable` means Conformance cannot establish the result mechanically under current authority and implementation.

It shall not be used as a substitute for Assurance judgment.

If undecidability results from ambiguous authority, the issue routes toward Assurance and Governance.

If undecidability results from missing or defective mechanical enforcement, it is a Conformance defect.

## Determinism

Equivalent accepted authority and equivalent observable state should produce equivalent Conformance outcomes.

Material enforcement outcomes should not depend on incidental nondeterminism such as:

- traversal order;
- filesystem order;
- hash ordering;
- locale;
- unstable defaults; or
- irrelevant environment state.

Where external state is normatively relevant, accepted authority shall establish that relevance.

## Generated Views

Generated Conformance coverage and correspondence views may be derived from canonical correspondence and primitive provenance.

Derived views may include:

- requirement identity;
- applicability;
- assertion relationships;
- evidence relationships;
- execution reachability;
- supporting primitives; and
- closure defects.

Generated views remain subordinate derived artifacts.

They shall not become competing correspondence or semantic authority.

A declaration such as `validated: true` shall not substitute for closure.

## Conformance Self-Validation

Conformance shall mechanically verify the integrity of its own governed model.

At minimum, Conformance self-validation shall enforce required:

- authority closure;
- coverage closure;
- evidence closure; and
- execution closure.

It should additionally verify:

- assertion identity integrity;
- primitive identity integrity where applicable;
- correspondence integrity; and
- hierarchy integrity.

Self-validation enforces accepted Conformance authority.

It does not independently create that authority.

## Closure Enforcement

A governed Conformance state that violates required closure shall be mechanically nonconforming.

Examples include:

### Authority Closure Defect

A maintained Conformance primitive has no provenance path to accepted normative authority.

### Coverage Closure Defect

A mechanically applicable normative requirement has no executable assertion.

### Evidence Closure Defect

An executable assertion does not satisfy its governed evidence obligations.

### Execution Closure Defect

A gating assertion is unreachable from authorized canonical execution.

Conformance shall mechanically reject such states.

## Other Conformance Defects

Other defects may include:

- assertion with no direct normative owner;
- invalid provenance edge;
- duplicate assertion identity;
- unrelated identity reuse;
- stale canonical correspondence;
- divergent duplicate mapping;
- enforcement outside the governed hierarchy;
- schema behavior imposing unauthorized constraints;
- helper behavior introducing undeclared constraints;
- finding semantics exceeding accepted authority; and
- canonical execution silently skipping required enforcement.

A Conformance defect shall not be repaired by inventing normative authority.

If accepted authority is insufficient, the issue shall route through Governance and, where semantic judgment is necessary, Assurance.

## Relationship to Governance

Governance creates and changes accepted normative authority.

Conformance consumes accepted normative authority.

Governance may require Conformance findings or evidence for stage acceptance.

Conformance results do not themselves constitute Governance acceptance.

When Conformance exposes a defect:

### Normative Semantic Defect

Route to Governance Design.

### Realization-Intent Defect

Route to Governance Plan.

### Realization Defect

Route to Governance Build.

Conformance reports mechanically established facts.

Governance determines persistent change and lifecycle disposition.

## Relationship to Assurance

Assurance may evaluate:

- whether Conformance applicability is semantically justified;
- whether an assertion correctly interprets accepted authority;
- whether mechanical decomposition introduces unintended semantics;
- whether evidence is semantically sufficient where mechanical criteria cannot decide sufficiency;
- whether a requirement is too ambiguous for mechanical enforcement; and
- whether a claimed `none` applicability is semantically justified.

Assurance shall not independently rewrite Conformance semantics into persistent authority.

Persistent semantic corrections shall route through Governance.

## Human and Automated Actors

Humans, automated tooling, and AI agents may perform Conformance work where authorized.

Actor capability does not determine authority.

When adding or changing mechanical enforcement, the governed sequence should be:

1. identify accepted normative authority;
2. identify canonical Conformance correspondence;
3. establish assertion identity;
4. implement or reuse supporting primitives;
5. provide required evidence;
6. connect gating assertions to canonical execution;
7. preserve primitive provenance; and
8. verify closure.

An automated actor shall not:

- add ad hoc enforcement outside the hierarchy;
- infer normative constraints from implementation;
- invent missing requirements;
- create orphan tests or fixtures;
- treat schemas as independent semantic authority;
- claim coverage from correspondence existence alone; or
- bypass canonical execution.

## Candidate Conformance Requirements

The following candidate requirements are intended for Design-stage normalization.

### CONF-01 — Closed Conformance Hierarchy

**Normative mechanical enforcement SHALL occur only through the governed Conformance hierarchy.**

### CONF-02 — Primitive Provenance

**Every maintained Conformance primitive SHALL resolve through governed provenance to at least one accepted normative requirement.**

### CONF-03 — Canonical Correspondence

**Each active normative requirement SHALL have exactly one canonical Conformance correspondence record.**

### CONF-04 — Conformance Applicability

**Each active normative requirement SHALL have exactly one canonical Conformance applicability determination.**

### CONF-05 — Mechanical Coverage

**Each normative requirement with mechanical Conformance applicability SHALL resolve to at least one executable assertion.**

### CONF-06 — Assertion Identity

**Each maintained Conformance assertion SHALL have a stable unique identity.**

### CONF-07 — Assertion Ownership

**Each maintained Conformance assertion SHALL directly resolve to exactly one accepted normative requirement.**

### CONF-08 — Conformance Semantic Boundary

**A Conformance primitive or finding SHALL NOT independently create, amend, or extend normative semantics.**

### CONF-09 — Non-Mechanical Rationale

**A normative requirement with no mechanical Conformance applicability SHALL have a governed rationale for that determination.**

### CONF-10 — Evidence Closure

**Each executable Conformance assertion SHALL satisfy the governed evidence obligations applicable to that assertion.**

### CONF-11 — Execution Closure

**Each gating Conformance assertion SHALL be reachable from an authorized canonical Conformance execution surface.**

### CONF-12 — Correspondence Integrity

**Canonical Conformance correspondence SHALL remain mechanically consistent with the maintained Conformance primitive graph.**

### CONF-13 — Single Correspondence Authority

**Requirement-to-Conformance correspondence SHALL NOT depend on independently maintained mappings that may silently diverge.**

### CONF-14 — Primitive Identity Preservation

**A Conformance primitive identity SHALL NOT be reused for unrelated Conformance behavior.**

### CONF-15 — Finding Traceability

**A Conformance violation finding SHALL identify the assertion and accepted normative requirement from which it derives.**

### CONF-16 — Closure Enforcement

**Conformance SHALL mechanically reject governed Conformance state that violates required authority, coverage, evidence, or execution closure.**

## Primary Design Invariant

**Conformance SHALL mechanically enforce accepted normative authority through a closed and self-validating provenance graph in which every maintained Conformance primitive is authorized by accepted normative requirements, every mechanically applicable requirement resolves to executable assertions, every executable assertion satisfies required evidence obligations, every gating assertion participates in authorized canonical execution, and no Conformance primitive or finding independently creates normative semantics.**

All detailed Conformance design shall preserve this invariant.

## Audit Questions

The current repository should be audited against this proposal by determining:

1. Which maintained validation artifacts are Conformance primitives.

2. Which current Conformance primitives lack resolvable provenance to accepted normative authority.

3. Which active normative requirements should have `mechanical` applicability.

4. Which active normative requirements should have `none` applicability.

5. Which current `none` or `not-applicable` decisions lack adequate rationale.

6. Which mechanically applicable requirements lack executable assertions.

7. Which current validation functions contain multiple independently identifiable assertions.

8. Which current tagged entry points identify implementation callables rather than independently governed assertions.

9. Which assertions directly map to more than one normative requirement and therefore require decomposition of assertion identity.

10. Which shared helpers, fixtures, schemas, runners, loaders, registries, or generators require transitive provenance.

11. Which unit tests, integration tests, self-tests, and other evidence primitives lack provenance.

12. Which executable assertions fail governed evidence obligations.

13. Which gating assertions are unreachable from canonical execution.

14. Which enforcement behavior exists outside the governed Conformance hierarchy.

15. Which schemas or helpers enforce constraints not clearly authorized by accepted normative authority.

16. Which current validation-package dispositions combine Conformance and Assurance responsibilities.

17. Which `partial` relationships should instead be represented by independent Conformance and Assurance correspondence.

18. Which `semantic-review` relationships belong entirely to Assurance.

19. Which validation task categories should become evidence classes rather than primary correspondence identities.

20. Which existing validator callables should expose multiple assertion identities.

21. Which current mappings are duplicated across packages, source metadata, runners, scripts, registries, or generated artifacts.

22. Which generated artifacts should remain subordinate projections of canonical correspondence.

23. Which current findings fail to identify both assertion and normative requirement identity.

24. Which existing self-tests already verify authority, coverage, evidence, or execution closure.

25. Whether each candidate CONF requirement represents one independently identifiable obligation.

26. Whether any candidate CONF requirement duplicates or logically follows from another.

27. Which candidate CONF requirements require Assurance for semantic evaluation.

28. What minimum Conformance authority must be accepted before Governance may require closure at Build acceptance.

## Explicitly Deferred Concerns

The following concerns are intentionally outside this Conformance proposal:

- exact directory layout;
- exact correspondence-package schema;
- exact primitive metadata syntax;
- exact assertion identifier format;
- exact decorator or source-tag syntax;
- exact evidence-policy matrix;
- exact fixture naming convention;
- exact runner implementation;
- exact programming language;
- exact diagnostic serialization;
- exact failure aggregation policy;
- exact generated Markdown format;
- exact mutation-testing framework;
- exact Assurance correspondence model;
- migration sequencing from the current validation architecture; and
- bootstrap accommodations.

These concerns may be defined by subordinate Conformance authority during detailed Design and Plan.

## Relationship to Assurance

The Assurance Architecture Proposal shall define semantic review of:

- normative requirement quality;
- ambiguous or incompletely mechanical obligations;
- Conformance applicability decisions;
- assertion interpretation;
- semantic sufficiency of evidence; and
- case-specific semantic conclusions.

Conformance shall establish mechanically decidable facts.

Assurance shall evaluate matters requiring semantic judgment.

Neither shall independently create persistent normative authority.

Persistent semantic change shall return through Governance.
