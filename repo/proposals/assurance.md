# Assurance Architecture Proposal

## Status

Design proposal for audit against the current repository.

This document is non-authoritative.

Its purpose is to define a candidate Assurance architecture subordinate to the Framework Contract and compatible with the proposed Governance and Conformance architectures.

Assurance is responsible for governed semantic review and case-specific semantic judgment where mechanical Conformance alone cannot establish meaning, adequacy, or sufficiency.

This proposal does not define persistent normative change or mechanical enforcement.

Persistent normative change belongs to Governance.

Mechanical enforcement belongs to Conformance.

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

Assurance shall not assume authority beyond that delegated by the Framework Contract.

## Governance Basis

This proposal assumes the Governance lifecycle:

**Design Proposal**  
→ **Design**  
→ **Plan**  
→ **Build**

Governance owns persistent normative change.

Assurance may provide semantic findings to Governance where accepted Governance authority requires review.

An Assurance finding does not itself create or amend persistent normative authority.

A persistent semantic correction identified through Assurance shall route through Governance Design.

## Conformance Basis

Conformance mechanically evaluates objectively decidable obligations.

Conformance may provide Assurance with:

- mechanical findings;
- correspondence;
- assertion identities;
- evidence;
- closure results; and
- observed state.

Assurance may evaluate the semantic adequacy of those results.

Assurance shall not replace Conformance for mechanically decidable enforcement.

## Objective

Assurance shall provide one governed semantic-review architecture in which:

- every governed semantic review derives from accepted authority;
- review responsibility is explicit;
- review scope is explicit;
- evidence is identifiable;
- findings are attributable and traceable;
- interpretation remains within accepted normative semantics;
- semantic judgment remains bounded to the reviewed case;
- ambiguity and insufficiency are exposed rather than silently converted into persistent semantics; and
- persistent semantic change returns through Governance.

The primary relationship is:

**accepted normative authority**  
→ **canonical Assurance correspondence**  
→ **review obligation**  
→ **review case**  
→ **evidence**  
→ **finding**  
→ **case disposition or Governance routing**

## Assurance Boundary

Assurance owns governed semantic review and case-specific semantic judgment.

Assurance may:

- evaluate semantic clarity;
- evaluate normative requirement quality;
- identify ambiguity;
- identify contradiction;
- identify omission;
- identify overlap;
- identify inappropriate implementation leakage;
- evaluate evidence sufficiency;
- evaluate Conformance interpretation;
- evaluate realization fidelity;
- issue case-specific findings; and
- identify defects requiring Governance action.

Assurance shall not:

- create persistent normative authority;
- amend accepted normative authority;
- extend or narrow accepted normative semantics;
- convert reviewer preference into authority;
- mechanically enforce obligations reserved to Conformance;
- redefine Conformance predicates directly;
- redefine Governance authority; or
- convert prior findings into persistent precedent without accepted authority.

## Assurance Terminology

### Assurance Primitive

A maintained artifact whose purpose participates in governed semantic review.

Assurance primitives may include:

- Assurance correspondence;
- review obligations;
- review cases;
- evidence manifests;
- reviewer instructions;
- rubrics;
- findings;
- dispositions;
- semantic checklists;
- Assurance schemas; and
- generated Assurance views.

### Assurance Correspondence

The governed relationship between accepted authority and Assurance responsibility.

Assurance correspondence identifies whether semantic-review responsibility exists and, where applicable, the review obligations derived from that authority.

Correspondence does not independently own normative semantics.

### Review Obligation

An independently identifiable semantic-review responsibility derived from accepted authority.

A review obligation defines why governed semantic review is required.

### Review Case

A bounded invocation of one or more review obligations against identified subject matter and evidence.

A review case provides the context within which Assurance judgment is valid.

### Evidence

Information considered by Assurance in a review case.

Evidence may include:

- accepted normative authority;
- Governance artifacts;
- Conformance findings;
- Conformance correspondence;
- implementation;
- repository state;
- generated artifacts;
- historical provenance; and
- prior Assurance findings.

Evidence does not acquire normative authority merely because it is considered during review.

### Finding

