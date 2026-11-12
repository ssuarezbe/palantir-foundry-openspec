# palantir-foundry-openspec

An internal kit of [OpenSpec](https://github.com/Fission-AI/OpenSpec) 1.16.0 for teams that build on Palantir Foundry in a network with no npm access. Version `1.16.0-foundry.4`, maintained by Optivia Labs.

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

1. Unzip the kit. Check the zip against its `.sha256` file.
2. In your repo, copy `addons/cli/` to `tools/openspec/` and `core/project-template/openspec/` to `openspec/`. Copy `addons/workspace/.continue/` to `.continue/` (or `addons/workspace/.claude/` to `.claude/`).
3. Edit `openspec/config.yaml` if you need to. Fill in `openspec/glossary.md`: delete the two `Example:` rows and add your terms.
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

Two folders deliver the value: **`core/project-template/`** and **`core/aip-skills/`**. They are a pair. The skills tell the assistant to read the config and glossary in the template. Everything in `addons/` is for one environment. Everything in `maintainer/` is for whoever builds the kit.

```
palantir-foundry-openspec/
  core/         what every team copies
  addons/       copy only what your environment needs
  maintainer/   build, test, provenance (in Git, not in the release zip)
  docs/         four guides
  README.md  CHANGELOG.md  VERSION  LICENSE  THIRD_PARTY_NOTICES.md
```

### core/ (copy these)

| Folder | Size | What it gives |
| --- | --- | --- |
| `core/project-template/` | 44K | The spec home: `openspec/config.yaml` (Foundry and Gherkin rules), `glossary.md`, and the `foundry-spec-driven` schema. The schema lives only here. Needed by every route. |
| `core/aip-skills/` | 28K | Four skills (explore, propose, apply, archive) with no CLI calls. This is what AI FDE uses. |

### addons/ (copy the ones your environment needs)

| Folder | Size | Use it when | Note |
| --- | --- | --- | --- |
| `addons/cli/` | 3.1M | You have Node 20+ (laptop, VS Code workspace, Claude via MCP) and want real validation. | The largest folder. Holds the bundle, launchers, `SHA256SUMS`, `PIN.md` and the bundled-package licences. |
| `addons/workspace/` | 336K | You use Continue or Claude Code. | Four workflows: explore, propose, apply, archive. It also holds the `openspec-sync-specs` skill, because the archive skill runs it inline. |
| `addons/ci/` | 28K | Your Checks can run Jest or Python. | Optional. In many Foundry setups gates are hard to run; the rules do not depend on it. |

### maintainer/ (not for teams)

| Folder | What it is for |
| --- | --- |
| `maintainer/scripts/` | Build the bundle (`build.sh`, from a pinned dependency lock), regenerate `addons/workspace/`, sync a new OpenSpec version. |
| `maintainer/tests/` | Fixtures and `run-all.sh`. The ignored Jest harness adds about 58 MB locally. |
| `maintainer/upstream/` | The untouched `init` output used to build `addons/workspace/` and to diff on upgrade, and the upstream licence. |
| `maintainer/UPGRADE.md` | How to move to a new OpenSpec version. |

### Release zip

`maintainer/scripts/build.sh --release` builds a lean zip: the top-level files, `docs/`, `core/` and `addons/`. Maintainer files stay in Git. The zip cannot run `run-all.sh`; check the bundle in it with `shasum -a 256 -c addons/cli/SHA256SUMS` from `addons/cli/`.

### Structure history

In `1.16.0-foundry.3` the kit had 11 top-level folders that had grown one feature at a time, a duplicate copy of the schema, a one-file `satellite-template/`, seven overlapping guides and a workspace with six workflows. `1.16.0-foundry.4` grouped the folders by audience, kept one copy of the schema, folded the satellite config into `docs/multi-repo.md`, cut the guides to four, trimmed the workspace to four workflows and made the zip lean. Every consumer path changed; see `CHANGELOG.md`.

## Rules this kit keeps

- Nothing downloads anything at runtime. Telemetry is off in every launcher and test.
- No install scripts. No dependencies beyond Node (route A) and the Python standard library.
- The artifact order is fixed: proposal, then specs and design, then tasks, then apply.
- No Palantir proprietary content, customer data or credentials.
- Specs and task checks are written in Gherkin. The assistant follows the rules; the validator checks only the basics.

## Check the kit

`maintainer/tests/run-all.sh` runs every check and works offline. The Jest part needs `maintainer/scripts/setup-test-env.sh` once on a connected machine. `maintainer/UPGRADE.md` covers new OpenSpec versions. `maintainer/scripts/build.sh --release` makes the lean transfer zip.
