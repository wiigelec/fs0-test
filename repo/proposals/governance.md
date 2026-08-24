# Governance Architecture Proposal

## Status

Design proposal for audit against the current repository.

This document is non-authoritative.

Its purpose is to define a candidate Governance architecture subordinate to the Framework Contract.

Governance is responsible for persistent normative change and for the controlled progression from design intent to accepted repository state.

This proposal does not define mechanical enforcement or semantic review. Those responsibilities belong to Conformance and Assurance.

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

Governance shall not assume authority beyond that delegated by the Framework Contract.

## Objective

Governance shall provide one controlled lifecycle through which detailed non-authoritative design intent becomes accepted repository state.

The primary Governance lifecycle shall be:

**Design Proposal**  
→ **Design**  
→ **Plan**  
→ **Build**

The Design Proposal is the non-authoritative entry point.

Design, Plan, and Build are distinct governed stages.

Their responsibilities are:

**Design determines what shall become accepted normative authority.**

**Plan determines how accepted normative authority shall be realized.**

**Build realizes the accepted Plan into repository state.**

A downstream stage shall not repair an upstream defect by inventing missing authority.

## Governance Boundary

Governance owns persistent normative change and governed progression between accepted stages.

Governance may:

- receive candidate design intent;
- create or amend accepted normative authority;
- establish accepted realization plans;
- authorize realization work;
- accept governed repository state;
- preserve change lineage;
- supersede or withdraw accepted normative authority;
- consume Conformance findings;
- consume Assurance findings; and
- route defects to the Governance stage responsible for resolving them.

Governance shall not:

- mechanically enforce normative requirements;
- replace Conformance with workflow completion;
- perform semantic review reserved to Assurance;
- treat Assurance findings as persistent normative authority without Governance acceptance;
- infer normative authority from implementation;
- allow Plan to invent missing Design authority;
- allow Build to invent missing Design authority;
- allow Build to invent missing Plan authority; or
- treat a Design Proposal as accepted authority.

## Governance Artifact Model

Governance shall distinguish four primary artifact classes:

1. Design Proposal
2. Design governed work
3. Plan governed work
4. Build governed work

Their roles are distinct.

| Artifact | Governance Role |
| --- | --- |
| Design Proposal | detailed non-authoritative candidate design |
| Design governed work | establishes accepted normative change |
| Plan governed work | establishes accepted realization intent |
| Build governed work | realizes accepted realization intent |

These artifacts shall participate in one resolvable Governance lineage.

## Design Proposal

A Design Proposal is the entry point into the Governance lifecycle.

A Design Proposal may contain:

- problem definition;
- architectural model;
- candidate invariants;
- candidate normative requirements;
- terminology;
- artifact structures;
- schemas;
- examples;
- implementation consequences;
- migration considerations;
- alternatives;
- conflicts;
- audit questions; and
- unresolved design questions.

Detail does not grant authority.

A Design Proposal remains non-authoritative until candidate semantics are accepted through Design.

A Design Proposal shall not itself:

- create accepted normative authority;
- amend accepted normative authority;
- authorize persistent Conformance behavior;
- authorize realization work;
- supersede accepted authority; or
- become normative merely because governed work references it.

## Primary Governance Stages

Governance shall define exactly three primary governed stages:

1. Design
2. Plan
3. Build

Each stage shall be represented by distinct governed work.

The Governance lineage is:

**Design Proposal**  
→ **Design**  
→ **Plan**  
→ **Build**  
→ **accepted repository state**

Each governed stage shall have:

- a stable identity;
- an explicit predecessor;
- a defined responsibility;
- an explicit candidate result;
- defined completion conditions;
- an explicit acceptance decision; and
- resolvable provenance.

## Stage Authority

Each stage owns one Governance responsibility.

### Design

**What normative authority shall change?**

Design owns normative semantics.

### Plan

**How shall accepted normative authority be realized?**

Plan owns realization intent.

