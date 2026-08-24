# FS0 GitHub Remote Operating Profile

## Status

Part of the non-authoritative FS0-Core Bootstrap Design Proposal.

Read `fs0-design.md` first. This chunk does not independently create authority.

---

# FS0.7 — GitHub Remote Operating Profile

## Purpose

Provide the minimum GitHub realization necessary for FS0 to be operated end to end without access to a contributor's local filesystem.

GitHub is the required initial operating platform for FS0.

GitHub does not define Governance, Conformance, or Assurance semantics.

It realizes those semantics.

## Required Remote Capabilities

FS0 shall be operable through the GitHub remote for:

- repository state inspection;
- file and artifact reads;
- governed artifact creation and update;
- stable governed-work identity;
- candidate branch or commit identity;
- candidate review;
- canonical remote Conformance execution;
- remote Assurance evidence and findings;
- explicit stage acceptance representation;
- exact candidate revision resolution;
- merge or equivalent accepted-state publication; and
- accepted repository-state resolution.

## Bootstrap GitHub Realization

FS0 may use GitHub-native mechanisms such as:

- issues;
- branches;
- commits;
- pull requests;
- Actions;
- comments or reviews; and
- repository files.

The allowed GitHub mechanism set above is implementation latitude only; the normative FS0 mapping is fixed by the binding below.

No GitHub mechanism gains framework authority merely because FS0 uses it.

## GitHub Capability and Credential Contract

The user is responsible for establishing Git and GitHub authentication before bootstrap.

Bootstrap and post-cutover FS0 shall verify only that the acting identity can perform the technical capabilities required by the intended operation.

Required capability classes include:

```text
repository metadata read
repository content read
repository content write
Git ref read
Git ref create/update
issue read
issue create/update/comment
pull-request read
pull-request create/update
workflow/check read
workflow execution through repository events
commit/status evidence read
authenticated actor identity resolution
```

Authentication secrets, tokens, private keys, and equivalent credentials shall remain external to repository-maintained state.

A missing required capability shall block the operation.

Technical write permission is capability only and shall not enlarge Governance authorization.

## FS0 GitHub Binding

The initial GitHub realization is fixed for FS0 bootstrap and first self-hosted operation.

The mapping is:

| Framework concept | FS0 GitHub realization |
| --- | --- |
| Design Proposal | maintained repository file |
| Design governed work | GitHub issue |
| Plan governed work | separate GitHub issue |
| Build governed work | separate GitHub issue |
| candidate repository state | Git branch and exact commit SHA |
| candidate review surface | pull request |
| canonical Conformance execution | GitHub Actions workflow |
| Conformance evidence | workflow/check result tied to exact candidate SHA |
| Assurance review context and evidence | governed GitHub issue and pull-request discussion/history, including structured JSON semantic-audit receipts, review/check history, and durable GitHub relationships |
| candidate semantic-audit receipt | structured JSON pull-request comment bound to governed work, exact PR head, required obligations, outcome, evidence, exclusions, and audit time |
| completion semantic-audit receipt | structured JSON governed-issue comment bound to governed work, exact accepted `main` revision, relevant accepted PRs, required obligations, outcome, evidence, exclusions, and audit time |
| candidate Assurance disposition | authorized merge of the exact conforming pull request after a satisfactory applicable pre-merge audit receipt |
| completed-work Assurance disposition | authorized closure of the governed issue after a satisfactory applicable pre-closure main audit receipt and Development linkage of its relevant accepted pull requests |
| Design/Plan/Build stage acceptance | authorized merge of an exact conforming pull request associated with exactly one governed-work issue after candidate semantic audit |
| bootstrap provenance | dedicated GitHub issue created by the external bootstrap process |
| bootstrap acceptance | authorized merge of the designated validated bootstrap-cutover pull request |
| accepted repository state | revision currently referenced by `refs/heads/main` after an authorized governed merge |

