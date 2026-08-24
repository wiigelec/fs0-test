# repo-spec FS0

FS0 is the minimal self-hosting core of repo-spec. It installs machine-readable authority, Conformance and Assurance identity surfaces, retained bootstrap maintenance data, and a canonical validation entry point.

This repository may be in bootstrap candidate state. Generated files, a merge, the default branch, CI success, issue closure, or an agent declaration do not by themselves create normative acceptance.

## Validate

Run:

```bash
./repo/scripts/validate
```

For detail:

```bash
./repo/scripts/validate --verbose
./repo/scripts/validate --json
```

Exit status is `0` for pass, `1` for failure, and `2` while the Conformance realization is incomplete.

## Authority and maintenance

Normative read surfaces live under `repo/authority/`.

`repo/bootstrap/data/` is the canonical maintained bootstrap data source used to derive FS0 artifacts. The generated surfaces are not independently maintained. After cutover, bootstrap source remains non-authoritative maintenance material and persistent framework change must route through Governance.

Regenerate from the repository root with:

```bash
./repo/bootstrap/scripts/bootstrap
```

Then validate the result.

`README.md` and `AGENTS.md` are operational orientation surfaces. They are not normative authority and must not be used to override accepted authority.

## License

This project is licensed under the GNU General Public License, version 3. See `LICENSE`.
## Discover successor Design Proposals

Use `repo/proposals/registry.json` as the canonical successor Design Proposal discovery surface. Each registry entry points to its canonical structured proposal read representation and generated Markdown projection.

Bootstrap Design source remains under `repo/bootstrap/design/` for bootstrap construction and maintenance context. It is non-authoritative after cutover.

## Discover bootstrap and accepted state

Read `repo/state/bootstrap.json` to determine whether the repository is still in bootstrap `candidate` state or has reached `cutover`.

After cutover, `refs/heads/main` is the canonical accepted repository state. A governed pull request becomes accepted when its exact candidate has passed canonical Conformance and semantic audit and is merged by its authorized acceptance actor. The merge itself records candidate Assurance satisfaction and acceptance. The governed issue remains open until the resulting main state passes completion semantic audit; relevant accepted PRs are then linked through GitHub Development and authorized issue closure records completed-work Assurance satisfaction. Technical write access does not enlarge Governance authorization.

## Branch model

`main` is the single persistent accepted repository branch. Candidate branches are temporary review surfaces and may be deleted after acceptance. GitHub merge history and governed repository/GitHub state provide acceptance provenance without a separate acceptance-receipt ref.