### Build

**Has accepted realization intent been realized?**

Build owns realization.

A Governance stage shall not independently exercise the responsibility of another stage.

## Stage Structure

Each primary Governance stage shall contain three substages.

| Stage | Analysis Substage | Production Substage | Decision Substage |
| --- | --- | --- | --- |
| Design | Audit | Normalize | Accept |
| Plan | Analyze | Specify | Accept |
| Build | Implement | Verify | Accept |

These substages are part of the proposed Governance architecture rather than illustrative terminology.

The shared structural pattern is:

1. evaluate authoritative input;
2. produce the stage result; and
3. explicitly accept or reject that result.

The substages have stage-specific semantics and shall not be treated as interchangeable merely because they share a common structure.

## Design

Design transforms non-authoritative design intent into accepted normative change.

Design may consume:

- a Design Proposal;
- accepted normative authority;
- relevant repository state;
- Conformance findings;
- Assurance findings; and
- governed historical context.

The output of Design is an accepted normative delta.

Design shall determine:

- what normative authority is created;
- what normative authority is amended;
- what normative authority is superseded;
- what normative authority is withdrawn;
- what existing authority remains unchanged; and
- what candidate semantics remain unaccepted.

Design shall not define realization details unless those details are intentionally normative.

## Design Audit

Design Audit compares candidate design intent against accepted authority and relevant repository state.

Audit should identify:

- existing authority relevant to the proposal;
- conflicting authority;
- duplicated authority;
- missing authority;
- implementation behavior with no normative owner;
- candidate semantics already expressed elsewhere;
- historical or bootstrap behavior that should not become target semantics;
- cross-keystone responsibility violations; and
- unresolved semantic questions.

Audit produces findings.

Audit findings are not accepted normative authority.

## Design Normalize

Design Normalize converts candidate intent into a coherent proposed normative delta.

Normalization should:

- assign or preserve stable identities;
- separate independent obligations;
- remove duplication;
- distinguish normative semantics from rationale;
- distinguish normative semantics from examples;
- distinguish normative semantics from implementation guidance;
- identify supersession relationships; and
- preserve intended semantic meaning.

Detailed requirement-quality criteria may be established by subordinate Governance, Conformance, or Assurance authority according to their respective responsibilities.

Normalization shall not alter intended semantics merely to simplify implementation or mechanical enforcement.

## Design Accept

Design Accept decides whether the proposed normative delta becomes accepted normative authority.

The accepted Design result shall identify:

- normative authority created;
- normative authority amended;
- normative authority superseded;
- normative authority withdrawn; and
- candidate semantics explicitly left unaccepted.

Only an accepted Design result may establish persistent normative change.

An accepted Design result authorizes Plan.

## Design Output

The authoritative output of Design is the accepted normative delta.

The Design Proposal remains non-authoritative provenance and context.

The Design governed-work artifact remains Governance evidence.

Neither replaces accepted normative authority.

## Plan

Plan transforms accepted Design authority into accepted realization intent.

Plan answers:

**How shall the accepted Design be realized without changing its normative semantics?**

Plan may identify:

- affected artifacts;
- realization work;
- dependency ordering;
- schema changes;
- generated artifacts;
- Conformance work;
- Assurance work;
- cleanup work;
- migration work; and
- expected completion evidence.

Plan shall not create or amend normative semantics.

If planning requires semantic change, work shall return to Design.

## Plan Analyze

Plan Analyze determines the realization impact of accepted Design authority.

Analysis should identify:

- affected normative authority;
- affected implementation;
- affected derived artifacts;
- affected Conformance mechanisms;
- required Assurance work;
- dependencies;
- sequencing constraints;
- obsolete artifacts; and
- realization risks.

Plan analysis shall remain traceable to accepted Design authority.

## Plan Specify

Plan Specify converts impact analysis into candidate realization intent.

The candidate Plan should identify:

