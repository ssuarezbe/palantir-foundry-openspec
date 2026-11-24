# palantir-foundry-openspec

Write down a Foundry change before you build it: why, the behavior, the Ontology types, actions and datasets it touches, and what is still unknown. An assistant writes the files, a person reviews them, then the assistant builds from them.

This is an internal [OpenSpec](https://github.com/Fission-AI/OpenSpec) 1.16.0 kit for teams on Palantir Foundry with no npm access. It brings Foundry-specific templates, skills for AI FDE (no shell, no Node), a company rulebook slot, and an optional bundled CLI and checks. Version `1.16.0-foundry.10`, by Optivia Labs.

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

AI FDE only sees what is added to the chat ([docs](https://www.palantir.com/docs/foundry/ai-fde/navigation/)). It cannot find `openspec/` by itself, and nothing in Foundry has the kit until a person puts it there. If you skip Step 0, it asks you to paste files.

**Where `openspec/` lives: a Code Repository, never a Compass folder.** Compass holds only the saved skills. A Compass folder of uploaded files has no branch, diff or review, no undo, no Checks and no Markdown preview, and it is not confirmed that AI FDE can edit those files. The skills assume branches, commits and Checks. A repository gives review, history, gates (situations 2 to 4 in `docs/setup.md`) and a split-pane Markdown preview for reviewers. No repository for this yet? Create one only for specs, holding just `openspec/`. Not confirmed that Foundry allows a repository with no code template.

**Step 0, once per project and once per chat**
1. A person commits `openspec/` (from `core/project-template/openspec/`, or `drop-in/situation-1/`) to a branch of a Code Repository.
2. Save `core/aip-skills/` as skills in a Compass folder and put them in one skill set, `OpenSpec` (`docs/ai-fde.md`). That folder holds only the saved skills, not the spec files.
3. In a new AI FDE chat, add the repository and the branch as context: drag the repository link in, add the branch from the ribbon. Not confirmed that a repository link can be attached: Prompt 0 shows it.
4. Paste the context block, then a prompt below.

**Context block** (replace the `<...>` values, keep the rest; the Compass paths are the variables)

```text
CONTEXT
Repository: <COMPASS_REPO: Compass path or link of the Code Repository, e.g. /Acme/Logistics/shipments-functions>
Branch:     <BRANCH: a feature branch, never main>
Skill set:  OpenSpec (saved in <COMPASS_SKILLS_FOLDER, e.g. /Acme/Logistics/OpenSpec skills>)
Spec home:  openspec/ at the root of the repository above

Every path below is relative to that repository on that branch. Open openspec/config.yaml
first. If you cannot open it, stop. Say what you tried and which context I must add
(repository link, branch). Do not ask me to paste files. Do not rebuild them from memory.

openspec/
  config.yaml  INDEX.md  glossary.md  ontology-design.md
  rulebook/    README.md, governance.md, security.md, infrastructure.md
  schemas/foundry-spec-driven/   schema.yaml, templates/ (seven files)
  specs/<capability>/spec.md     changes/<name>/ (seven artifacts)     changes/archive/
```

AI FDE tends to skip artifacts it is not told about, so each template names every file. Replace the other `<...>` parts. None of this is tested with a model: a person reviews what it writes.

### Prompt 0: preflight (run first)

```text
CONTEXT block above. Do not write anything. Report:
1. Which OpenSpec skills you loaded (Explore, Propose, Apply, Archive). List any missing.
2. Whether you can open openspec/config.yaml in the repository and branch above. If not,
   say which resource you could not open, and stop. If openspec/ is missing, say a person
   must commit core/project-template/openspec/ there.
3. The tree you see under openspec/, compared with the map. List what is missing.
4. Whether glossary.md and rulebook/ hold only `Example:` rows (then they are not filled in yet).
5. Whether you can read Checks results and the Ontology tools, or need openspec/ontology.json.
6. The branch you are on. If it is main, say so.
End with "Ready" or the list of what to fix.
```

### Template 1: existing code to OpenSpec

Use it on a repository that already works and has no specs. It writes the baseline main specs, not a change. Do one area per prompt.

```text
CONTEXT block above. First say which OpenSpec skills you loaded. If Explore is not one, stop.
Use OpenSpec Explore to read. This task overrides its "do not write" rule for the files
listed below only. Write no code and create no change. The kit is in openspec/. Work on a branch.

Read: openspec/config.yaml, openspec/ontology-design.md, openspec/rulebook/README.md.
Then read the code in <area, e.g. functions-typescript/src/shipments>.
Write only what the code shows. Mark any guess "unconfirmed". Never invent rules,
owners or classifications.

Write:
1. openspec/glossary.md: one row per business concept, with a definition. Keep its
   headers (openspec/glossary.md already has them).
2. openspec/specs/<capability>/spec.md, one per capability, in main-spec form:
   `# <capability> Specification`, `## Purpose` (50+ characters), `## Requirements`,
   then `### Requirement:` blocks with SHALL, an `Ontology:` line and
   `#### Scenario:` blocks with GIVEN, one WHEN and THEN. No ADDED/MODIFIED headings.
   (Do not copy templates/spec.md: that is the change form.)
3. openspec/INDEX.md: a Capabilities row per spec, a Resources row per API name
   (object type, link type, action, function, dataset, automation), then set Last audited.

Finish with: the files you wrote, and what a person must confirm.
```

Changes later hold seven artifacts (below). Review the baseline, then commit.

### Template 2: OpenSpec as the build plan

Use it for new work. The spec files are the plan, and the code follows `tasks.md`. If the idea is still unclear, first run `CONTEXT block above. Load OpenSpec Explore. I want <idea>. Read INDEX.md, the glossary and the rulebook, and tell me what exists and which rules apply.`

```text
CONTEXT block above. First say which OpenSpec skills you loaded. If Propose is not one, stop.
Load OpenSpec Propose. We build <feature, in business words>. Use OpenSpec as the build
plan. The kit is in openspec/. Work on a branch. Write no code.
Follow the skill. This list is a checklist, not a replacement for it.

Templates and rules: openspec/schemas/foundry-spec-driven/ holds schema.yaml and
templates/. Open the template for every file you write and keep its headers exactly:
the checks read them.

Create openspec/changes/<kebab-case-name>/ with .openspec.yaml and all seven artifacts:
1. proposal.md  2. open-questions.md  3. specs/<capability>/spec.md  4. design.md
5. ontology.md  6. logic.md  7. tasks.md
Include: glossary terms in specs, Ontology resources by API name, GIVEN/WHEN/THEN
scenarios, a `classification:` line per object type and dataset, a Rulebook review table
in design.md citing rule IDs, a `Verify:` line on every task, and an In flight row in
openspec/INDEX.md.
If a question blocks, mark it "yes" in open-questions.md, do not write tasks.md,
and list the questions for me.
Finish with: the files in the change folder, and which of the seven are missing.
```

Then continue with short prompts, each with its skill loaded:
- **Answer.** Answer the rows in `openspec/changes/<name>/open-questions.md`, commit, then `Load OpenSpec Propose. Finish tasks.md for <name>.`
- **Review (before Apply, and before merge).** Without a gate, nothing else checks the files:
  `CONTEXT block above. Do not edit. Review openspec/changes/<name>/ against the review list in docs/ai-fde.md (items 1 to 10) and the checklists in the Propose skill. For each item say pass or fail, with the file and line. Name the headers that differ from the templates, any forbidden synonym, any Ontology name you could not confirm, any blocking open row, and any task without a Verify line.`
- **Apply.** `CONTEXT block above. Load OpenSpec Apply. Implement openspec/changes/<name>/tasks.md one task at a time, run each Verify line, tick it off, follow the Rulebook review. Stop if a task needs something the artifacts do not say.`
- **Archive.** `CONTEXT block above. Load OpenSpec Archive. Archive <name>: check the Rulebook review still matches what was built, update the main specs, the glossary and INDEX.md, move the change to openspec/changes/archive/.`
- **Resume, in any new chat.** `CONTEXT block above. Do not edit. Read openspec/INDEX.md and list openspec/changes/ (skip archive/). For each open change give its stage (which of the seven files exist, tasks done of total, blocking open rows) and the next prompt I should run.`

Start every chat afresh: the repository files carry the context, not the chat. Without a gate (situation 1), the Review prompt is a model's read, not a gate: a person still reads the change before merge.

## Guides

| Guide | Covers |
| --- | --- |
| `docs/setup.md` | Every situation step by step, the CLI copy-in, what each check covers, what to confirm in Foundry |
| `docs/ai-fde.md` | AI FDE: skills in Compass, the repository, Checks, the review list when no gate runs |
| `docs/how-it-works.md` | The four steps, the files in a change, open questions, where the rules are enforced |
| `docs/gherkin.md` | Scenario and task style |
| `docs/glossary-and-ontology.md` | Business term versus Ontology resource, and how the kit uses Palantir's design guidance |
| `docs/rulebook.md` | The company rulebook: fill it in and customize it |
| `docs/index-options.md` | `openspec/INDEX.md`, the agent map: upkeep with no code, and options to replace it |
| `docs/multi-repo.md` | One spec home for several repositories |

Folders: `core/` (every team copies), `addons/` (per environment), `docs/`, `maintainer/` (build and test, not in the release zip; `maintainer/README.md`).
