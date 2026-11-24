# palantir-foundry-openspec

Write down a Foundry change before you build it: why, the behavior, the Ontology types, actions and datasets it touches, and what is still unknown. An assistant writes the files, a person reviews them, then the assistant builds from them.

This is an internal [OpenSpec](https://github.com/Fission-AI/OpenSpec) 1.16.0 kit for teams on Palantir Foundry with no npm access. It brings Foundry-specific templates, skills for AI FDE (no shell, no Node), a company rulebook slot, and an optional bundled CLI and checks. Version `1.16.0-foundry.8`, by Optivia Labs.

Not an official OpenSpec or Palantir product. "Palantir" and "Foundry" are trademarks of Palantir Technologies Inc. OpenSpec is MIT licensed (`THIRD_PARTY_NOTICES.md`).

**Tested:** offline on Node 20.19.3, the CLI, the schema, 30 fixtures and three checks that agree (`maintainer/tests/run-all.sh`). **Not tested:** anything inside Foundry, and any AI model on these rules. Before a wider rollout, run one real change through AI FDE and read what it writes.

## Pick your situation

Every situation uses the same files (`core/`). They differ in what checks the specs automatically. Steps for each: `docs/setup.md`.

| # | You have | Copy | Checked automatically |
| --- | --- | --- | --- |
| 1 | **AI FDE only.** No shell, no Node, Checks run no tests | `core/` | Nothing. A person uses the review list in `docs/ai-fde.md` |
| 2 | **TypeScript repo, Jest can start a child process** | `core/`, `addons/cli/`, two test files | Full OpenSpec validation plus the glossary, index and rulebook checks |
| 3 | **TypeScript repo, no child process or unknown Node** | `core/`, two test files | A TypeScript port of the same rules |
| 4 | **Python repo, no Node** | `core/`, one test file | The same rules in Python |
| 5 | **Laptop or Foundry VS Code workspace, Node 20+** | `core/`, `addons/cli/`, `addons/workspace/` | What you run: `validate --strict` |
| 6 | **Several repositories, one product** | one spec home, one line elsewhere | As in the spec home |

Situations combine. The release zip has `drop-in/`, one ready folder per situation to copy over your repository root. Not sure which you are? Commit `drop-in/probe/tests/probe.test.ts` alone, read the Checks log, then delete it. A filled-in change is in `docs/example/`.

## Examples with AI FDE only

Save `core/aip-skills/` as skills in a Compass folder and copy `core/project-template/openspec/` into your repository (`docs/ai-fde.md`). Then use a prompt below. Neither is tested with a model.

### Prompt: document existing code (start from a repository that already works)

The kit has no skill for this. The prompt below uses the Explore skill to read, then asks AI FDE to write the baseline files by hand. Not tested with a model: review every file it writes.

```text
Load the OpenSpec Explore skill. This repository already has working code and no specs.
The kit is in openspec/ (copied from core/project-template/). Do not create a change.

1. Read openspec/config.yaml, openspec/ontology-design.md and openspec/rulebook/README.md.
2. Read the code under <folders, e.g. functions-typescript/src, transforms-python/src>.
   List the object types, link types, actions, functions and datasets you find, by API name.
   Say which you could not confirm from the code.
3. Write these, using only what the code shows:
   - openspec/glossary.md: one row per business concept, with a definition.
   - openspec/specs/<capability>/spec.md: one per capability. A Purpose of at least 50
     characters, requirements, GIVEN/WHEN/THEN scenarios, and an `Ontology:` line.
   - openspec/INDEX.md: one Resources row per API name, and one Capabilities row each.
4. Mark every guess "unconfirmed". Do not invent rules, owners or classifications.
5. End with a list of what I must confirm. Do not edit code.
```

Then commit on a branch, have a person confirm the "unconfirmed" items, and load Propose for the first real change.

### Prompt: write a new feature with AI FDE only

Run the four skills in order. Start each in a new chat, so the repository files carry the context.

```text
1. Load OpenSpec Explore.
   "I want <feature, in business words>. Read openspec/INDEX.md, the glossary and the
   rulebook. Tell me what exists, what overlaps and which rules apply. Write nothing."

2. Load OpenSpec Propose.
   "Create the change <kebab-case-name> for what we just discussed. Write the artifacts in
   order: proposal, open-questions, specs, design, ontology, logic, tasks. Cite rulebook
   rule IDs in the Rulebook review. Stop at tasks.md if a blocking question is open and
   list the questions for me."

   Answer the questions in openspec/changes/<name>/open-questions.md. Commit. Ask Propose
   to finish tasks.md.

3. Load OpenSpec Apply.
   "Implement openspec/changes/<name>/tasks.md. Do one task at a time, run its Verify
   line and tick it off. Follow the Rulebook review. Stop and ask if a task needs
   something the artifacts do not say."

4. Load OpenSpec Archive.
   "Archive <name>. Check the Rulebook review rows still match what was built, update
   the main specs, the glossary and openspec/INDEX.md, then move the change to
   changes/archive/."
```

Without a gate (situation 1), review the change with the list in `docs/ai-fde.md` before step 3 and before you merge.

## Guides

| Guide | Covers |
| --- | --- |
| `docs/setup.md` | Every situation step by step, the CLI copy-in, what each check covers, what to confirm in Foundry |
| `docs/ai-fde.md` | AI FDE: Compass folder, skills, Checks, the review list when no gate runs |
| `docs/how-it-works.md` | The four steps, the files in a change, open questions, where the rules are enforced |
| `docs/gherkin.md` | Scenario and task style |
| `docs/glossary-and-ontology.md` | Business term versus Ontology resource, and how the kit uses Palantir's design guidance |
| `docs/rulebook.md` | The company rulebook: fill it in and customize it |
| `docs/index-options.md` | `openspec/INDEX.md`, the agent map: upkeep with no code, and options to replace it |
| `docs/multi-repo.md` | One spec home for several repositories |

Folders: `core/` (every team copies), `addons/` (per environment), `docs/`, `maintainer/` (build and test, not in the release zip; `maintainer/README.md`).
