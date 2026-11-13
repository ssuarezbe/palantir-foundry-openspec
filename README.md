# palantir-foundry-openspec

An internal kit of [OpenSpec](https://github.com/Fission-AI/OpenSpec) 1.16.0 for teams that build on Palantir Foundry in a network with no npm access. Version `1.16.0-foundry.5`, maintained by Optivia Labs.

Teams that build on Foundry describe a change in one place, before they build it: why, what behavior, which Ontology object types, link types, actions, functions and datasets, and what is still unknown. An AI assistant (AI FDE, Claude Code or Continue) writes those files, a person reviews them, and the assistant then builds from them. This kit supplies the rules, templates and skills for that, adapted to Foundry, plus a bundled OpenSpec CLI for teams that can run Node.

This is not an official OpenSpec or Palantir product. "Palantir" and "Foundry" are trademarks of Palantir Technologies Inc. The kit is internal. If it is ever published, rename it (for example `foundry-openspec-kit`). OpenSpec is MIT licensed; see `THIRD_PARTY_NOTICES.md`.

## Status: what is tested

- **Tested, offline, on Node 20.19.3:** the bundled CLI, the schema, 18 fixtures through the CLI, the TypeScript check, its pure TypeScript port and the Python port (all three agree), copying the CLI into a plain repository with no npm, the multi-repo store flow, and the checks on the skills, launchers and URLs. `maintainer/tests/run-all.sh` runs all of it.
- **Not tested:** anything inside Foundry (the Node version in Checks, whether Checks allow a child process, AIP skill size limits, menu names in AI FDE). No AI model has been run against the Gherkin, Foundry or design rules, so we do not know how well assistants follow them. OpenSpec declares Node 22.12 or later; we tested 20.
- **Before a wider rollout:** run one real change through AI FDE and one through Claude Code or Continue, and read what they write.

## How it works

Every change follows four steps. Each step is a skill (AI FDE) or a command (Claude Code, Continue):

| Step | Skill or command | What happens |
| --- | --- | --- |
| Explore | `OpenSpec Explore`, `/opsx:explore` | Read-only thinking. Confirms Ontology API names, matches words to the glossary, sketches scenarios and open questions. |
| Propose | `OpenSpec Propose`, `/opsx:propose` | Writes the change files (next section) on a branch. Checks then validate them. |
| Apply | `OpenSpec Apply`, `/opsx:apply` | Builds the tasks one at a time, acts out each `Verify:` line and ticks the box. Stops on a blocking open question. |
| Archive | `OpenSpec Archive`, `/opsx:archive` | After the work merges, folds the spec changes into `openspec/specs/` and moves the change folder to `openspec/changes/archive/`. The Foundry files stay in that folder with the change. |

In Continue the commands are written `/opsx-propose` and so on.

Three ideas run through the kit:

- **The glossary is the business vocabulary; the Ontology is the data model.** Specs are written in glossary terms and name Ontology resources by API name.
- **Rules live in files an assistant reads**, because gates are hard to run in a regulated Foundry network. The only automatic check is OpenSpec's own validation.
- **Gaps are recorded, not guessed.** Unknowns go in a log that blocks the tasks until answered.

## Pick your situation

Foundry teams have different tools and different checks available. Find yours. Every situation uses the same files (`core/`); they differ in what checks the specs automatically. Full steps: `docs/setup.md`.

| # | Your situation | Copy | Checked automatically | Checked only by a person |
| --- | --- | --- | --- | --- |
| 1 | **AI FDE only. Checks run no tests.** No shell, no Node | `core/` | Nothing about the specs | Everything: use the review list in `docs/ai-fde.md` |
| 2 | **TypeScript functions repository. Jest runs in Checks and can start a child process** | `core/`, `addons/cli/`, `openspec.test.ts`, `glossary.test.ts` | Full OpenSpec validation (strict), forbidden synonyms, empty definitions, Ontology names | Gherkin style, design review, open questions |
| 3 | **TypeScript repository. Jest runs, but no child process, or the Node version in Checks is old or unknown** | `core/`, `openspec-rules.test.ts`, `glossary.test.ts` (no CLI) | A TypeScript port of the OpenSpec rules, plus the glossary checks | The same, plus the few OpenSpec warnings the port does not cover |
| 4 | **Python repository or Python checks. No Node** | `core/`, `test_openspec_rules.py` | Same as 3, in Python | Same as 3 |
| 5 | **Laptop or Foundry VS Code workspace with Node 20+** | `core/`, `addons/cli/`, `addons/workspace/` | What you run: `validate --strict` before each commit | The same as 2 |
| 6 | **Several repositories, one product** | 1 to 5 in the spec home; one line elsewhere (`docs/multi-repo.md`) | As in the spec home | As in the spec home |

Situations combine: one repository can serve AI FDE (1) and Checks (2), and laptops can use 5. A gate can be added later without changing the specs.

What each item is, and where it goes in the Code Repository you work in:

| From this kit | To your repo | Situations |
| --- | --- | --- |
| `core/project-template/openspec/` | `openspec/` | all |
| `core/aip-skills/*.md` | a Compass folder, not the repo | 1 to 4 (AI FDE) |
| `addons/cli/` | `tools/openspec/` | 2, 5 |
| `addons/workspace/.continue/` or `.claude/` | `.continue/` or `.claude/` | 5 |
| `addons/ci/typescript/openspec.test.ts`, `glossary.test.ts`, `tsconfig.snippet.json` | your TypeScript test folder | 2 |
| `addons/ci/typescript/openspec-rules.test.ts`, `glossary.test.ts`, `tsconfig.snippet.json` | your TypeScript test folder | 3 |
| `addons/ci/python/test_openspec_rules.py` | your Python test folder | 4 |
| one line, `store: <id>` | `openspec/config.yaml` of every other repo | 6 |

## Add the CLI to an existing repository without npm

For situations 2 and 5. The CLI is one JavaScript file with its dependencies inside. There is no `npm install`, no `package.json` entry and no network use. You copy a folder:

1. Unzip the kit and check the bundle: from `addons/cli/` run `shasum -a 256 -c SHA256SUMS` (macOS) or `sha256sum -c SHA256SUMS` (Linux). On Windows, compare `certutil -hashfile openspec-1.16.0\dist\cli\openspec.mjs SHA256` with the line in `SHA256SUMS`.
2. Copy `addons/cli/` into your repository as `tools/openspec/`, whole. The bundle reads `package.json` two folders above itself and `schemas/` beside it, so do not flatten or rename `openspec-1.16.0/`.
3. Check that Git will keep `dist/`: `git check-ignore -v tools/openspec/openspec-1.16.0/dist/cli/openspec.mjs`. Many `.gitignore` files ignore `dist`; if a rule prints, add `!/tools/openspec/openspec-1.16.0/dist/`.
4. Copy `core/project-template/openspec/` to `openspec/` at the repository root.
5. Run `./tools/openspec/launchers/openspec --version` and expect `1.16.0`. No execute bit after the copy? Use `sh tools/openspec/launchers/openspec --version`. On Windows use `tools\openspec\launchers\openspec.cmd`.

The only requirement is Node on the PATH. OpenSpec declares Node 22.12 or newer; we tested 20.19.3. If your Node is older, or Checks cannot start a child process, use situation 3 or 4 for the gate. `maintainer/tests/run-all.sh` section 9 proves steps 2 to 5 from a plain copy with the execute bit removed. Not proven: that a Foundry Code Repository accepts the folder and keeps it in the Checks checkout (`docs/setup.md`, section 6).

## Quick start

### With Node 20+ (situations 2 and 5)

1. Do the five steps above.
2. Copy `addons/workspace/.continue/` to `.continue/`, or `addons/workspace/.claude/` to `.claude/`.
3. Fill in `openspec/glossary.md`: delete the two `Example:` rows and add your terms, each with the object, link and action types that represent it. Edit `openspec/config.yaml` if you need to.
4. Validate: `./tools/openspec/launchers/openspec validate --all --strict --no-interactive` (Windows: `tools\openspec\launchers\openspec.cmd validate ...`). Expect `No items found to validate.`
5. Run `/opsx-propose` in Continue or `/opsx:propose` in Claude Code, and describe a change.
6. Validate again. Commit on a branch. For a gate in Checks, add the situation 2 tests (`docs/setup.md`).

### TypeScript Checks without a child process (situation 3)

1. Copy `core/project-template/openspec/` to `openspec/`. Fill in the glossary as above.
2. Copy `openspec-rules.test.ts`, `glossary.test.ts` and the tsconfig snippet from `addons/ci/typescript/` into your test folder. Run `npm test`. Both pass on an empty project.
3. Write changes with the AIP skills (below). Checks now fail on a missing scenario, a missing `SHALL`, a forbidden synonym or an unknown Ontology name.

### Python (situation 4)

1. Copy `core/project-template/openspec/` to `openspec/` and `addons/ci/python/test_openspec_rules.py` to your test folder.
2. Write changes with the AIP skills or the prompts.
3. Run `python3 test_openspec_rules.py`. Expect `OK`.

### AI FDE (situations 1 to 4)

1. Make a Compass folder. Save the four files in `core/aip-skills/` as skills (`docs/ai-fde.md`).
2. Copy `core/project-template/openspec/` into your Code Repository on a branch.
3. Load the OpenSpec Explore skill, then Propose. Commit.
4. Read Checks and fix what they name. With no gate (situation 1), a person reviews with the list in `docs/ai-fde.md` before merge.

## What a change contains

The `foundry-spec-driven` schema gives every change these files. They live in `openspec/changes/<name>/`. Write `proposal.md` first. After it, `open-questions.md`, the specs, `design.md`, `ontology.md` and `data.md` can be written in any order. `logic.md` needs `ontology.md`. `tasks.md` needs all the others.

| File | Holds |
| --- | --- |
| `proposal.md` | Why, the capabilities, and glossary changes (each term with its Ontology resources) |
| `open-questions.md` | Every knowledge gap: ID, stage, question, blocking, affects, owner, status, answer. Started with the proposal; every later file adds rows |
| `specs/<capability>/spec.md` | Behavior in Gherkin and glossary terms, with `Ontology: <ApiName>, <ApiName>` lines |
| `design.md` | Technical approach, with pointers to the three Foundry files |
| `ontology.md` | The data model: scope (space, owner), object types, link types (each tagged with its glossary term, with units and how links are stored), interfaces and shared properties, value types, the questions the model must answer, access, and a design review |
| `data.md` | Datasets (dataset, virtual table or model), transforms and pipelines, data quality checks |
| `logic.md` | Actions (rules, who may run them, side effects), functions (their edits and the function-backed action), writeback to other systems, AIP Logic and agents with evaluation cases |
| `tasks.md` | Checklist in dependency order, each task with a `Verify:` line |

Files that sit outside a change, in `openspec/`:

| File | Holds | Who edits it |
| --- | --- | --- |
| `config.yaml` | The schema name, project context and per-artifact rules every assistant follows | The team, rarely |
| `glossary.md` | Business terms, their Ontology resources and forbidden synonyms | The team, in the change that adds a term |
| `ontology-design.md` | Palantir's Ontology design rules and anti-patterns, condensed | The kit maintainer |
| `ontology.json` | Optional list of API names. Checks match every `Ontology:` name against it | The team, from an Ontology export |
| `schemas/foundry-spec-driven/` | The artifact graph, instructions and templates | The kit maintainer |
| `specs/`, `changes/` | Current specs, and open and archived changes | The team |

### Glossary, Ontology and design rules

A glossary term is a business concept, not an Ontology type. One term can be represented by several object types and link types, and one object type can serve several terms. The glossary row (`Ontology resources` column) lists all of them. `Ontology:` lines in a spec list the ones a requirement touches. Checks verify the names against `openspec/ontology.json`; whether the mapping is right is a review job. Details: `docs/glossary-and-ontology.md`.

The model in `ontology.md` and `logic.md` is checked against `openspec/ontology-design.md`, which condenses Palantir's design guidance: naming, one entity per object type, real relationships, interfaces, action design, security and eight anti-patterns. The "Design review" table in `ontology.md` records every rule a change breaks, why, and when to revisit it. No tool checks this. The assistant follows it and a reviewer reads it.

### Open questions are a gate

No tasks are written, and `apply` does not start, while a row in `open-questions.md` is blocking and open. A row is never deleted. Its status changes to `answered`, `assumed` (the assumption is written down) or `dropped`. Archive asks before closing a change that still has open or assumed rows.

Other Foundry artifacts we considered but did not build (access, app, automation, integration, rollout) are listed in `docs/glossary-and-ontology.md`.

## Gherkin scenarios and tasks

Specs and tasks are written in Gherkin: `GIVEN` (context), `WHEN` (one trigger), `THEN` (a result someone can see), `AND` / `BUT` to continue a step, and an `**Examples**` table when the same steps run with different data. It is a plain-language format that business, QA and developers can all read.

It is written inside the normal OpenSpec Markdown, not in separate `.feature` files. OpenSpec already requires every requirement to have `#### Scenario:` blocks with a `WHEN`/`GIVEN` and a `THEN` line, so Gherkin fits with no change to the validator and no new tool.

In a spec (`openspec/changes/<name>/specs/<capability>/spec.md`):

```
### Requirement: Approve a batch release
The system SHALL let a QA approver release a batch only when all tests pass.
Ontology: ApproveBatchRelease

#### Scenario: Release blocked by a failed test
- **GIVEN** a batch with a failed test
- **WHEN** the user approves the release
- **THEN** the system rejects the approval
- **BUT** the batch status stays In Review

#### Scenario: Release by role
- **GIVEN** a user with role <role>
- **WHEN** the user approves the release of a passed batch
- **THEN** the approval is <result>

**Examples**

| role | result |
| --- | --- |
| QA approver | accepted |
| Operator | rejected |
```

In `tasks.md`, each task has one indented `Verify:` line, in Gherkin or citing a scenario. The line is not a checkbox, so progress counting is unchanged:

```
- [ ] 1.1 Add the validateRelease function
  - **Verify:** GIVEN a batch with a failed test; WHEN validateRelease runs; THEN it returns an error.
- [ ] 2.1 Show the rejection on the release page
  - **Verify:** scenario "Release blocked by a failed test" of batch-release.
```

Rules the assistant follows: one behavior per scenario, exactly one `WHEN`, business language and glossary terms (no clicks, field ids or function names), cover the main path, each stated rule and at least one failure case. There is no `Background`: put shared context in the requirement text or repeat the `GIVEN`. Keep the keywords in English, because validation looks for them. The step text can be in any language.

## Where the rules are enforced

Nothing here needs a runner. The rules live in files that an assistant reads and follows.

| Layer | What it does | Who follows it |
| --- | --- | --- |
| `schemas/foundry-spec-driven/` | Templates and artifact instructions spell out the Foundry, Gherkin and design rules | Claude (CLI or MCP), Continue, anything that reads `openspec instructions` |
| `config.yaml` | `rules:` repeat them per artifact | Same |
| `core/aip-skills/` | Explore sketches, Propose writes, Apply acts out each `Verify:` line, Archive checks the scenarios still describe what was built | AI FDE, with no shell |
| OpenSpec validation (`--strict`, or its TypeScript or Python port) | Checks that each requirement has a scenario with a `WHEN`/`GIVEN` and a `THEN`. The glossary check adds forbidden synonyms and Ontology names. | CI, if you run it |

The limit is plain: validation does not check keyword order, a single `WHEN`, business wording, the `Examples` table, the design review or the open questions. The assistant follows those rules and a reviewer checks them. No Cucumber or Behave runner is shipped. If a team later automates, each spec scenario maps one to one to a `.feature` scenario.

## What is in the kit

```
palantir-foundry-openspec/
  core/         copy these: every team, every situation
  addons/       copy what your environment needs
  docs/         four guides
  maintainer/   build, test, provenance (in Git, not in the release zip)
  README.md  CHANGELOG.md  VERSION  LICENSE  THIRD_PARTY_NOTICES.md
```

| Folder | Use it when | Key contents |
| --- | --- | --- |
| `core/project-template/` | Always. It is the spec home a repo starts from | `openspec/` with `config.yaml`, `glossary.md`, `ontology-design.md`, the schema (the only copy), empty `specs/` and `changes/archive/` |
| `core/aip-skills/` | AI FDE, or any assistant without a shell (situations 1 to 4) | `openspec-explore.md`, `-propose.md`, `-apply.md`, `-archive.md`. No CLI calls. The skills read the config, glossary and design rules from the template |
| `addons/cli/` | Node 20+ and you want real validation | `openspec-1.16.0/` (bundled CLI), `launchers/` (sh and `.cmd`, telemetry off), `SHA256SUMS`, `PIN.md` (version, hashes, local patches), licence files |
| `addons/workspace/` | You use Continue or Claude Code | `.continue/` and `.claude/`: the four workflows plus the `openspec-sync-specs` skill, which archive runs. Generated; do not edit |
| `addons/ci/` | Your Checks can run Jest or Python | `typescript/` (`openspec.test.ts` runs the bundle; `openspec-rules.test.ts` is a pure TypeScript port with no child process; `glossary.test.ts`; `tsconfig.snippet.json`) and `python/test_openspec_rules.py`. All skip themselves in a repo whose config has `store:` |

| Guide | Covers |
| --- | --- |
| `docs/setup.md` | Every situation step by step, the CLI copy-in, what each check covers, what to confirm in Foundry |
| `docs/ai-fde.md` | AI FDE: Compass folder, skills, Checks, and the review list when no gate runs |
| `docs/glossary-and-ontology.md` | Concept versus resource, what Palantir's docs say and how the kit uses it, other artifacts considered |
| `docs/multi-repo.md` | One spec home for several repositories (stores), satellite config |

## Maintaining the kit

One person owns the kit (today: Optivia Labs). Work on a connected machine. The release zip is the only thing that crosses into the restricted network.

### The maintainer folder (in Git, not in the zip)

| Path | What it is for |
| --- | --- |
| `maintainer/scripts/` | `build.sh` (pinned dependency lock, `--release` zip), `sync-upstream.sh`, `make-workspace.py`, `setup-test-env.sh`, `pinned/` |
| `maintainer/tests/` | `run-all.sh`, `fixtures/` (valid and invalid), `allowed-urls.txt`, `jest-env/` (ignored, about 58 MB) |
| `maintainer/upstream/` | Untouched `init` output used to build `addons/workspace/` and to diff on upgrade, and the upstream licence |
| `maintainer/UPGRADE.md` | How to move to a new OpenSpec version |

### Where to change what

| To change | Edit | Then |
| --- | --- | --- |
| A rule for specs, tasks or a Foundry artifact | `core/project-template/openspec/schemas/foundry-spec-driven/` (instructions, templates), and the matching `rules:` in `config.yaml` | Update the same rule in `core/aip-skills/` by hand: the skills carry no CLI, so they do not read the schema |
| Ontology design guidance | `core/project-template/openspec/ontology-design.md` | Re-read Palantir's pages and keep the "read on" date in `docs/glossary-and-ontology.md`. Update the schema and skills only if a rule they repeat changed |
| A skill | `core/aip-skills/*.md` | Keep zero `openspec <command>` calls and 150 lines or fewer |
| Continue or Claude prompts | Never by hand. `addons/workspace/` is generated | Run `maintainer/scripts/make-workspace.py` |
| A check (Jest, TypeScript port, Python) | `addons/ci/typescript/` and `addons/ci/python/` together | Keep the messages the same in all three. Add a fixture in `maintainer/tests/fixtures/` with an `expected` file for bundle, jest and python |
| The bundle or OpenSpec version | Follow `maintainer/UPGRADE.md` | Rebuild and update `addons/cli/PIN.md` |

### Check the kit

`maintainer/tests/run-all.sh` runs every check and works offline. The Jest part needs `maintainer/scripts/setup-test-env.sh` once on a connected machine; `--no-jest` skips it.

### Release steps

1. Make the change. Run `maintainer/tests/run-all.sh`. All checks must pass.
2. Bump `VERSION`, then the version in `README.md` and `addons/cli/PIN.md` (`run-all.sh` fails if they disagree). Add a `CHANGELOG.md` entry.
3. If the artifact graph changed, raise `version:` in `schema.yaml` and say in the changelog what open changes must add. Adding an artifact changes the graph: agree it first.
4. Run `maintainer/scripts/build.sh --release`. It zips the top-level files, `docs/`, `core/` and `addons/`, and writes a `.sha256`. The zip cannot run `run-all.sh`. Check the zip against its `.sha256`, and the bundle against `SHA256SUMS`.
5. Send the zip and `.sha256` through the approved transfer. Tell teams to discard any earlier zip with the same version.

### Routine upkeep

| When | Do |
| --- | --- |
| Every quarter, and when Foundry ships a notable Ontology change | Re-read the Palantir pages listed in `docs/glossary-and-ontology.md`. Update `ontology-design.md` and the changelog |
| A new OpenSpec release | Follow `maintainer/UPGRADE.md`. Do not skip the diff of the generated skills |
| A team reports a rule the assistant ignores | Add a fixture if a check can catch it. Otherwise tighten the instruction, and say so in the changelog |
| Foundry or AI FDE changes names or menus | Fix `docs/ai-fde.md` and `docs/setup.md` ("What to confirm in Foundry") |
| A new artifact is requested (access, app, automation, rollout) | See `docs/glossary-and-ontology.md`. A new artifact changes the graph |

## Rules this kit keeps

- Nothing downloads anything at runtime. Telemetry is off in every launcher and test.
- No install scripts. No dependencies beyond Node (the bundled CLI) and the Python standard library (the Python check). The TypeScript port needs neither.
- The artifact order is fixed: proposal, then open questions, specs, design, ontology and data, then logic (after ontology), then tasks, then apply.
- No Palantir proprietary content, customer data or credentials.
- Specs and task checks are written in Gherkin. The assistant follows the rules; validation checks only the basics.
