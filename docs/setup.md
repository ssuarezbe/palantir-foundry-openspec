# Setup

How to set up the kit for the tools and checks you actually have. Find your situation in section 1, then follow its steps in section 3.
Every situation uses the same files (`core/`). They differ in what, if anything, checks the specs automatically.
Tested here: the bundle, the three checks and the copy-only install on macOS, Node 20.19.3 and Python 3.14, offline. Not tested here: anything inside Foundry (see section 6).

## 1. Find your situation

| # | Your situation | Copy | Checked automatically | Checked only by a person |
| --- | --- | --- | --- | --- |
| 1 | **AI FDE only. Checks run no tests.** No shell, no Node | `core/` | Nothing about the specs | Everything. Use the review list in `docs/ai-fde.md` |
| 2 | **TypeScript functions repository. Jest runs in Checks and can start a child process** | `core/`, `addons/cli/`, `openspec.test.ts`, `glossary.test.ts` | Full OpenSpec validation (strict), forbidden synonyms, empty definitions, Ontology names | Gherkin style, design review, open questions |
| 3 | **TypeScript repository. Jest runs, but no child process, or the Node version in Checks is old or unknown** | `core/`, `openspec-rules.test.ts`, `glossary.test.ts` (no CLI) | The TypeScript port of the OpenSpec rules, forbidden synonyms, empty definitions, Ontology names | The same, plus the OpenSpec warnings the port does not cover (for example a Purpose under 50 characters) |
| 4 | **Python repository or Python checks. No Node** | `core/`, `test_openspec_rules.py` | Same as 3, in Python | Same as 3 |
| 5 | **Laptop or Foundry VS Code workspace with Node 20+** | `core/`, `addons/cli/`, `addons/workspace/` | Whatever you run: `validate --strict` before each commit | The same as 2 |
| 6 | **Several repositories, one product** | Put 1 to 5 in the spec home. Other repositories get one line (`docs/multi-repo.md`) | As in the spec home | As in the spec home |

You can combine situations: the same repository can have situation 1 for AI FDE and situation 2 for Checks, and laptops can use 5. The files are the same.
`core/` means `core/project-template/openspec/` copied to `openspec/` in your repository, and `core/aip-skills/` loaded as skills in AI FDE (`docs/ai-fde.md`).

## 2. Add the CLI to an existing repository without npm

Situations 2 and 5. The CLI is one JavaScript file with its own dependencies inside. There is no `npm install`, no entry in `package.json` and no network access. You copy a folder.

1. Unzip the kit (or copy the unpacked folder). Check the bundle: from `addons/cli/` run `shasum -a 256 -c SHA256SUMS` (macOS), `sha256sum -c SHA256SUMS` (Linux), or on Windows compare `certutil -hashfile openspec-1.16.0\dist\cli\openspec.mjs SHA256` with the line in `SHA256SUMS`.
2. Copy the folder `addons/cli/` into your repository as `tools/openspec/`. Copy it whole. The bundle reads `package.json` two folders above itself and `schemas/` next to it, so do not flatten or rename `openspec-1.16.0/`.

   ```
   tools/openspec/
     launchers/openspec          sh launcher (Windows: openspec.cmd)
     openspec-1.16.0/
       dist/cli/openspec.mjs     the CLI, one file
       package.json
       schemas/
     SHA256SUMS  PIN.md  ...
   ```

3. Make sure Git keeps `dist/`. Many `.gitignore` files contain `dist`. Run `git check-ignore -v tools/openspec/openspec-1.16.0/dist/cli/openspec.mjs`. If it prints a rule, add `!/tools/openspec/openspec-1.16.0/dist/` to `.gitignore`.
4. Copy `core/project-template/openspec/` to `openspec/` at the repository root.
5. Run it. The launcher sets `OPENSPEC_TELEMETRY=0` and calls `node`:
   - macOS or Linux: `./tools/openspec/launchers/openspec --version`. Expect `1.16.0`.
   - If the execute bit was lost in the copy (some uploads drop it): `sh tools/openspec/launchers/openspec --version`, or `chmod +x tools/openspec/launchers/openspec`.
   - Windows: `tools\openspec\launchers\openspec.cmd --version`.
   - No launcher at all: `OPENSPEC_TELEMETRY=0 node tools/openspec/openspec-1.16.0/dist/cli/openspec.mjs --version`.