A governed semantic conclusion produced for a review case.

A finding remains bounded to that case unless persistent semantics are subsequently established through Governance.

## Closed Assurance Hierarchy

Governed semantic review shall occur only through the authorized Assurance hierarchy.

A maintained artifact whose purpose participates in governed semantic review shall participate in that hierarchy.

Applicable artifacts may include:

- Assurance correspondence;
- review obligations;
- review cases;
- evidence manifests;
- reviewer instructions;
- rubrics;
- findings;
- dispositions;
- semantic checklists;
- Assurance schemas; and
- generated Assurance views.

Artifacts outside the governed Assurance hierarchy shall not independently produce governed Assurance findings.

General analysis may inform Assurance.

It does not acquire Assurance authority merely because it exists.

## Purpose of the Closed Hierarchy

The closed Assurance hierarchy is an authority-control mechanism.

It prevents:

- reviewer preference becoming policy;
- AI interpretation becoming implicit authority;
- findings with no normative basis;
- reviews with undefined scope;
- findings disconnected from evidence;
- findings disconnected from authority;
- repeated conclusions becoming undeclared precedent;
- ad hoc semantic gates; and
- semantic obligations hidden outside governed review structure.

The expected relationship is:

**accepted authority**  
→ **canonical Assurance correspondence**  
→ **review obligation**  
→ **review case**  
→ **evidence**  
→ **finding**

## Canonical Assurance Correspondence

Each active normative requirement shall have exactly one canonical Assurance correspondence record.

The correspondence shall identify:

- normative requirement identity;
- Assurance applicability; and
- applicable review obligations where Assurance is required.

The correspondence record shall not restate normative requirement semantics as independent authority.

## Assurance Applicability

Each active normative requirement shall have exactly one canonical Assurance applicability determination.

The candidate vocabulary is:

### `required`

The normative requirement has governed semantic-review responsibility.

At least one review obligation shall exist.

### `none`

No Assurance responsibility exists for the normative requirement under accepted authority.

A rationale may be required where absence of Assurance responsibility is not self-evident.

Assurance applicability describes only Assurance responsibility.

It does not encode Conformance responsibility.

## Cross-Keystone Applicability

Conformance and Assurance applicability are independent dimensions.

A requirement may therefore be:

| Conformance | Assurance | Meaning |
| --- | --- | --- |
| mechanical | none | mechanical enforcement only |
| none | required | semantic review only |
| mechanical | required | both mechanical and semantic responsibility |
| none | none | neither keystone directly evaluates the requirement |

The final combination should be explicitly justified where meaningful enforcement or review might otherwise be expected.

This model replaces overloaded concepts such as `partial` or `semantic-review` dispositions spanning multiple keystones.

## Review Obligation Model

A review obligation represents one independently identifiable semantic-review responsibility.

Examples may include:

- ambiguity review;
- requirement-quality review;
- Conformance-applicability review;
- assertion-interpretation review;
- evidence-sufficiency review;
- realization-fidelity review;
- conflict review; and
- Governance-stage review.

A normative requirement or other accepted framework authority may derive multiple review obligations.

Review-obligation identity is distinct from:

- normative requirement identity;
- review-case identity;
- reviewer identity; and
- finding identity.

## Review Obligation Authority

Every maintained review obligation shall resolve to accepted authority requiring or authorizing the review.

Assurance shall not create mandatory semantic-review obligations merely because additional review appears useful.

Exploratory analysis may occur without becoming governed Assurance responsibility.

## Assurance Provenance

Every maintained Assurance primitive shall resolve through governed provenance to accepted authority.

The provenance chain shall permit resolution of:

**accepted authority**  
→ **review obligation**  
→ **review case**  
→ **finding**

Evidence used by a finding shall also be identifiable.

No orphan Assurance finding is permitted.

## Review Case Identity

Each governed Assurance review case shall have a stable unique identity.

Case identity shall be distinct from:

- normative requirement identity;
- review-obligation identity;
- reviewer identity; and
- finding identity.

This permits repeated reviews against the same authority without conflating their conclusions.

## Review Scope

Every review case shall explicitly define its scope.

