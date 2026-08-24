# FS0 Operating Substrate

## Status

Part of the non-authoritative FS0-Core Bootstrap Design Proposal.

Read `fs0-design.md` first. This chunk does not independently create authority.

---

# Bootstrap Repository Methodology

The disposable bootstrap environment supplies the Design input, canonical realization inputs, and bootstrap implementation required to construct the first FS0 candidate.

The bootstrap repository and candidate repository may use concrete paths chosen by their configuration and realization, but this Design does not define those repository-specific filesystem paths.

Bootstrap shall expose one canonical invocation surface and shall keep invocation concerns separate from substantive bootstrap implementation.

The bootstrap payload retained after cutover remains non-authoritative maintenance source and generation machinery.

Its retention does not grant structural permission; retained filesystem objects must be authorized by the canonical repository-structure configuration of the candidate or accepted repository.

---

# Bootstrap Principle

FS0 cannot authorize its own initial existence.

Therefore one explicit external bootstrap exception is required.

Before cutover, the bootstrap process operates outside FS0 Governance authority.

Pre-cutover execution of candidate FS0 mechanisms produces bootstrap verification evidence only.

It shall not be represented as governed FS0 Conformance, governed FS0 Assurance, or FS0 Governance acceptance before the first FS0 state is accepted.

The bootstrap mechanism may:

- construct the initial FS0 candidate inside a user-supplied Git repository;
- install the minimum FS0 GitHub operating profile into repository content;
- publish and inspect candidate state through the user-established Git/GitHub environment;
- run initial bootstrap mechanical verification;
- run external bootstrap semantic audit;
- correct bootstrap defects; and
- explicitly accept one exact repository revision as the first FS0 operating state.

After initial FS0 acceptance, bootstrap authority is exhausted.

Bootstrap maintenance machinery may remain in use for FS0 maintenance.

Its execution shall not independently authorize mutation or create accepted state.

All subsequent persistent framework change shall occur through FS0 Governance.

---

---

## Local Bootstrap and GitHub Publication Boundary

The retained bootstrap payload is copied into an otherwise empty target directory.

Bootstrap shall initialize the target Git repository when it is absent, verify required local Git and execution capabilities, construct the complete initial FS0 candidate, and create the first local commit containing that complete candidate.

Bootstrap shall not create the GitHub repository, configure or publish a remote, or establish user credentials.

After local bootstrap succeeds, the user creates the GitHub repository and may use `gh repo create` to add the remote and push the existing local repository.

That first remote push publishes the already complete locally bootstrapped FS0 candidate; no partial bootstrap commit is required on the remote.

GitHub authentication, network connectivity, and remote mutation capability are operating prerequisites for publication and subsequent FS0 operation, not prerequisites to construction of the initial local candidate.

A missing local prerequisite shall stop bootstrap with a clear error.

Technical Git or GitHub capability does not create FS0 authority.

# FS0.6 — Operating Substrate

## Purpose

Provide the minimum execution, Git, network, authentication, privileged-mutation, and repository-orientation capabilities required for FS0 to build and evolve itself after the external bootstrap environment is removed.

FS0 should be understood like a minimal base operating-system installation: deliberately small, but already capable of acquiring, building, installing, verifying, and publishing the rest of the system.

Minimality shall not be achieved by removing capabilities required for self-hosting.

## Required Local and Remote Tooling Capabilities

The FS0 operating environment shall provide access to:

- Git repository inspection;
- Git branch, commit, ref, fetch, pull, and push operations;
- HTTPS/TLS network access;
- DNS/network resolution as required by GitHub;
- authenticated GitHub API access;
- GitHub issue, branch, pull-request, comment/review, ref, and workflow operations required by the FS0 GitHub binding;
- execution of FS0-maintained scripts and Conformance commands;
- retrieval of remote Conformance evidence; and
- publication of accepted state.

These are operating capabilities, not independent authority.

## Governed Privileged Mutation

FS0 requires the repository-framework equivalent of privilege escalation.

An actor or automation may possess technical credentials capable of changing repository or GitHub state, but possession of those credentials does not grant Governance authority.

Privileged mutation shall follow:

```text
accepted authority
→ accepted Plan
→ authorized Build
→ bounded privileged mutation
→ verification
→ explicit acceptance
```

