# Framework Contract Architecture Proposal

## Status

Design proposal for audit against the current repository.

This document is non-authoritative.

Its purpose is to define a candidate foundational authority model for the repository framework before Governance, Conformance, and Assurance are designed and normalized into accepted authority.

This proposal intentionally defines only:

- framework authority;
- delegated authority;
- keystone separation;
- authority flow;
- provenance;
- framework/product authority boundaries; and
- framework self-governance.

Detailed keystone mechanics, requirement-quality mechanics, migration mechanics, bootstrap mechanics, and successor-construction mechanics are outside this proposal.

## Objective

The repository framework shall define one foundational Framework Contract that authorizes and bounds three authority-bearing keystones:

1. Governance
2. Conformance
3. Assurance

The Framework Contract shall establish:

- where framework authority resides;
- what powers each keystone may exercise;
- what powers each keystone may not exercise;
- how persistent normative authority may change;
- how mechanical enforcement remains subordinate to accepted authority;
- how semantic review remains subordinate to accepted authority;
- how derived framework behavior remains traceable to accepted authority;
- how product authority remains subordinate to framework authority; and
- how authority relationships remain explicit and machine-resolvable.

The primary architectural objective is separation of responsibility under explicit accepted authority.

## Foundational Model

`repo/` contains accepted repository-framework normative authority.

The Framework Contract is the foundational normative layer within `repo/`.

The Framework Contract authorizes and bounds:

- Governance;
- Conformance; and
- Assurance.

Those keystones collectively support the governed framework and maintained product.

The authority topology is:

**repo/**  
→ Framework Contract  
→ Governance / Conformance / Assurance  
→ governed framework and maintained product

Implementation does not acquire authority merely because it exists.

## Framework Authority

Framework authority is accepted normative authority that defines the repository framework.

Accepted repository-framework normative authority shall reside within `repo/`.

Framework authority may define:

- authority relationships;
- framework structure;
- artifact roles;
- keystone powers;
- provenance obligations;
- framework/product relationships; and
- framework evolution constraints.

Implementation may realize framework authority but shall not independently establish, extend, or amend it.

Normative authority shall not arise solely from:

- implementation behavior;
- validation behavior;
- review findings;
- generated artifacts;
- workflow convention;
- historical repository state; or
- product behavior.

## Framework Contract

The Framework Contract defines the foundational authority topology of the repository framework.

It shall establish:

- `repo/` as the authoritative framework namespace;
- Governance, Conformance, and Assurance as the three authority-bearing keystones;
- the authority delegated to each keystone;
- the authority prohibited to each keystone;
- the separation of keystone responsibilities;
- the permitted direction of normative authority flow;
- foundational provenance obligations;
- the prohibition against implicit authority creation;
- the relationship between framework authority and product authority; and
- requirements for explicit, resolvable authority representation;
- default-deny authorization of maintained governed state;
- single controlling semantic ownership; and
- acyclic normative authority dependency.

The Framework Contract shall remain intentionally compact.

It shall define authority and boundaries rather than detailed operating mechanics.

Subordinate framework specifications shall define how the keystones perform their authorized responsibilities.

## Authority-Bearing Keystones

The repository framework shall define exactly three authority-bearing keystones:

1. Governance
2. Conformance
3. Assurance

Supporting mechanisms may exist.

Supporting mechanisms shall operate only under authority delegated through accepted repository-framework authority.

A supporting mechanism shall not independently acquire authority equivalent to a keystone.

## Governance

Governance is the framework mechanism responsible for persistent normative change.

Governance answers:

**What accepted normative authority may be created, changed, superseded, or withdrawn?**

Governance may:

- create or change accepted framework authority;
- create or change accepted product authority; and
- consume Conformance or Assurance findings when persistent normative change is required.

Governance shall not:

- derive normative authority from implementation behavior;
- derive normative authority from validation behavior;
- treat Assurance findings as persistent normative authority without governed acceptance; or
- substitute workflow completion for required Conformance or Assurance.

Persistent changes to accepted normative authority shall occur only through Governance.

Because repository-framework authority is normative authority, persistent changes to the Framework Contract or keystone authority are themselves subject to Governance.

Detailed Governance lifecycle, stage, artifact, transition, and acceptance mechanics belong in the Governance Architecture Proposal.

## Conformance

Conformance is the framework mechanism responsible for mechanical enforcement of accepted normative authority.

Conformance answers:

**Does observable state satisfy the mechanically decidable obligations established by accepted normative authority?**

Conformance may:

- mechanically evaluate observable state;
- reject mechanically nonconforming state; and
- produce mechanical findings and evidence.

Conformance shall not:

- create normative requirements;
- extend accepted normative semantics;
- convert implementation preference into normative enforcement;
- infer normative authority from historical behavior; or
- claim semantic certainty where mechanical evaluation cannot decide the matter.

Mechanical enforcement of accepted normative authority shall occur only through Conformance.

Detailed validation hierarchy, packages, primitives, tests, fixtures, runners, evidence, correspondence, and enforcement-provenance mechanics belong in the Conformance Architecture Proposal.

## Assurance

Assurance is the framework mechanism responsible for governed semantic review and case-specific semantic judgment.

Assurance answers:

**Is the authority, realization, evidence, or application under review semantically adequate and sufficiently justified?**

Assurance may:

- evaluate semantic properties that Conformance cannot decide;
- evaluate the sufficiency of evidence;
- identify ambiguity, contradiction, omission, or inappropriate interpretation; and
- issue case-specific semantic findings.

Assurance shall not:

- create persistent normative authority;
- amend accepted normative authority;
- extend accepted normative semantics through review;
- replace Governance as the mechanism for persistent normative change; or
- replace Conformance for mechanically decidable enforcement.

Governed semantic review and case-specific semantic judgment shall occur only through Assurance.

An Assurance finding may affect disposition of the specific case under review where authorized by accepted framework authority.

An Assurance finding shall not independently create or amend persistent normative authority.

A finding that requires persistent normative change shall return through Governance.

Detailed Assurance artifacts, reviewer roles, finding taxonomy, interpretation rules, review lifecycle, evidence requirements, and adjudication mechanics belong in the Assurance Architecture Proposal.

## Keystone Separation

Each keystone has one primary authority domain.

| Keystone | Authority Domain |
| --- | --- |
| Governance | persistent normative change |
| Conformance | mechanical normative enforcement |
| Assurance | governed semantic review and case-specific judgment |

A keystone shall exercise only authority delegated by accepted repository-framework authority.

A keystone shall not independently exercise authority reserved to another keystone.

A supporting mechanism shall not bypass keystone separation by exercising equivalent authority under another name.

## Authority Flow

Normative authority flows through the framework as follows:

**Framework Contract**  
→ delegates authority to Governance, Conformance, and Assurance

**Governance**  
→ creates or changes accepted normative authority

**Accepted normative authority**  
→ governs realization  
→ authorizes mechanical Conformance  
→ provides the semantic basis for Assurance

**Conformance**  
→ produces mechanical findings and evidence

**Assurance**  
→ produces semantic findings

**Persistent normative change**  
→ returns through Governance

Authority flow and implementation dependency flow are distinct.

Implementation structure shall not obscure, replace, or invert normative authority.

## Authority Inversion

Authority inversion occurs when a subordinate or derived artifact or mechanism is treated as normative authority without Governance having established that authority.

The framework shall prohibit the following authority inversions:

**implementation behavior → normative authority**

**validation behavior → normative authority**

**review finding → persistent normative authority**

**generated artifact → normative authority**

**workflow convention → normative authority**

**historical repository state → normative authority**

**product behavior → framework authority**

Existing behavior may be incorporated into normative authority only through Governance.

Historical or bootstrap behavior shall not become normative solely because preserving it is convenient.

## Framework Authority and Product Authority

Framework authority and product authority are distinct.

Framework authority defines how the repository framework operates.

Product authority defines accepted normative semantics for the maintained product.

Framework authority defines how product authority is:

- created or changed;
- mechanically enforced;
- semantically reviewed; and
- related to product realization.

Neither product authority nor product implementation shall independently define or amend repository-framework authority.

Product implementation remains subordinate to applicable framework authority and product authority.

## Provenance

Every maintained derived framework primitive shall resolve to accepted normative authority that authorizes its existence or use.

For a derived framework primitive, it shall be possible to determine:

- that the primitive is derived rather than normative;
- which accepted normative authority authorizes it; and
- which keystone responsibility it serves.

The absence of resolvable provenance shall be treated as a framework defect.

Missing provenance shall not permit authority to be inferred from implementation, convention, or historical behavior.

Detailed primitive identity, provenance representation, and correspondence mechanics belong in subordinate framework specifications.

## Explicit Authority Representation

Accepted repository-framework authority shall have stable machine-resolvable identities.

Delegated authority relationships shall be resolvable without inference from non-authoritative repository state.

A human or automated consumer shall not be required to infer authority from:

- implementation behavior;
- file proximity;
- historical convention;
- generated output;
- reviewer preference; or
- other non-authoritative context.

Automated tooling and AI agents are subject to the same authority boundaries as human contributors.

The ability to inspect or modify repository state does not grant additional authority.

## Framework Contract and Keystone Specifications

The Framework Contract defines:

- framework authority;
- keystone delegation;
- authority boundaries;
- authority flow;
- provenance obligations;
- framework/product authority separation; and
- explicit authority representation.

The Governance Architecture Proposal shall define how persistent normative change operates.

The Conformance Architecture Proposal shall define how mechanical normative enforcement operates.

The Assurance Architecture Proposal shall define how governed semantic review operates.

A subordinate framework specification shall not redefine or exceed authority delegated by the Framework Contract.

Maintained governed framework state shall require accepted authorization or an explicitly governed extension point.

Each independently governed framework semantic invariant shall have one controlling normative owner.

Normative authority shall not depend for its authority on a cycle of normative dependencies.

## Candidate Foundational Requirements

The following candidate requirements are intended for Design-stage normalization.

### FC-01 — Framework Authority Location

**Accepted repository-framework normative authority SHALL reside within `repo/`.**

### FC-02 — Framework Contract Role

**The Framework Contract SHALL define the foundational authority topology of the repository framework.**

### FC-03 — Keystone Set

**The repository framework SHALL define Governance, Conformance, and Assurance as its three authority-bearing keystones.**

### FC-04 — Delegated Authority

**A keystone SHALL exercise only authority delegated by accepted repository-framework authority.**

### FC-05 — Governance Exclusivity

**Persistent changes to accepted normative authority SHALL occur only through Governance.**

### FC-06 — Conformance Exclusivity

**Mechanical enforcement of accepted normative authority SHALL occur only through Conformance.**

### FC-07 — Assurance Exclusivity

**Governed semantic review and case-specific semantic judgment SHALL occur only through Assurance.**

### FC-08 — Assurance Persistence Boundary

**An Assurance finding SHALL NOT independently create or amend persistent normative authority.**

### FC-09 — Keystone Separation

**A keystone SHALL NOT independently exercise authority reserved to another keystone.**

### FC-10 — Derived Provenance

**Every maintained derived framework primitive SHALL resolve to accepted normative authority that authorizes its existence or use.**

### FC-11 — No Implicit Authority

**Normative authority SHALL NOT arise solely from the existence or behavior of a non-normative repository artifact or mechanism.**

### FC-12 — Product Subordination

**Neither product authority nor product implementation SHALL independently define or amend repository-framework authority.**

### FC-13 — Authority Identity

**Accepted repository-framework authority SHALL have stable machine-resolvable identities.**

### FC-14 — Delegation Resolution

**Delegated authority relationships SHALL be resolvable without inference from non-authoritative repository state.**

### FC-15 — Default-Deny Maintained State

**Maintained governed framework state SHALL require accepted authorization or an explicitly governed extension point.**

### FC-16 — Single Semantic Owner

**Each independently governed framework semantic invariant SHALL have one controlling normative owner.**

### FC-17 — Acyclic Normative Dependency

**Normative authority SHALL NOT depend for its authority on a cycle of normative dependencies.**

## Primary Design Invariant

**The authoritative `repo/` framework SHALL define and bound Governance, Conformance, and Assurance such that persistent normative authority changes only through Governance, mechanical normative enforcement occurs only through Conformance, governed semantic review occurs only through Assurance, maintained governed state is positively authorized, each independently governed semantic invariant has one controlling normative owner, normative authority does not depend on circular normative dependencies, and derived framework behavior remains subordinate and traceable to accepted normative authority.**

All subordinate framework design shall preserve this invariant.

## Audit Questions

The current repository should be audited against this proposal by determining:

1. Which current `repo/` specifications already express candidate Framework Contract authority.

2. Which framework semantics exist only in implementation, validation, workflow automation, review behavior, generated artifacts, or historical convention.

3. Which existing normative requirements combine Framework Contract concerns with Governance, Conformance, Assurance, or product-specific mechanics.

4. Which current authority relationships permit authority inversion.

5. Which current mechanisms exercise authority reserved to another keystone.

6. Which artifacts or behaviors function as de facto normative authority without an accepted normative owner.

7. Which derived framework primitives lack resolvable provenance to accepted normative authority.

8. Which product authority or implementation improperly defines framework authority.

9. Which current normative requirements are too compound, ambiguous, or implementation-specific to serve as clean authority anchors.

10. Which current framework behaviors represent intended target semantics and which represent bootstrap or historical behavior.

11. Whether each candidate foundational requirement represents one independently identifiable obligation.

12. Whether any candidate foundational requirement duplicates or logically subsumes another.

13. Which candidate foundational requirements are mechanically enforceable through Conformance.

14. Which candidate foundational requirements require Assurance.

15. What minimum Framework Contract authority must be accepted before Governance, Conformance, and Assurance can be normalized without circular authority.

## Explicitly Deferred Concerns

The following concerns are intentionally outside the Framework Contract:

- detailed normative-requirement quality rules;
- Governance lifecycle details;
- Design, Plan, and Build stage mechanics;
- governed-work issue structure;
- Conformance hierarchy details;
- validation package design;
- validation primitive taxonomy;
- test and fixture architecture;
- Assurance review mechanics;
- reviewer assignment;
- finding taxonomy;
- migration mechanics;
- bootstrap accommodations; and
- successor-generation construction mechanics.

These concerns may be governed by subordinate framework authority but shall remain consistent with the Framework Contract.

## Follow-On Design Proposals

This proposal establishes the authority boundaries for three follow-on proposals:

1. Governance Architecture Proposal
2. Conformance Architecture Proposal
3. Assurance Architecture Proposal

Those proposals shall not assume authority that the Framework Contract does not delegate.

The Framework Contract should therefore be normalized before the keystone architectures are accepted.