- governed work items;
- affected artifact classes or paths where known;
- dependencies;
- sequencing;
- required Conformance changes;
- required Assurance checkpoints;
- removals;
- generated changes; and
- expected completion evidence.

Every governed Plan work item shall resolve to accepted normative authority that requires or authorizes the work.

A Plan shall not contain orphan governed work.

## Plan Accept

Plan Accept decides whether candidate realization intent becomes the accepted Plan.

Plan acceptance shall establish that:

- accepted Design obligations requiring realization are addressed;
- the Plan does not introduce unauthorized semantics;
- dependencies are coherent;
- required Conformance work is identified;
- required Assurance work is identified; and
- Build can proceed without unresolved Design decisions.

An accepted Plan authorizes Build.

## Plan Output

The authoritative Governance output of Plan is accepted realization intent.

The accepted Plan does not become normative framework or product semantics.

It remains subordinate to accepted Design authority.

## Build

Build realizes the accepted Plan.

Build answers:

**Has accepted realization intent been implemented into repository state?**

Build may:

- modify implementation;
- create or modify derived artifacts;
- create or modify Conformance mechanisms where authorized;
- produce Assurance evidence;
- remove superseded implementation; and
- regenerate governed outputs.

Build shall not:

- create normative requirements;
- reinterpret accepted Design;
- expand realization scope without Governance authority;
- omit required Plan work;
- invent mechanical enforcement without accepted normative authority; or
- convert implementation convenience into authority.

## Build Implement

Build Implement performs accepted realization work.

Each governed Build change shall resolve to an accepted Plan work item that authorizes the change.

Implementation may expose upstream defects but shall not silently repair them by creating missing authority.

## Build Verify

Build Verify evaluates the candidate realization against the accepted Plan and applicable accepted authority.

Verification may consume:

- Conformance results;
- Assurance findings;
- generated-output checks;
- provenance checks;
- Plan-completion evidence; and
- repository-state inspection.

Build Verify does not replace Conformance or Assurance.

It consumes their governed outputs where required.

## Build Accept

Build Accept decides whether the candidate realization becomes accepted repository state.

Build acceptance shall require:

- accepted Plan work is complete;
- applicable Conformance obligations are satisfied;
- required Assurance findings are resolved or dispositioned;
- required generated artifacts are current;
- required provenance is complete; and
- no unresolved upstream defect is hidden in Build.

Build acceptance establishes the accepted repository state produced by the Governance lifecycle.

Build acceptance shall not create normative semantics beyond accepted Design authority.

## Stage Acceptance

Acceptance is the common Governance decision that promotes a candidate stage result into the accepted result of that stage.

Acceptance shall be:

- explicit;
- attributable;
- traceable; and
- distinguishable from incidental repository or platform activity.

Acceptance shall not arise solely because:

- code was merged;
- an issue was closed;
- Conformance passed;
- review approval was recorded;
- an AI agent declared completion; or
- downstream activity began.

Conformance or Assurance evidence may be required for acceptance without themselves constituting Governance acceptance.

The consequence of acceptance depends on the stage:

| Stage | Acceptance Consequence |
| --- | --- |
| Design | candidate normative delta becomes accepted normative authority |
| Plan | candidate realization intent becomes the accepted Plan and authorizes Build |
| Build | candidate realization becomes accepted repository state |

## Stage Rejection

A Governance stage may reject its candidate result.

Rejection shall preserve:

- the rejected candidate;
- the reason for rejection; and
- provenance to the governed work.

Rejected semantics, realization intent, or realization shall not become accepted merely because downstream artifacts or implementation exist.

## Feedback Routing

Governance shall route defects to the stage responsible for the defective responsibility.

### Design Routing

Work shall return to Design when:

- accepted normative authority is ambiguous;
- accepted normative authority is contradictory;
- required semantics are missing;
- a new semantic choice is required; or
- accepted semantics require amendment.

### Plan Routing

Work shall return to Plan when:

