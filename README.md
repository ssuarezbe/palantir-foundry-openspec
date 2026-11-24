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

## Prompt templates for AI FDE only

Save `core/aip-skills/` as skills in a Compass folder and copy `core/project-template/openspec/` into your repository on a branch (`docs/ai-fde.md`). Markdown lives only in the Code Repository, not in Compass or Notepad. AI FDE tends to skip artifacts it is not told about, so each template names every file in its first prompt. Replace the `<...>` parts. Neither is tested with a model: a person reviews what it writes.

### Template 1: existing code to OpenSpec

Use it on a repository that already works and has no specs. It writes the baseline, not a change.

```text
Load the OpenSpec Explore skill. Read-only for code. Do not create a change.
This repository has working code and no specs. The kit is in openspec/.

Read first: openspec/config.yaml, openspec/ontology-design.md, openspec/rulebook/README.md.
Then read the code in <folders, e.g. functions-typescript/src, transforms-python/src>.

Write only what the code shows. Mark any guess "unconfirmed". Never invent rules,
owners or classifications. Write these files:
1. openspec/glossary.md: one row per business concept, with a definition.
2. openspec/specs/<capability>/spec.md, one per capability: Purpose of at least 50
   characters, requirements with SHALL, GIVEN/WHEN/THEN scenarios, an `Ontology:` line.
3. openspec/INDEX.md: a Capabilities row per spec, a Resources row per API name
   (object type, link type, action, function, dataset, automation).
4. openspec/ontology.json: the API names you found, if that file is empty.

Do not write change artifacts now. Later changes hold seven: proposal, open-questions,
specs, design, ontology, logic, tasks.
Finish with: the files you wrote, and a list of what a person must confirm.
```

### Template 2: OpenSpec as the build plan

Use it for new work. The spec files are the plan, and the code follows `tasks.md`.

```text
Load the OpenSpec Explore skill, then Propose. We build <feature, in business words>.
Use OpenSpec as the build plan. The kit is in openspec/. Work on a branch.

Read first: openspec/INDEX.md, openspec/glossary.md, openspec/rulebook/README.md,
openspec/ontology-design.md, openspec/config.yaml. Name what exists and which rules apply.

Create openspec/changes/<kebab-case-name>/ with all seven artifacts, in this order:
1. proposal.md  2. open-questions.md  3. specs/<capability>/spec.md  4. design.md
5. ontology.md  6. logic.md  7. tasks.md
Rules: glossary terms in specs, Ontology resources by API name, GIVEN/WHEN/THEN scenarios,
a `classification:` line per object type and dataset, a Rulebook review table in
design.md citing rule IDs, a `Verify:` line on every task. Add a row for this change
to the In flight table in openspec/INDEX.md.
If a question blocks, mark it "yes" in open-questions.md, do not write tasks.md,
and list the questions for me.
Finish with: the files in the change folder, and which of the seven are missing.
Write no code.
```

Then answer the questions in `open-questions.md`, ask Propose to finish `tasks.md`, and continue with these short prompts, each with its skill loaded:
- `Load OpenSpec Apply. Implement openspec/changes/<name>/tasks.md one task at a time, run each Verify line, tick it off, follow the Rulebook review. Stop if a task needs something the artifacts do not say.`
- `Load OpenSpec Archive. Archive <name>: check the Rulebook review still matches what was built, update the main specs, the glossary and INDEX.md, move the change to openspec/changes/archive/.`

Without a gate (situation 1), review the change with the list in `docs/ai-fde.md` before Apply and before you merge.

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