A review case shall distinguish:

- **authorizing authority** — accepted authority that requires or permits Assurance to perform the review; and
- **review subject** — the candidate authority, accepted authority, Governance artifact, Conformance artifact, implementation, repository state, or other material being evaluated.

This distinction permits Assurance to review non-authoritative candidates without allowing the candidate to authorize its own review.

Scope shall identify, as applicable:

- authorizing authority;
- reviewed subject matter;
- review obligations being exercised;
- Governance artifact or stage under review;
- Conformance correspondence or assertions under review;
- implementation or repository state under review;
- relevant evidence; and
- relevant exclusions.

A finding shall not silently claim semantic effect outside the defined review scope.

## Finding Identity

Each maintained Assurance finding shall have a stable identity within its review case.

A finding identity shall not be reused for an unrelated conclusion.

Findings participating in Governance lineage or later evidence shall remain historically resolvable.

## Finding Traceability

Each Assurance finding shall resolve to:

- its review case;
- applicable review obligation;
- authorizing authority;
- reviewed subject matter; and
- evidence basis.

A finding should distinguish:

- observation;
- semantic analysis;
- conclusion; and
- recommended action.

The exact representation belongs in subordinate Assurance authority.

## Review Execution Closure

A review obligation may exist without being continuously active.

When accepted authority triggers a review obligation for a governed decision, that obligation shall be realized by a governed review case before the decision may be accepted.

A declared review obligation that is triggered but never instantiated does not satisfy Assurance responsibility.

## Assurance Semantic Boundary

Assurance judgment is bounded to the authorized review case in which it is issued.

An Assurance finding shall not independently:

- create normative authority;
- amend normative authority;
- supersede normative authority;
- withdraw normative authority;
- establish persistent normative semantics beyond the reviewed case; or
- establish persistent precedent.

A case-specific finding may affect disposition of the reviewed case where accepted authority grants that effect.

Persistent semantic effect requires Governance.

## Interpretation Boundary

Assurance may interpret accepted authority when necessary to decide a bounded review case.

Interpretation shall remain anchored to accepted normative semantics.

Assurance shall not independently:

- manufacture missing obligations;
- broaden accepted obligations;
- narrow accepted obligations;
- convert implementation preference into semantics; or
- permanently settle unresolved ambiguity.

Where materially different interpretations remain reasonable, Assurance should identify ambiguity rather than create persistent resolution.

## Governance Routing

A finding requiring persistent normative semantic change shall route through Governance Design.

Examples include:

- ambiguous accepted authority;
- contradictory authority;
- missing normative semantics;
- requirement-quality defects requiring rewritten authority;
- persistent interpretation disputes; and
- desired precedent not already established by accepted authority.

Assurance identifies the semantic defect.

Governance owns its persistent resolution.

## Finding Classes

Assurance may distinguish finding classes such as:

### `satisfied`

The reviewed semantic responsibility is adequately satisfied for the bounded case.

### `concern`

A semantic issue exists but does not necessarily prevent disposition.

### `insufficient`

Available evidence or reasoning is insufficient to establish the required conclusion.

### `ambiguous`

Accepted authority supports materially different relevant interpretations.

### `contradictory`

Applicable accepted authority contains incompatible semantics.

### `defect`

The reviewed realization, correspondence, or interpretation conflicts with accepted authority.

### `governance-required`

Persistent normative action is required before the semantic issue can be properly resolved.

The exact vocabulary belongs in subordinate Assurance design.

## Evidence Sufficiency

Assurance may evaluate whether evidence is semantically sufficient for a governed claim.

Evidence sufficiency is distinct from evidence existence.

Conformance may mechanically determine:

- whether evidence exists;
- whether required evidence categories are present; and
- whether evidence conforms structurally.

Assurance may determine:

- whether evidence meaningfully supports the claimed conclusion;
- whether evidence scope matches the claim;
- whether relevant cases are omitted;
- whether evidence relies on incorrect semantic interpretation; and
- whether the evidence is sufficient for the governed review purpose.

Detailed evidence-sufficiency policies belong in subordinate Assurance authority.

## Normative Requirement Quality