- realization work is missing;
- dependency analysis is incomplete;
- sequencing is incorrect;
- realization strategy must change; and
- accepted normative semantics do not need to change.

### Build Routing

Work shall remain in Build when:

- implementation is incorrect;
- accepted Plan work is incomplete;
- generated artifacts are stale;
- implementation cleanup remains;
- required evidence has not been produced; and
- neither Design nor Plan must change.

The governing routing rule is:

**Semantic defect → Design**

**Realization-intent defect → Plan**

**Realization defect → Build**

## No Downstream Invention

A downstream Governance stage shall not create authority required from an upstream stage.

Plan shall not create normative semantics missing from Design.

Build shall not create normative semantics missing from Design.

Build shall not create realization intent missing from Plan.

Downstream discovery of an upstream defect shall cause backward routing rather than local invention.

## Governance Provenance

A completed Governance lifecycle shall preserve a resolvable lineage:

**Design Proposal**  
→ **Design governed work**  
→ **accepted normative delta**  
→ **Plan governed work**  
→ **accepted realization intent**  
→ **Build governed work**  
→ **accepted repository state**

The lineage shall make it possible to determine:

- why a change exists;
- what proposal initiated it;
- what normative authority changed;
- what accepted Plan authorized realization;
- what Build realized that Plan; and
- what Conformance and Assurance evidence supported acceptance.

## Governed Work Provenance

Governed work shall not exist without resolvable authority.

Each governed Plan work item shall resolve to accepted normative authority that requires or authorizes it.

Each governed Build change shall resolve to an accepted Plan work item that authorizes the change.

The exact provenance representation belongs in detailed Governance authority.

## Normative Requirement Identity

Accepted normative obligations shall be represented by stable machine-resolvable normative requirement identities.

The normative requirement is the canonical addressable unit of accepted normative semantics.

A normative obligation shall not remain accepted only as unidentified prose that escapes Conformance and Assurance correspondence.

## Governed Identity

Governance artifacts participating in authoritative lineage shall have stable identities.

At minimum, identity shall exist for:

- Design Proposal;
- Design governed work;
- accepted Design result;
- Plan governed work;
- accepted Plan result;
- Build governed work; and
- accepted Build result.

The exact identity representation belongs in detailed Governance authority.

## Evaluation Disposition

Each accepted normative requirement shall have governed Conformance and Assurance applicability.

A requirement for which Conformance applicability is `none` and Assurance applicability is `none` shall have a governed rationale explaining why neither keystone directly evaluates that requirement.

Governance owns acceptance of this cross-keystone disposition.

Neither Conformance nor Assurance shall independently determine the responsibility of the other keystone.

## Acceptance Authority

Governance acceptance shall depend only on authority accepted before the candidate result acquires the authority produced by that acceptance.

A candidate authority shall not require itself, or authority that exists only because that candidate has already been accepted, as a prerequisite for its own acceptance.

This prevents circular self-authorization during framework evolution and self-hosting.

## Governed State

Governance state shall be explicitly represented.

Governed authorization shall be bounded to explicitly governed scope.

A governed work item shall not independently authorize unrelated or successor work merely because the current work is accepted or complete.

A governed-work artifact shall not rely solely on surrounding platform state to determine its Governance state.

Detailed state vocabulary and transition rules belong in subordinate Governance authority.

## Authority Lifecycle

Governance shall support persistent normative-authority lifecycle operations including:

- creation;
- amendment;
- supersession; and
- withdrawal.

Superseded or withdrawn normative authority shall remain historically resolvable.

A normative identity shall not be reused in a manner that obscures previously accepted authority.

Authority lifecycle operations shall preserve lineage to the Governance work that authorized them.

## Relationship to Conformance

Governance may require Conformance evidence for stage acceptance.

Governance shall not define mechanical enforcement semantics merely because it requires such evidence.

Conformance remains responsible for mechanically evaluating observable state against accepted normative authority.

