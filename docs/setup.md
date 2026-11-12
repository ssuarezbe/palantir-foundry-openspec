# Setup

How to set up the kit: pick a route, set up a Foundry VS Code workspace, and add the optional CI gate. Each part starts with a three-line summary and ends with what to confirm in Foundry.

## Routes

Pick the route that matches the tools you have. Route A needs Node. Route B needs Python. Route C needs only AI FDE.
All routes use the same rules: a change has a proposal, specs, a design, Foundry files (`ontology.md`, `data.md`, `logic.md`), an open questions log and tasks, and the specs must pass validation.
Tested here: route A end to end (new change, validate, archive) and route B checks. Route C skills are written and grep-tested, not run in AI FDE.

### Steps

1. Find out what you have.
   - Node 20 or newer on the machine or workspace terminal: route A.
   - No Node, but Python 3.11 or newer: route B.
   - AI FDE with no shell: route C.
2. Route A.
   - Copy `addons/cli/` to `tools/openspec/`. Always call the CLI through `tools/openspec/launchers/openspec` (or `openspec.cmd`). The launcher sets `OPENSPEC_TELEMETRY=0` and runs `node` on the bundle.
   - The bundle is one file plus `package.json` and `schemas/`. Keep that layout. The file reads `package.json` two folders above itself.
   - Verify it: `shasum -a 256 -c addons/cli/SHA256SUMS` from the `addons/cli/` folder.
3. Route B.
   - Copy `addons/ci/python/test_openspec_rules.py` into the repo. It checks the same rules as `openspec validate --strict`: a requirement needs a `#### Scenario:`, each scenario needs a WHEN/GIVEN and a THEN step, a requirement needs SHALL or MUST, a change needs at least one delta unless `.openspec.yaml` has `skip_specs: true`. It also runs the glossary rules.
   - Write specs with the AIP skills. They tell the assistant each step in words.
   - The port covers the rules listed above. It does not cover every OpenSpec warning (for example a Purpose under 50 characters). On a machine with Node, run the real CLI before a release.
4. Route C.
   - Load the four skills as in `docs/ai-fde.md`.
   - AI FDE edits a branch of the Code Repository and reads Checks. Checks run the gate from `docs/setup.md`.
5. Mix routes. A team can use route A on laptops and route C in Foundry. The files are the same.

### What to confirm in Foundry

- The Node version in your VS Code workspaces and in Checks. OpenSpec 1.16.0 states `node >=22.12.0`. The bundle was tested here on Node 20.19.3 only. Run `node --version` in each place.
- Whether the workspace terminal can run `./tools/openspec/launchers/openspec` (execute bit kept after the repo copy). If not, call `node tools/openspec/openspec-1.16.0/dist/cli/openspec.mjs` with `OPENSPEC_TELEMETRY=0`.
- Whether Python 3.11 or newer is available for route B.

## Foundry VS Code workspace

In a Foundry VS Code workspace you have a terminal, the Continue extension with Palantir models and the Palantir MCP.
Copy the kit files into the repository once, then call the CLI only through the launcher.
Tested here: launcher on macOS, the rewritten prompt files, validate and archive. Not tested here: Continue inside Foundry.

### Steps

1. In the repository root, copy:
   - `addons/cli/` to `tools/openspec/`
   - `core/project-template/openspec/` to `openspec/`
   - `addons/workspace/.continue/` to `.continue/`
2. Check the launcher: `./tools/openspec/launchers/openspec --version`. Expect `1.16.0`. If you get "permission denied", run `chmod +x tools/openspec/launchers/openspec`.
3. Open `openspec/glossary.md`. Delete the `Example:` rows. Add your terms.
4. In Continue, type `/opsx-` and pick a prompt: `explore`, `propose`, `apply`, `archive`, `sync`, `update`. They call the launcher, so telemetry stays off.
5. Work on a branch. Never commit to main.
6. Before every commit, validate:
   `./tools/openspec/launchers/openspec validate --all --strict --no-interactive`
   Fix every error and warning. `--strict` turns warnings into failures, as in Checks.
7. If the repository has the gate (`docs/setup.md`), also run the repo's test command and expect it to pass.
8. Commit, push, and read Checks.

### Notes

