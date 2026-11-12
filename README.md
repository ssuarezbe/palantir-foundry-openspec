# palantir-foundry-openspec

An internal kit of [OpenSpec](https://github.com/Fission-AI/OpenSpec) 1.16.0 for teams that build on Palantir Foundry in a network with no npm access. Version `1.16.0-foundry.5`, maintained by Optivia Labs.

It gives you three things: Foundry and Gherkin rules for specs (the core), skills and prompts for the tools you use in Foundry, and optional add-ons: a bundled OpenSpec CLI and a CI check.

This is not an official OpenSpec or Palantir product. "Palantir" and "Foundry" are trademarks of Palantir Technologies Inc. The kit is internal. If it is ever published, rename it (for example `foundry-openspec-kit`). OpenSpec is MIT licensed; see `THIRD_PARTY_NOTICES.md`.

## Pick a route

| Route | You have | You get | Doc |
| --- | --- | --- | --- |
| **A. Bundle** | Node 20+ on a laptop or in a Foundry VS Code workspace | CLI, Continue or Claude Code prompts, full validation | `docs/setup.md` |
| **B. Written rules** | No Node, but Python 3 | AIP skills, Python check | `docs/setup.md` |
| **C. AI FDE** | AI FDE only, no shell | AIP skills from a Compass folder, Checks on commit | `docs/ai-fde.md` |

Any route can use the CI gate: `docs/setup.md`. A product with several repositories keeps one set of specs in one "spec home": `docs/multi-repo.md`.

## How the pieces fit

Copy these into the Code Repository you work in:

| From this kit | To your repo | Route |
| --- | --- | --- |
| `addons/cli/` | `tools/openspec/` | A |
| `core/project-template/openspec/` | `openspec/` | A, B, C |
| `addons/workspace/.continue/` | `.continue/` | A (Continue) |
| `addons/workspace/.claude/` | `.claude/` | A (Claude Code) |
| one line, `store: <id>` | `openspec/config.yaml` of every other repo (see `docs/multi-repo.md`) | multi-repo |
| `addons/ci/typescript/*.test.ts` and `tsconfig.snippet.json` | your TypeScript test folder | gate |
| `addons/ci/python/test_openspec_rules.py` | your Python test folder | gate |
| `core/aip-skills/*.md` | a Compass folder (not the repo) | C |

## Quick start (about 10 minutes)

### Route A: Node 20+

1. Unzip the kit. Check the zip against its `.sha256` file. The zip has no test suite, so check the bundle too: from `addons/cli/` run `shasum -a 256 -c SHA256SUMS` (macOS) or `sha256sum -c SHA256SUMS` (Linux; on Windows compare `certutil -hashfile openspec-1.16.0\dist\cli\openspec.mjs SHA256` with the line in `SHA256SUMS`). Then run `./launchers/openspec --version` and expect `1.16.0`.
2. In your repo, copy `addons/cli/` to `tools/openspec/` and `core/project-template/openspec/` to `openspec/`. Copy `addons/workspace/.continue/` to `.continue/` (or `addons/workspace/.claude/` to `.claude/`).
3. Edit `openspec/config.yaml` if you need to. Fill in `openspec/glossary.md`: delete the two `Example:` rows and add your terms, each with the object, link and action types that represent it.
4. Check it works. On macOS or Linux: `./tools/openspec/launchers/openspec validate --all --strict --no-interactive`. On Windows: `tools\openspec\launchers\openspec.cmd validate --all --strict --no-interactive`. Expect `No items found to validate.`
5. In Continue, run `/opsx-propose` and describe a change. In Claude Code, run `/opsx:propose`.
6. Validate again with the same command. Commit on a branch.

### Route B: no Node, Python 3

1. Copy `core/project-template/openspec/` to `openspec/` and `addons/ci/python/test_openspec_rules.py` to your test folder.
2. Load the four skills from `core/aip-skills/` into your assistant (see `docs/ai-fde.md`), or follow them by hand.
3. Write a change with the OpenSpec Propose skill.
4. Run `python3 test_openspec_rules.py` from your test folder. Expect `OK`.

### Route C: AI FDE

1. Make a Compass folder. Save the four files in `core/aip-skills/` as skills. Follow `docs/ai-fde.md`.
2. Copy `core/project-template/openspec/` into your Code Repository on a branch.
3. Load the OpenSpec Explore skill, then Propose. Commit.
4. Read Checks. Fix what they name.

## What a change contains

The `foundry-spec-driven` schema gives every change these files. Each needs the ones above it. The first four after the proposal can be written in any order.

| File | Holds | Needs |
| --- | --- | --- |
| `proposal.md` | Why, capabilities, glossary changes (each term with its Ontology resources) | nothing |
| `open-questions.md` | Every knowledge gap, with ID, stage, blocking, owner, status, answer. Started with the proposal; every later file adds rows. | proposal |
| `specs/<capability>/spec.md` | Behavior in Gherkin and glossary terms, with `Ontology: <ApiName>, <ApiName>` lines | proposal |
| `design.md` | Technical approach, with pointers to the three Foundry files | proposal |
| `ontology.md` | The data model: scope (space, owner), object types, link types (each tagged with its glossary term, with units and how links are stored), interfaces and shared properties, value types, the questions the model must answer, access, and a design review against `ontology-design.md` | proposal |
| `data.md` | Datasets (dataset, virtual table or model), transforms and pipelines, data quality checks | proposal |
| `logic.md` | Actions (rules, who may run them, side effects), functions (their edits and the function-backed action), writeback to other systems, AIP Logic and agents with evaluation cases | `ontology.md` |
| `tasks.md` | Checklist in dependency order, each task with a `Verify:` line | all of the above |

Project files that sit outside a change, in `openspec/`:

| File | Holds | Who edits it |
| --- | --- | --- |
| `config.yaml` | The schema name, project context and per-artifact rules every assistant follows | The team, rarely |
| `glossary.md` | Business terms, their Ontology resources and forbidden synonyms | The team, in the change that adds a term |
| `ontology-design.md` | Palantir's Ontology design rules and anti-patterns, condensed | The kit maintainer (see "Maintaining the kit") |
| `ontology.json` | Optional list of API names; checks match every `Ontology:` name against it | The team, from an Ontology export |
| `schemas/foundry-spec-driven/` | The artifact graph, instructions and templates | The kit maintainer |
| `specs/`, `changes/` | Current specs, and open and archived changes | The team |

A glossary term is a business concept, not an Ontology type. One term can be represented by several object types and link types, and one object type can serve several terms. The glossary row (`Ontology resources` column) lists all of them; `Ontology:` lines in a spec list the ones a requirement touches. Checks verify the names against `openspec/ontology.json`; whether the mapping is right is a review job. Details: `docs/glossary-and-ontology.md`.

The model in `ontology.md` and `logic.md` is checked against `openspec/ontology-design.md`, which condenses Palantir's design guidance (naming, one entity per object type, real relationships, interfaces, action design, security, eight anti-patterns). The "Design review" table in `ontology.md` records every rule a change breaks, why, and when to revisit it. No tool checks this: the assistant follows it and a reviewer reads it.

Open questions are a gate: no tasks are written, and `apply` does not start, while a row is blocking and open. A row is never deleted; its status changes to `answered`, `assumed` or `dropped`. Other Foundry artifacts we considered (access, app, automation, integration, rollout) are listed in `docs/glossary-and-ontology.md`.

## Gherkin scenarios and tasks

Specs and tasks are written in Gherkin: `GIVEN` (context), `WHEN` (one trigger), `THEN` (a result someone can see), `AND` / `BUT` to continue a step, and an `**Examples**` table when the same steps run with different data. Gherkin is a plain-language format that business, QA and developers can all read.

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

### Where this is enforced

Foundry is a regulated place where running gates is hard, so the rules live in files that an assistant reads and follows. Nothing here needs a runner.

| Layer | What it does | Who follows it |
| --- | --- | --- |
| `core/project-template/openspec/schemas/foundry-spec-driven/` | Spec and task templates use Gherkin. The artifact instructions spell out the rules. | Claude (CLI or MCP), Continue, anything that reads `openspec instructions` |
| `core/project-template/openspec/config.yaml` | `rules:` repeat the Gherkin rules for specs and tasks. | Same |
| `core/aip-skills/` | Explore sketches scenarios. Propose writes them. Apply acts out each `Verify:` line and walks every scenario before it calls the change done. Archive checks the scenarios still describe what was built. | AI FDE, with no shell |
| OpenSpec validation (`--strict`, and the Python port) | Checks that each scenario has a `WHEN`/`GIVEN` and a `THEN`. This is the only automatic check. | CI, if you run it |

Be clear about the limit. The validator does not check keyword order, a single `WHEN`, business wording, or the `Examples` table. Those rules are followed by the assistant and checked in review. No Cucumber or Behave runner is shipped. If a team later automates, each spec scenario maps one to one to a `.feature` scenario.

Tested here: a Gherkin spec with outlines and `Verify:` tasks passes `validate --strict`; a scenario with no `THEN` fails in the bundle, Jest and the Python port; the config and schema parse cleanly. Not tested: whether AI FDE, Claude or Continue actually follow the Gherkin rules. Run a real change through each and read the output.

## What is in the kit

**Objective:** let teams on Foundry write specs the same way (OpenSpec, Gherkin, Ontology names, a glossary) with no npm access and no new repositories.

```
palantir-foundry-openspec/
  core/         copy these: every team, every route
  addons/       copy what your environment needs
  docs/         four guides
  maintainer/   build, test, provenance (in Git, not in the release zip)
  README.md  CHANGELOG.md  VERSION  LICENSE  THIRD_PARTY_NOTICES.md
```

### core/ (every team)

| Folder | Objective | Key artifacts |
| --- | --- | --- |
| `core/project-template/` | The spec home a repo starts from. | `openspec/config.yaml` (Foundry and Gherkin rules), `openspec/glossary.md`, `openspec/ontology-design.md` (Ontology design rules and anti-patterns), `openspec/schemas/foundry-spec-driven/` (the only copy of the schema), empty `specs/` and `changes/archive/` |
| `core/aip-skills/` | Run the workflow in AI FDE, with no shell. | `openspec-explore.md`, `-propose.md`, `-apply.md`, `-archive.md`. No CLI calls. |

The two are a pair: the skills read the config and glossary from the template.

### addons/ (one per environment)

| Folder | Use it when | Key artifacts |
| --- | --- | --- |
| `addons/cli/` | Node 20+ and you want real validation. | `openspec-1.16.0/` (bundled CLI), `launchers/` (sh and `.cmd`, telemetry off), `SHA256SUMS`, `PIN.md` (version, hashes, local patches), licence files |
| `addons/workspace/` | You use Continue or Claude Code. | `.continue/` and `.claude/`: four workflows plus the `openspec-sync-specs` skill (archive runs it). Generated; do not edit. |
| `addons/ci/` | Your Checks can run Jest or Python. | `typescript/` (`openspec.test.ts`, `glossary.test.ts`, `tsconfig.snippet.json`), `python/test_openspec_rules.py` |

### docs/

| File | Covers |
| --- | --- |
| `docs/setup.md` | Routes A and B, the CI gate, what to confirm in Foundry |
| `docs/ai-fde.md` | Route C: Compass folder, skills, Checks |
| `docs/glossary-and-ontology.md` | Concept versus resource, the Foundry files in a change, other artifacts considered |
| `docs/multi-repo.md` | One spec home for several repositories (stores), satellite config |

### maintainer/ (not for teams)

| Path | Objective | Key artifacts |
| --- | --- | --- |
| `maintainer/scripts/` | Build and refresh the kit. | `build.sh` (pinned lock, `--release` zip), `sync-upstream.sh`, `make-workspace.py`, `setup-test-env.sh`, `pinned/` |
| `maintainer/tests/` | Prove the kit, offline. | `run-all.sh`, `fixtures/` (valid and invalid), `allowed-urls.txt`, `jest-env/` (ignored, about 58 MB) |
| `maintainer/upstream/` | Baseline to diff on upgrade. | `generated/` (untouched `init` output), `OPENSPEC_LICENSE` |
| `maintainer/UPGRADE.md` | Move to a new OpenSpec version. | |

### Release zip

`maintainer/scripts/build.sh --release` zips the top-level files, `docs/`, `core/` and `addons/`, plus a `.sha256`. It cannot run `run-all.sh`; check the bundle with `shasum -a 256 -c SHA256SUMS` from `addons/cli/`.

## Maintaining the kit

One person owns the kit (today: Optivia Labs). Work on a connected machine. The release zip is the only thing that crosses into the restricted network.

### Where to change what

| To change | Edit | Then |
| --- | --- | --- |
| A rule for specs, tasks or a Foundry artifact | `core/project-template/openspec/schemas/foundry-spec-driven/` (instructions, templates), and the matching `rules:` in `config.yaml` | Update the same rule in `core/aip-skills/` by hand: the skills carry no CLI, so they do not read the schema |
| Ontology design guidance | `core/project-template/openspec/ontology-design.md` | Re-read Palantir's pages; keep the "read on" date in `docs/glossary-and-ontology.md`; update the schema and skills only if a rule they repeat changed |
| A skill | `core/aip-skills/*.md` | Keep zero `openspec <command>` calls and 150 lines or fewer |
| Continue or Claude prompts | Never by hand. `addons/workspace/` is generated | Run `maintainer/scripts/make-workspace.py` |
| A check (Jest, Python) | `addons/ci/typescript/` and `addons/ci/python/` together | Keep both messages the same. Add a fixture in `maintainer/tests/fixtures/` with an `expected` file for bundle, jest and python |
| The bundle or OpenSpec version | `maintainer/UPGRADE.md` | Rebuild, update `addons/cli/PIN.md` |

### Release steps

1. Make the change. Run `maintainer/tests/run-all.sh`. All checks must pass.
2. Bump `VERSION`, then the version in `README.md` and `addons/cli/PIN.md` (`run-all.sh` fails if they disagree). Add a `CHANGELOG.md` entry.
3. If the artifact graph changed, raise `version:` in `schema.yaml` and say in the changelog what open changes must add. Adding an artifact changes the graph: agree it first.
4. Run `maintainer/scripts/build.sh --release`. Check the zip against its `.sha256`, and the bundle against `SHA256SUMS`.
5. Send the zip and `.sha256` through the approved transfer. Tell teams to discard any earlier zip with the same version.

### Routine upkeep

| When | Do |
| --- | --- |
| Every quarter, and when Foundry ships a notable Ontology change | Re-read the Palantir pages listed in `docs/glossary-and-ontology.md`. Update `ontology-design.md` and the changelog |
| A new OpenSpec release | Follow `maintainer/UPGRADE.md`. Do not skip the diff of the generated skills |
| A team reports a rule the assistant ignores | Add a fixture if a check can catch it. Otherwise tighten the instruction, and say so in the changelog |
| A feature of Foundry or AI FDE changes names or menus | Fix `docs/ai-fde.md` and `docs/setup.md` ("What to confirm in Foundry") |
| A candidate artifact is requested (access, app, automation, rollout) | See `docs/glossary-and-ontology.md`. A new artifact changes the graph |

### Not yet verified

Nothing in the kit has run inside Foundry. No model has been run against the Gherkin, Foundry or design rules. Tested on Node 20.19.3 only. Before a wider rollout, run one real change through AI FDE and one through Claude or Continue, and read the output.

## Rules this kit keeps

- Nothing downloads anything at runtime. Telemetry is off in every launcher and test.
- No install scripts. No dependencies beyond Node (route A) and the Python standard library.
- The artifact order is fixed: proposal, then specs, design, ontology, data and open questions (logic after ontology), then tasks, then apply.
- No Palantir proprietary content, customer data or credentials.
- Specs and task checks are written in Gherkin. The assistant follows the rules; the validator checks only the basics.

## Check the kit

`maintainer/tests/run-all.sh` runs every check and works offline. The Jest part needs `maintainer/scripts/setup-test-env.sh` once on a connected machine. `maintainer/UPGRADE.md` covers new OpenSpec versions. `maintainer/scripts/build.sh --release` makes the lean transfer zip.