Passing Conformance does not create normative authority or constitute Governance acceptance.

## Relationship to Assurance

Governance may require Assurance findings for stage acceptance.

Assurance may identify:

- ambiguity;
- contradiction;
- semantic insufficiency;
- evidence insufficiency; and
- case-specific semantic conclusions.

Governance remains responsible for persistent normative change.

An Assurance finding requiring persistent semantic change shall route to Design.

An Assurance finding does not itself constitute Governance acceptance.

## Human and Automated Actors

Governance may be performed by humans, automated tooling, AI agents, or combinations of them where authorized.

Actor capability does not determine authority.

Authority derives from accepted Governance rules.

The ability to inspect, modify, merge, close, approve, or otherwise manipulate repository or platform state does not independently grant Governance authority.

## Candidate Governance Requirements

The following candidate requirements are intended for Design-stage normalization.

### GOV-01 — Governance Lifecycle

**Governance SHALL define Design, Plan, and Build as its three primary governed stages.**

### GOV-02 — Design Proposal Entry

**A Governance lifecycle SHALL originate from a non-authoritative Design Proposal.**

### GOV-03 — Distinct Governed Work

**Design, Plan, and Build SHALL each be represented by distinct governed work.**

### GOV-04 — Stage Lineage

**Each governed stage SHALL resolve to the predecessor artifact or accepted result that authorizes it.**

### GOV-05 — Design Authority

**Design SHALL be the Governance stage responsible for creating or changing accepted normative authority.**

### GOV-06 — Plan Authority

**Plan SHALL be the Governance stage responsible for establishing realization intent for accepted Design authority.**

### GOV-07 — Plan Semantic Boundary

**Plan SHALL NOT independently create or amend normative semantics.**

### GOV-08 — Build Authority

**Build SHALL be the Governance stage responsible for realizing the accepted Plan.**

### GOV-09 — Build Semantic Boundary

**Build SHALL NOT independently create or amend normative semantics.**

### GOV-10 — Stage Separation

**A Governance stage SHALL NOT independently exercise authority assigned to another Governance stage.**

### GOV-11 — Explicit Stage Acceptance

**A governed stage result SHALL NOT become accepted until explicitly accepted through Governance.**

### GOV-12 — Acceptance Independence

**Governance acceptance SHALL NOT arise solely from incidental repository or platform activity.**

### GOV-13 — Acceptance Consequence

**Acceptance SHALL promote only the candidate result belonging to the governed stage in which acceptance occurs.**

### GOV-14 — Semantic Defect Routing

**A defect requiring persistent normative semantic change SHALL route to Design.**

### GOV-15 — Plan Defect Routing

**A defect requiring realization-intent change without normative semantic change SHALL route to Plan.**

### GOV-16 — No Downstream Invention

**A downstream Governance stage SHALL NOT create authority required from an upstream Governance stage.**

### GOV-17 — Governance Lineage

**A completed Governance lifecycle SHALL preserve resolvable provenance from Design Proposal through Design, Plan, Build, and accepted repository state.**

### GOV-18 — Governed Work Provenance

**Each governed realization work item SHALL resolve to accepted authority that requires or authorizes the work.**

### GOV-19 — Design Delta

**An accepted Design result SHALL identify the normative authority created, amended, superseded, or withdrawn.**

### GOV-20 — Plan Coverage

**An accepted Plan SHALL address each accepted Design obligation that requires governed realization work.**

### GOV-21 — Explicit Governed State

**Governed-work state SHALL be explicitly represented rather than inferred solely from surrounding repository or platform state.**

### GOV-22 — Authority Lifecycle

**Governance SHALL support creation, amendment, supersession, and withdrawal of accepted normative authority.**

### GOV-23 — Historical Resolution

**Superseded or withdrawn normative authority SHALL remain historically resolvable.**

### GOV-24 — Identity Preservation

**A normative identity SHALL NOT be reused in a manner that obscures previously accepted authority.**