Assurance may evaluate semantic properties of normative requirements that cannot be reliably decided mechanically.

Examples include:

- atomicity;
- clarity;
- ambiguity;
- contradiction;
- overlap;
- duplication;
- inappropriate implementation leakage;
- undefined subjective qualifiers;
- hidden obligations inside rationale; and
- inappropriate coupling of independent obligations.

Assurance findings about requirement quality do not themselves amend the requirement.

Persistent correction occurs through Governance.

## Mechanical Quality and Semantic Quality

Requirement quality spans multiple keystones.

**Governance** owns creation and acceptance of normative authority.

**Conformance** may mechanically enforce objectively decidable structural quality rules.

**Assurance** may evaluate semantic quality requiring judgment.

No keystone gains the authority of another merely because all three participate in requirement quality.

## Conformance Review

Where authorized, Assurance may evaluate whether Conformance faithfully represents accepted normative authority.

Assurance may review:

- Conformance applicability;
- assertion decomposition;
- assertion interpretation;
- evidence sufficiency;
- over-enforcement;
- under-enforcement; and
- claims of mechanical decidability.

Assurance may issue findings about Conformance.

It shall not directly create persistent Conformance semantics.

Persistent correction routes through Governance.

## Realization Fidelity

Where authorized, Assurance may review whether realization faithfully reflects accepted normative intent.

This review may identify semantic defects not completely captured by mechanical assertions.

Examples include:

- semantic omission;
- inappropriate abstraction;
- unintended interpretation;
- misleading derived documentation; and
- mechanically valid but semantically inadequate realization.

Assurance shall not rewrite authority to conform to existing implementation.

## Governance Stage Review

Governance may require Assurance at defined stage gates.

### Design Assurance

May evaluate:

- requirement quality;
- semantic clarity;
- atomicity;
- internal consistency;
- authority boundaries; and
- unresolved ambiguity.

### Plan Assurance

May evaluate:

- fidelity to accepted Design;
- semantic completeness of realization intent;
- inappropriate reinterpretation; and
- adequacy of planned semantic evidence.

### Build Assurance

May evaluate:

- realization fidelity;
- evidence sufficiency;
- semantic fidelity of Conformance; and
- unresolved semantic defects.

Governance decides whether review is required.

Assurance produces the finding.

Governance performs acceptance.

## Reviewer Attribution

Assurance findings shall be attributable to the actor or governed actor class responsible for review.

Reviewers may include:

- humans;
- AI agents;
- automated semantic systems; or
- governed combinations of actors.

Reviewer identity does not create authority.

The reviewer's ability, expertise, confidence, or implementation access does not independently enlarge Assurance authority.

## Human and AI Review

Human and AI reviewers are subject to the same accepted Assurance boundaries.

AI-assisted review may be useful for:

- ambiguity detection;
- requirement-decomposition analysis;
- cross-specification consistency review;
- provenance review;
- evidence analysis; and
- implementation-to-authority comparison.

An AI reviewer shall not:

- treat confidence as authority;
- invent persistent semantics;
- create undeclared precedent;
- infer authority from implementation;
- waive Governance obligations; or
- waive Conformance obligations.

Human reviewers shall not acquire those powers merely through judgment or expertise either.

## Prior Findings

Prior Assurance findings may be evidence in later review cases.

Prior findings are not automatically binding precedent.

Absent accepted authority establishing a precedent model, a prior finding remains a case-specific conclusion.

Repeated identical findings do not independently transform the conclusion into persistent normative authority.

## Conflicting Findings

Multiple Assurance cases may produce materially conflicting findings.

Conflict shall remain explicit until resolved through an authorized governed mechanism.

Assurance shall not hide the conflict by selecting one preferred interpretation as persistent semantics.

If persistent semantic resolution is required, the conflict shall route through Governance.

## Single Assurance Correspondence Authority

Assurance shall define one canonical authority for requirement-to-Assurance correspondence.

Independently maintained mappings shall not be allowed to silently diverge.

Operational representations may exist in:

- correspondence records;
- governed-work metadata;
- review manifests;
- reviewer tooling;
- generated reports; and
- documentation.