A privileged mutation capability shall be usable only within the scope authorized by the applicable governed Build work.

Technical write access shall not authorize adjacent, unrelated, or successor work.

## Self-Modification

After cutover, FS0 shall be capable of:

- reading its accepted authority;
- proposing a bounded change;
- establishing accepted Design authority;
- establishing an accepted Plan;
- creating and publishing candidate repository state;
- changing its own maintained framework implementation when authorized;
- changing its own GitHub realization when authorized;
- executing remote Conformance against the candidate;
- performing required semantic audits and resolving their GitHub merge/issue-closure dispositions;
- explicitly accepting or rejecting the candidate; and
- publishing the resulting accepted repository state.

No step in this sequence may require the external bootstrap environment.

## Network Sufficiency

GitHub access is part of the initial FS0 operating substrate.

The installed FS0 shall have enough authenticated network capability to read and mutate every GitHub object used by the FS0 GitHub binding, subject to Governance authorization.

Networking is operational substrate.

GitHub-specific semantics remain subordinate to portable FS0 authority.

## Bootstrap-Generated Repository Orientation Surfaces

Bootstrap may generate repository-orientation, licensing, workflow, authority, state, or other required operating surfaces.

Design may define required semantic roles and content responsibilities for those surfaces where necessary for FS0 self-hosting.

Design shall not define their concrete repository paths.

Every generated filesystem object shall be positively authorized by the canonical repository-structure configuration.

Generation does not itself grant structural permission.

The generated destination of any artifact is realization/configuration state rather than Design-defined repository structure.

## Bootstrap Payload Scope

The retained bootstrap payload shall contain only material required to construct, verify, accept, cut over, and maintain FS0.

Its allowed source roles are non-authoritative bootstrap Design input, canonical bootstrap realization input, and bootstrap invocation/implementation.

Generated artifacts shall remain semantically distinct from non-authoritative bootstrap maintenance source and shall not be classified as bootstrap maintenance-source artifacts merely by generation.

The bootstrap payload shall not contain requirements, design discussion, or implementation assumptions for the future developed repo-spec product except where strictly necessary to define the bootstrap output required for FS0 self-hosting.

The canonical bootstrap invocation surface shall contain only invocation concerns. Substantive transformation, validation, installation, verification, and cutover behavior shall reside in separately identified bootstrap implementation and shall not embed successor semantics that belong in canonical realization input.

After the complete bootstrap payload is present in a compliant target repository, bootstrap shall require no semantic, template, or script input from the originating repository.

## Bootstrap Data, Template, and Generator Model

For bootstrap-created maintained artifacts, the canonical maintenance methodology is:

```text
structured source data
+ applicable transformation or template
+ generator
-> generated artifact
```

Each generated artifact shall have machine-resolvable provenance identifying its canonical source material, transformation/generation mechanism, and destination.

Those provenance and generation records are maintenance metadata and shall not become independent normative authority.

Concrete source-tree layout, template-tree layout, implementation-module layout, and generated destinations shall be defined by repository configuration and realization rather than by Design.

Bootstrap implementation shall keep invocation concerns separate from substantive transformation, validation, installation, verification, and cutover logic.

Successor Design Proposal source and FS0 realization source shall remain semantically distinguishable where their authority status differs, without requiring Design to prescribe concrete filesystem layout.

## Bootstrap Independence

After cutover, authoritative determination shall not require reading non-authoritative bootstrap maintenance source.

FS0 maintenance may use the accepted repository's retained bootstrap source and generation machinery when authorized by FS0 Governance.

Post-cutover operation shall require no semantic, template, generator, or script input from the originating bootstrap repository or another external bootstrap environment.

## Operating-Substrate Acceptance Test

FS0 operating substrate is sufficient only if an authorized agent operating through the GitHub remote can:

1. discover repository purpose and operating rules from the canonical repository-orientation surfaces;
2. resolve current accepted state;
3. inspect controlling authority and governed work;
4. create bounded candidate work;
5. publish candidate repository changes;
6. execute and inspect remote Conformance;
7. create or inspect required structured Assurance audit receipts, GitHub evidence/history, and merge/issue-closure disposition state;
8. perform authorized privileged GitHub mutations;
9. record explicit acceptance; and
10. publish the successor accepted state without access to the bootstrap environment.

---

---