6. Validate: `./tools/openspec/launchers/openspec validate --all --strict --no-interactive`. An empty project prints `No items found to validate.`
7. Commit `tools/` and `openspec/` on a branch.

The only requirement is Node on the PATH. OpenSpec 1.16.0 declares Node 22.12 or newer. We tested 20.19.3 only. If your Node is older than that, use situation 3 or 4 for the gate.
`maintainer/tests/run-all.sh` section 9 proves steps 2 to 6 from a plain copy, with the execute bit removed.

## 3. Steps for each situation

### Situation 1: AI FDE only, no gate

1. Load the four skills and prepare the repository: `docs/ai-fde.md`.
2. Work in the order Explore, Propose, Apply, Archive. Each skill uses a branch, never commits to main and reads Checks.
3. With no gate, a person reviews every change before merge. Use the review list in `docs/ai-fde.md`. It is the same list the automatic checks apply.
4. Later you can add a gate without changing anything else: situation 2, 3 or 4.

### Situation 2: TypeScript repository, Jest can run a child process

1. Follow section 2 to copy the CLI and the template.
2. Copy `addons/ci/typescript/openspec.test.ts` and `addons/ci/typescript/glossary.test.ts` into a folder Jest already scans. They must be inside the repository, below the folder that holds `openspec/`. The test looks for the bundle at `tools/openspec/openspec-1.16.0/dist/cli/openspec.mjs`; set `OPENSPEC_CLI` to use another path.
3. Merge `addons/ci/typescript/tsconfig.snippet.json` into `tsconfig.json`: `"types": ["jest", "node"]`. The tests need Node types for `child_process`, `fs` and `path`. The code uses ES2020 features such as `matchAll`: set `target` or `lib` to ES2020 or newer.
4. Run `npm test` (or your repository's test command). Both tests pass on an empty project.
5. If `openspec.test.ts` fails with a spawn or permission error, or with a Node version message, Checks cannot run the bundle. Delete it and use situation 3.

### Situation 3: TypeScript repository, no child process

No CLI is needed, so section 2 does not apply. Copy only `core/project-template/openspec/` to `openspec/`.

1. Copy `addons/ci/typescript/openspec-rules.test.ts` and `addons/ci/typescript/glossary.test.ts` into a folder Jest already scans. Do not copy `openspec.test.ts` as well: it would only repeat the same rules through the bundle.
2. Merge the tsconfig snippet as in situation 2. These tests use only `fs` and `path`, so Node types are enough.
3. Run `npm test`. Both pass on an empty project.
4. The port checks what the bundle checks in strict mode for requirements, scenarios and deltas, and gives the same answer on every fixture in the source repository. It does not reproduce every OpenSpec warning. On a machine with Node, run the real CLI before a release.

### Situation 4: Python

1. Copy `addons/ci/python/test_openspec_rules.py` into the tests folder.
2. Run `python3 test_openspec_rules.py`. It needs only the standard library (Python 3.11 or newer). Expect `OK`.
3. Write specs with the AIP skills or the Claude and Continue prompts. The skills tell the assistant each step in words.

### Situation 5: laptop or Foundry VS Code workspace

In a Foundry VS Code workspace you have a terminal, the Continue extension with Palantir models and the Palantir MCP.

1. Follow section 2 to copy the CLI and the template.
2. Copy `addons/workspace/.continue/` to `.continue/`, or `addons/workspace/.claude/` to `.claude/` for Claude Code.
3. Fill in `openspec/glossary.md`: delete the `Example:` rows and add your terms.
4. In Continue, type `/opsx-` and pick `explore`, `propose`, `apply` or `archive`. In Claude Code the commands are `/opsx:explore` and so on. They call the launcher, so telemetry stays off.
5. Work on a branch. Before every commit, validate: `./tools/openspec/launchers/openspec validate --all --strict --no-interactive`. Fix every error and warning: `--strict` turns warnings into failures, as in Checks.
6. Commit, push and read Checks.

Notes: do not run `openspec init` in the repository: the template already holds `openspec/` with the Foundry schema. Use the Palantir MCP to confirm Ontology API names while you explore. The prompts and skills call `./tools/openspec/launchers/openspec`.

### Situation 6: several repositories

Put the gate only in the spec home (`docs/multi-repo.md`). Other repositories declare `store: <id>` in `openspec/config.yaml`. All three checks skip themselves there.

## 4. Optional: Ontology names and branch protection

- Put a JSON list of object type, link type and action type API names at `openspec/ontology.json`, for example `["Shipment", "Carrier"]`. The glossary check then fails on any `Ontology:` name or glossary Ontology resource not in the list. Without the file the check is skipped. Refresh the file when the Ontology changes.
- Protect the branch: require Checks to pass before merge and block direct commits to main.

### Read a failure

- `openspec validate failed:` followed by OpenSpec's message (situation 2): fix the file it names.
- `... must include at least one scenario`, `... should contain SHALL or MUST`, `... is missing a THEN step`, `Change must have at least one delta` (situations 3 and 4): fix the spec or the change it names.
- `forbidden synonym 'x' (use 'Y') in file:line`: replace the word with the glossary term.
- `glossary term 'T' has no definition`: fill in the definition.
- `Ontology reference 'N' ... is not in openspec/ontology.json`: fix the name or update the export.

## 5. What each check covers

| Rule | CLI bundle (2, 5) | TypeScript port (3) | Python (4) |
| --- | --- | --- | --- |
| Requirement has a scenario | yes | yes | yes |
| Scenario has WHEN/GIVEN and THEN | yes (strict) | yes | yes |
| Requirement has SHALL or MUST | yes (strict) | yes | yes |
| Change has a delta, or `skip_specs: true` | yes | yes | yes |
| Other OpenSpec warnings (for example a short Purpose) | yes (strict) | no | no |
| Forbidden synonym, empty definition, unmapped Ontology name | no, `glossary.test.ts` adds it | no, `glossary.test.ts` adds it | yes, in the same file |

No check covers keyword order, a single `WHEN`, business wording, the design review or open questions.
Code spans and fenced code are ignored by the synonym check, and so are `Ontology:` and `Implemented in:` lines. Rows whose term starts with `Example:` are skipped. Archived changes are not scanned.
The source repository tests the CLI, the TypeScript port and the Python port against 18 fixtures and requires the three to agree (`maintainer/tests/fixtures/`, not in the release zip).

## 6. What to confirm in Foundry

Nothing below has been tested inside Foundry.

- **Node version.** Run `node --version` in each workspace and in Checks. OpenSpec 1.16.0 declares Node 22.12 or newer. Our tests used 20.19.3.
- **Child process.** Whether Checks lets Jest start `process.execPath`. If not, situation 3.
- **tsconfig.** Whether the repository's `tsconfig` accepts Node types and ES2020.
- **Repository contents.** That a Code Repository accepts `tools/openspec/` (about 3 MB, one 2 MB file), keeps `dist/` out of `.gitignore`, and has `tools/` present in the Checks checkout. That the repository's build, lint and formatting do not scan `tools/`.
- **Execute bit.** Whether the launcher keeps it after the copy. If not, call it with `sh`.
- **Python.** The version available for situation 4.
- **Workspace.** That Continue shows the `/opsx-` prompts from `.continue/prompts/`, loads skills from `.continue/skills/`, may run terminal commands, and that the Palantir MCP is on.
- **AI FDE.** See `docs/ai-fde.md`.