### GOV-25 — Normative Requirement Identity

**Each accepted normative obligation SHALL be represented by a stable machine-resolvable normative requirement identity.**

### GOV-26 — Evaluation Disposition

**Each accepted normative requirement SHALL have governed Conformance and Assurance applicability, and a requirement with neither mechanical Conformance nor required Assurance SHALL have a governed rationale.**

### GOV-27 — Acceptance Authority

**Governance acceptance SHALL depend only on authority accepted before the candidate result acquires the authority produced by that acceptance.**

### GOV-28 — Bounded Governed Authorization

**A governed work item SHALL authorize only its explicitly governed scope and SHALL NOT independently authorize unrelated or successor work.**

## Primary Design Invariant

**Governance SHALL transform non-authoritative design intent into accepted repository state through a traceable Design → Plan → Build lifecycle in which accepted normative obligations have stable requirement identities and governed evaluation dispositions, Design owns normative semantics, Plan owns realization intent, Build realizes only accepted Plan work, governed authorization remains bounded to explicit scope, acceptance is explicit and depends only on previously accepted authority, and downstream stages route upstream defects rather than invent missing authority.**

All detailed Governance design shall preserve this invariant.

## Audit Questions

The current repository should be audited against this proposal by determining:

1. Which current workflows already perform Design, Plan, or Build responsibilities.

2. Which workflows combine multiple Governance stages into one governed artifact.

3. Which current mechanisms allow implementation to create de facto normative semantics.

4. Which current artifacts function as accepted authority without explicit Governance acceptance.

5. Which Plan or Build work lacks provenance to accepted authority.

6. Which processes treat merge, issue closure, Conformance success, review approval, or downstream activity as implicit acceptance.

7. Which normative changes bypass distinct Design governed work.

8. Which Build activities require unresolved semantic decisions that belong in Design.

9. Which Plan activities create semantics not accepted by Design.

10. Which defects are currently repaired downstream rather than routed to the stage that owns them.

11. Which accepted Designs lack complete realization coverage in Plan.

12. Which superseded or withdrawn authority is not historically resolvable.

13. Which governed state is inferred from GitHub platform state rather than explicitly represented.

14. Whether the Audit / Normalize / Accept Design structure cleanly separates semantic discovery, normative production, and acceptance.

15. Whether the Analyze / Specify / Accept Plan structure cleanly separates impact analysis, realization planning, and acceptance.

16. Whether the Implement / Verify / Accept Build structure cleanly separates realization, evidence evaluation, and acceptance.

17. Whether each candidate GOV requirement represents one independently identifiable obligation.

18. Whether any candidate GOV requirement duplicates or logically follows from another.

19. Which GOV requirements are mechanically enforceable through Conformance.

20. Which GOV requirements require Assurance.

21. What minimum Governance authority must be accepted before Conformance and Assurance lifecycle integration can be normalized.

## Explicitly Deferred Concerns

The following concerns are intentionally outside this Governance proposal:

- exact GitHub issue schema;
- exact issue labels;
- detailed governed-state vocabulary;
- exact transition syntax;
- exact acceptance actor model;
- exact approval cardinality;
- detailed normative-requirement quality criteria;
- exact Conformance implementation;
- exact Assurance implementation;
- validation package architecture;
- review finding schema;
- implementation-language choices;
- migration execution details; and
- bootstrap sequencing.

These concerns may be defined by subordinate Governance authority or by Conformance and Assurance according to their delegated responsibilities.

## Relationship to Conformance and Assurance

The Conformance Architecture Proposal shall define how objective mechanical enforcement operates under accepted normative authority.

The Assurance Architecture Proposal shall define how governed semantic review and case-specific judgment operate under accepted normative authority.

Governance may consume outputs from both keystones but shall not absorb their responsibilities.

The Governance architecture should be normalized before lifecycle coupling to Conformance and Assurance is accepted.
