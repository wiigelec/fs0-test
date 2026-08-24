# FS0-Core Bootstrap Design Proposal

## Status

Design proposal for the disposable `fs0-proto` bootstrap repository.

This document is non-authoritative bootstrap Design input.

It does not become accepted FS0 authority before cutover.

The one-time external bootstrap process may use this Design input to construct, audit, verify, and explicitly accept the first FS0 operating state.

Its purpose is to define the minimum end-to-end functional set required to install a self-hosting repository framework that can use its own Governance, Conformance, Assurance, operating substrate, and GitHub mechanisms to build the remainder of the successor repo-spec design.

FS0 is intentionally minimal.

Anything FS0 can correctly build after bootstrap should be deferred unless it is required for the first complete self-hosted remote lifecycle.

---

# Design Proposal Structure

This Design Proposal is split into bounded chunks so a human or AI agent can load only the context required for the current question.

The chunks collectively form one non-authoritative FS0 Design Proposal. No chunk independently creates authority.

| File | Primary content |
| --- | --- |
| `fs0-design.md` | entry point, objective, invariant, capability map |
| `fs0-authority-governance.md` | acceptance state, authority, Governance, normative requirements |
| `fs0-conformance-assurance.md` | mechanical Conformance and semantic Assurance kernels |
| `fs0-operating-substrate.md` | bootstrap boundary, user prerequisites, operating substrate, bootstrap implementation |
| `fs0-github.md` | GitHub capability contract, fixed GitHub binding, cutover |
| `fs0-installed-layout.md` | repository-structure governance methodology and structural Conformance semantics |
| `fs0-self-hosting.md` | installed state, exclusions, self-hosting demonstration, acceptance and audit |

## Loading Rule

Always read this index first.

Then load only the chunk or chunks relevant to the current operation. Cross-cutting audits may load all chunks.

---

# Objective

FS0-Core shall establish the smallest remotely operable framework capable of performing this complete loop:

**bootstrap seed**
→ **accepted FS0 authority**
→ **Design Proposal**
→ **Design**
→ **accepted normative authority**
→ **Plan**
→ **accepted realization intent**
→ **Build**
→ **Conformance**
→ **Assurance**
→ **Build acceptance**
→ **new accepted repository state**
→ **repeat without bootstrap authority**

FS0 succeeds when it can build and accept FS1 using only FS0-governed mechanisms operating against the GitHub remote.

---

---

# Primary Design Invariant

**FS0 SHALL be the smallest self-sufficient network-capable framework kernel able to govern, modify, evaluate, and publish itself after cutover, and every capability not required for the first successful FS0-governed construction and acceptance of FS1 SHALL be deferred.**

---

---

# FS0 Capability Set

FS0 consists of eight capability groups:

1. Authority Kernel
2. Governance Kernel
3. Normative Requirement Kernel
4. Conformance Kernel
5. Assurance Kernel
6. Operating Substrate
7. GitHub Remote Operating Profile
8. Bootstrap Installation and Cutover

These groups are capability boundaries, not necessarily final specification or directory boundaries.

---

# Repository-Structure Methodology Boundary

FS0 Design defines repository-structure governance methodology and validation semantics.

FS0 Design shall not define repository-specific filesystem structure.

One canonical repository-structure configuration shall be the sole instance-level source of permission for filesystem objects beneath the repository root.

The repository root is a closed structural governance boundary.

Every filesystem object beneath that boundary shall require positive authorization from the canonical repository-structure configuration.

Absence of applicable authorization shall mean deny.

No filesystem object, directory class, tool-created state, generated state, ignored state, temporary state, or implementation convention shall receive implicit structural permission.

A directory authorization shall apply only to the directory itself unless that authorization explicitly grants permission to the complete descendant subtree.

Design may define the semantics by which the configuration expresses required or permitted presence, exact object authorization, directory authorization, and whole-subtree authorization, but concrete repository paths and concrete repository layout belong to configuration rather than Design.

Conformance shall mechanically evaluate the actual filesystem namespace beneath the repository root against that configuration.

Bootstrap may construct the initial configuration as part of candidate creation, but after the candidate exists no bootstrap convention or implementation default shall substitute for configuration authorization.

---

# FS0 Maintenance and Read-Surface Boundary

FS0 shall distinguish non-authoritative maintenance source, generation implementation, generated read surfaces, and accepted authoritative read surfaces by machine-resolvable semantic role rather than filesystem location.

After cutover, authoritative determination shall use accepted authoritative read surfaces and shall not use non-authoritative maintenance source as fallback authority when source and generated read surfaces disagree.

Post-cutover maintenance may modify retained bootstrap maintenance source only through FS0 Governance-authorized work.

Generated FS0 read surfaces shall be produced from canonical maintenance inputs and generation implementation.

Generated FS0 read surfaces shall not be independently maintained as canonical source.

Generation shall be deterministic for identical canonical inputs and explicitly declared variable inputs.

Conformance shall mechanically verify correspondence between canonical maintenance source and generated FS0 read surfaces.

A source/read-surface mismatch is a Conformance defect.

Post-cutover FS0 shall require no semantic, template, generator, or script input from outside the accepted repository state.

## Repository-Structure Configuration Resolution

Governed repository state shall determine exactly one canonical repository-structure configuration identity for the validation subject.

The operating substrate shall resolve that governed identity to the corresponding configuration object through a location-independent mechanism.

The operating substrate resolves configuration identity; it shall not select among candidate configurations.

Configuration identity determination, configuration object resolution, and configuration authorization are distinct operations.

After resolution, the configuration shall authorize its own filesystem object under the same structural rules that govern every other object.

Failure to determine exactly one governed configuration identity or to resolve that identity to exactly one configuration object shall cause repository-structure Conformance failure.

Caller preference, environment convention, implementation default, search order, filename convention, or fallback location shall not determine the canonical configuration identity.

---