- The prompts and skills use `./tools/openspec/launchers/openspec`. On Windows cmd, use `tools\openspec\launchers\openspec.cmd` with the same arguments.
- Do not run `openspec init` in the repository. `core/project-template/` already holds `openspec/` with the Foundry schema.
- Telemetry: the launcher sets `OPENSPEC_TELEMETRY=0`. Do not call `node .../openspec.mjs` without that variable.
- For Claude Code on a laptop, copy `addons/workspace/.claude/` to `.claude/` instead. Commands are `/opsx:propose` and so on.
- Palantir MCP: use it to confirm Ontology API names while you explore.

### What to confirm in Foundry

- Node is on the workspace PATH and is 20 or newer (`node --version`).
- The repository copy keeps the launcher's execute bit.
- Continue shows the `/opsx-` prompts from `.continue/prompts/`, and loads skills from `.continue/skills/`.
- Continue's agent may run terminal commands and the Palantir MCP is on.

## CI gate

Checks runs your Jest tests on every commit. The gate adds two tests: one runs OpenSpec validation, one checks the glossary and Ontology names.
Repositories without Node use the Python port, which gives the same answers on every test fixture in the source repository (`maintainer/tests/fixtures/`, not in the release zip).
Tested here: both tests and the port against 13 fixtures, on Node 20.19.3 and Python 3.14. Not tested here: any Foundry Checks run.

### Steps

0. Several repositories? Put the gate only in the spec home (`docs/multi-repo.md`). Satellites declare `store: <id>`, and both tests skip themselves there.
1. TypeScript functions repository.
   1. Copy `addons/cli/` to `tools/openspec/` and `core/project-template/openspec/` to `openspec/`.
   2. Copy `addons/ci/typescript/openspec.test.ts` and `addons/ci/typescript/glossary.test.ts` into a folder Jest already scans.
   3. Merge `addons/ci/typescript/tsconfig.snippet.json` into `tsconfig.json`: `"types": ["jest", "node"]`. The tests need Node types for `child_process`, `fs` and `path`. The code uses ES2020 features such as `matchAll`; set `target` or `lib` to ES2020 or newer.
   4. Run `npm test`. Both tests pass on an empty project.
2. Python repository.
   1. Copy `addons/ci/python/test_openspec_rules.py` into the tests folder.
   2. Run `python3 test_openspec_rules.py`. It needs only the standard library.
3. Optional Ontology check. Put a JSON list of object type API names at `openspec/ontology.json`, for example `["Shipment", "Carrier"]`. Then the glossary test fails on any `Ontology:` line or glossary API name not in the list. Without the file, the check is skipped. Refresh the file from the Ontology when it changes.
4. Protect the branch. Require the Checks to pass before merge, and block direct commits to main.
5. Read a failure.
   - `openspec validate failed:` followed by OpenSpec's message: fix the file it names.
   - `forbidden synonym 'x' (use 'Y') in file:line`: replace the word with the glossary term.
   - `glossary term 'T' has no definition`: fill in the definition.
   - `Ontology reference 'N' ... is not in openspec/ontology.json`: fix the name or update the export.

### What the checks cover

| Rule | CLI bundle | Jest | Python |
| --- | --- | --- | --- |
| Requirement has a scenario | yes | yes (runs bundle) | yes |
| Scenario has WHEN/GIVEN and THEN | yes (strict) | yes (runs bundle) | yes |
| Requirement has SHALL or MUST | yes (strict) | yes | yes |
| Change has a delta, or `skip_specs: true` | yes | yes | yes |
| Forbidden synonym, empty definition, unmapped Ontology name | no | yes | yes |

Code spans and fenced code are ignored by the synonym check. Rows whose term starts with `Example:` are skipped. Archived changes are not scanned.

### What to confirm in Foundry

- The Node version in Checks. OpenSpec 1.16.0 states `node >=22.12.0`; this kit was tested on 20.19.3.
- Whether Checks allows a child process. `openspec.test.ts` runs `process.execPath` on the bundle. If it is blocked, use the Python port or drop that test and keep `glossary.test.ts`, which needs no child process.
- Whether the repository's `tsconfig` accepts Node types and ES2020.
- That `tools/openspec/` is present in the Checks checkout (the bundle is about 3 MB).
- The Python version in Python repositories.