Where multiple representations are required, they shall be generated from canonical correspondence or mechanically verified against it.

## Assurance Correspondence Integrity

Canonical Assurance correspondence shall remain consistent with the maintained review-obligation graph.

Examples of defects include:

- `required` applicability with no review obligation;
- review obligation referencing unknown authority;
- review case referencing nonexistent obligations;
- finding with no review case;
- finding with no authority reference; and
- divergent duplicate mappings.

Objectively decidable integrity properties may themselves be mechanically enforced through Conformance.

## Generated Assurance Views

Generated Assurance views may expose:

- normative requirement identity;
- Assurance applicability;
- review obligations;
- review cases;
- findings;
- unresolved ambiguity;
- Governance routing; and
- historical findings.

Generated views remain subordinate derived artifacts.

They do not independently establish semantic authority.

## Assurance Defects

Examples of Assurance defects include:

- review obligation with no accepted authority;
- required review responsibility with no review obligation;
- review case with undefined scope;
- finding without evidence basis;
- finding without accepted authority;
- finding exceeding case scope;
- interpretation extending or narrowing accepted semantics;
- reviewer preference treated as authority;
- repeated findings treated as precedent without authorization;
- semantic review occurring outside the governed hierarchy;
- divergent correspondence mappings; and
- persistent ambiguity being silently resolved without Governance.

An Assurance defect shall not be repaired by inventing normative authority.

## Relationship to Governance

Governance changes accepted normative authority.

Assurance consumes accepted authority and produces semantic findings.

Routing follows the responsibility owning the defect.

### Semantic Authority Defect

**Assurance → Governance Design**

### Realization-Intent Defect

**Assurance → Governance Plan**

when accepted semantics remain sound.

### Realization Defect

**Assurance → Governance Build**

when Design and Plan remain sound.

### Case-Specific Finding

Return to the governed consumer or Governance stage requesting the review.

Governance determines persistent disposition.

## Relationship to Conformance

Conformance establishes mechanically decidable facts.

Assurance evaluates semantic matters requiring judgment.

Assurance may conclude that Conformance:

- faithfully represents authority;
- over-enforces;
- under-enforces;
- incompletely represents authority;
- uses semantically insufficient evidence; or
- claims mechanical determinacy where ambiguity remains.

Assurance shall not directly rewrite persistent Conformance semantics.

Persistent correction routes through Governance.

## Candidate Assurance Requirements

The following candidate requirements are intended for Design-stage normalization.

### ASSUR-01 — Governed Assurance Hierarchy

**Governed semantic review and case-specific semantic judgment SHALL occur only through the authorized Assurance hierarchy.**

### ASSUR-02 — Assurance Provenance

**Every maintained Assurance primitive SHALL resolve through governed provenance to accepted authority.**

### ASSUR-03 — Canonical Assurance Correspondence

**Each active normative requirement SHALL have exactly one canonical Assurance correspondence record.**

### ASSUR-04 — Assurance Applicability

**Each active normative requirement SHALL have exactly one canonical Assurance applicability determination.**

### ASSUR-05 — Required Review Coverage

**Each normative requirement with required Assurance applicability SHALL resolve to at least one governed review obligation.**

### ASSUR-06 — Review Obligation Identity

**Each maintained Assurance review obligation SHALL have a stable unique identity.**

### ASSUR-07 — Review Case Identity

**Each governed Assurance review case SHALL have a stable unique identity.**

### ASSUR-08 — Review Case Scope

**Each governed Assurance review case SHALL explicitly identify its authorizing authority, review obligations, and reviewed subject matter.**

### ASSUR-09 — Finding Identity

**Each maintained Assurance finding SHALL have a stable identity within its review case.**

### ASSUR-10 — Finding Traceability

**Each Assurance finding SHALL resolve to its review case, applicable review obligation, authorizing authority, reviewed subject matter, and evidence basis.**

### ASSUR-11 — Assurance Semantic Boundary

**An Assurance finding SHALL NOT independently create, amend, supersede, withdraw, or establish persistent normative semantics beyond its authorized review case.**

### ASSUR-12 — Governance Routing