GitHub merge state creates Governance acceptance only for an exact conforming governed pull request merged by its authorized acceptance actor after semantic audit. That merge is also the candidate Assurance satisfaction disposition. Later authorized issue closure records completed-work Assurance satisfaction and completion but does not create or alter repository acceptance.

GitHub provides identity, collaboration, execution, and publication surfaces.

Framework semantics remain defined by accepted FS0 authority.

## Required Remote Questions

FS0 must make these questions answerable from repository/GitHub state without relying on chat history:

1. What revision is currently accepted?
2. What Design work is active?
3. What Design Proposal initiated it?
4. What normative delta is the candidate or accepted Design result?
5. What Plan is accepted?
6. What Build work is authorized?
7. What exact revision is under review?
8. What Conformance evidence applies to that revision?
9. What Assurance audit context, GitHub evidence/history, and disposition apply to that revision?
10. Has the candidate been explicitly accepted?
11. What resulting revision became accepted?
12. What work remains unauthorized?

## Minimum GitHub State Management

FS0 shall distinguish:

```text
repository content
desired GitHub operating state
observed GitHub state
authorized mutation
verified resulting state
```

However, FS0 does not need to govern all GitHub settings.

## Deferred GitHub Capabilities

FS0 shall defer unless strictly required for safe bootstrap operation:

- generalized hosting-platform profile framework;
- branch-protection management;
- repository ruleset management;
- merge queues;
- comprehensive label management;
- repository settings management;
- generalized rollback framework;
- generated issue forms;
- generated pull-request templates;
- full remote desired-state management; and
- support for hosting platforms other than GitHub.

---

---

# FS0.8 — Bootstrap Installation and Cutover

## Purpose

Create the one accepted FS0 state from which all later framework evolution becomes self-hosted.

## Bootstrap Sequence

The bootstrap sequence shall be:

1. verify local Git, GitHub remote, authentication, and required technical capabilities before remote publication;
2. create the dedicated bootstrap provenance issue;
3. create a temporary bootstrap-cutover branch from the current `refs/heads/main`;
4. construct the complete cutover candidate on that branch;
5. generate required maintained and generated surfaces;
6. execute bootstrap mechanical validation and canonical Conformance;
7. commit and publish the validated candidate branch;
8. open one designated bootstrap-cutover pull request targeting `refs/heads/main`;
9. have the authorized user perform the external semantic review;
10. merge the pull request to express semantic audit satisfaction and explicit bootstrap acceptance;
11. treat the resulting `refs/heads/main` revision as the first accepted FS0 repository state;
12. exhaust bootstrap authority and use FS0 Governance for later framework evolution.

## One-Way Cutover Marker

FS0 shall maintain a machine-resolvable bootstrap cutover record.

The committed cutover record shall identify at least:

```text
cutover state
bootstrap provenance issue
accepted Git ref
cutover timestamp
```

The bootstrap-cutover operation and GitHub remote state shall machine-resolvably identify the designated bootstrap pull request, its exact candidate head SHA, and its association with the bootstrap provenance issue. The designated pull request identity need not be embedded in the committed cutover record because that pull request is created only after the exact cutover candidate has been committed and published.

The only valid bootstrap lifecycle is:

```text
candidate
→ cutover
```

There is no transition from `cutover` back to bootstrap candidate mode.

After `cutover`:

- bootstrap authority shall remain exhausted;
- authoritative determination shall use accepted authoritative read surfaces rather than non-authoritative bootstrap maintenance source;
- bootstrap maintenance machinery may be used only within FS0 Governance-authorized work;
- bootstrap maintenance machinery shall not independently create acceptance; and
- ordinary framework evolution shall occur only through FS0 Governance.

## Bootstrap Artifact Status

Bootstrap Design artifacts remain non-authoritative provenance.

Bootstrap source data, templates, and generators may remain active FS0 maintenance state after cutover.

They shall not become authoritative read surfaces or independent authorization paths.

## Cutover Invariant

**After FS0 cutover, every persistent framework change SHALL occur through FS0 Governance, and no bootstrap-only mechanism SHALL independently create accepted framework state.**

---