**An Assurance finding requiring persistent normative semantic change SHALL route through Governance Design.**

### ASSUR-13 — Interpretation Boundary

**Assurance interpretation SHALL remain within accepted normative semantics and SHALL NOT independently extend or narrow those semantics.**

### ASSUR-14 — Single Correspondence Authority

**Requirement-to-Assurance correspondence SHALL NOT depend on independently maintained mappings that may silently diverge.**

### ASSUR-15 — Review Execution Closure

**Each triggered Assurance review obligation SHALL be realized by a governed review case before the governed decision requiring that review may be accepted.**

## Primary Design Invariant

**Assurance SHALL provide governed semantic review through a closed provenance model in which every maintained Assurance primitive derives from accepted authority, every triggered review obligation is realized by a traceable and explicitly scoped review case, every finding resolves to its authorizing authority, reviewed subject matter, and evidence basis, interpretation remains within accepted normative semantics, findings remain bounded to their authorized cases, and persistent semantic change returns through Governance.**

All detailed Assurance design shall preserve this invariant.

## Audit Questions

The current repository should be audited against this proposal by determining:

1. Which current semantic review practices qualify as Assurance.

2. Which semantic review practices exist only as informal convention.

3. Which active normative requirements require Assurance responsibility.

4. Which active normative requirements have no meaningful Assurance responsibility.

5. Which existing `semantic-review` validation dispositions should become Assurance applicability.

6. Which existing `partial` dispositions should become independent Conformance and Assurance relationships.

7. Which review obligations currently have no accepted authority.

8. Which required Assurance relationships have no identifiable review obligation.

9. Which current reviews lack stable review-case identity.

10. Which review cases lack explicit scope.

11. Which findings lack stable identity.

12. Which findings lack resolvable review obligations.

13. Which findings lack resolvable normative authority.

14. Which findings lack identifiable evidence basis.

15. Which current findings exceed the semantic scope of their review cases.

16. Which reviewer conclusions have become de facto persistent semantics without Governance.

17. Which prior findings are being treated as precedent without accepted precedent authority.

18. Which current semantic interpretations broaden or narrow accepted authority.

19. Which current requirement-quality checks belong to Conformance because they are mechanically decidable.

20. Which requirement-quality checks require Assurance judgment.

21. Which current Conformance applicability decisions require Assurance review.

22. Which current assertions may over-enforce or under-enforce accepted authority.

23. Which mechanically complete evidence sets may remain semantically insufficient.

24. Which Governance stage gates should require Assurance.

25. Which Assurance correspondence mappings are duplicated across metadata, review tooling, templates, or generated documentation.

26. Whether each candidate ASSUR requirement represents one independently identifiable obligation.

27. Whether any candidate ASSUR requirement duplicates or logically follows from another.

28. Which candidate ASSUR requirements can be structurally enforced through Conformance.

29. What minimum Assurance authority must be accepted before Governance may require Assurance at Design, Plan, or Build acceptance.

## Explicitly Deferred Concerns

The following concerns are intentionally outside this Assurance proposal:

- exact Assurance correspondence schema;
- exact review-obligation schema;
- exact review-case schema;
- exact finding schema;
- exact finding vocabulary;
- exact reviewer-assignment rules;
- exact reviewer cardinality;
- exact reviewer-independence rules;
- exact AI/human reviewer composition;
- exact confidence representation;
- exact semantic review rubrics;
- exact evidence-manifest representation;
- exact precedent model;
- exact generated report format;
- migration sequencing from current review practices; and
- bootstrap accommodations.

These concerns may be defined by subordinate Assurance authority during detailed Design and Plan.

## Relationship to the Framework

The proposed framework model is:

**Framework Contract**  
→ defines authority topology

**Governance**  
→ controls persistent normative change

**Conformance**  
→ mechanically enforces accepted normative authority

**Assurance**  
→ performs governed semantic review and case-specific judgment

The three keystones interact without absorbing one another's powers.

Governance changes authority.

Conformance mechanically evaluates authority.

Assurance semantically evaluates authority, realization, and evidence.

Persistent semantic change returns through Governance.
