# AI FDE skills

AI FDE has no shell and no Node, so it uses the four files in `core/aip-skills/`. This guide covers situation 1 of `docs/setup.md` (no gate) and the AI FDE side of situations 2 to 4.
Each is a skill: a `Name:` line, a `Description:` line, then a Markdown body. None calls a CLI.
Not tested here: everything in this guide. The menu names below follow the build brief and may differ in your Foundry version.

## Steps

1. Make a Compass folder for the skills, for example `OpenSpec skills`. Give your team read access.
2. Open one file from `core/aip-skills/`. For each, in AIP:
   1. Choose Create new skill.
   2. Paste the `Name:` value as the name and the `Description:` value as the description.
   3. Paste the Markdown body.
   4. Choose Save as and save it into the Compass folder.
3. Do this for all four: Explore, Propose, Apply, Archive.
4. Open Manage skill set. Add the four skills to one skill set named `OpenSpec`.
5. In AI FDE, choose Load skills and pick the `OpenSpec` skill set.
6. Optional: make a pre-fill link that opens AI FDE on your Code Repository branch with the skill set loaded. Share it with the team.
7. Prepare the repository: on a branch, add `openspec/` from `core/project-template/openspec/`. The skills expect `openspec/config.yaml` and `openspec/glossary.md`. A person does this: nothing in Foundry holds the kit. AI FDE sees only what is added to the chat, so in each chat add the repository link and the branch as context, then paste the context block from the README.
8. Work in this order: Explore, Propose, Apply, Archive. Each skill tells the assistant to use a branch, never commit to main and read Checks after each commit.
9. Update a skill when the kit changes: repeat step 2 with Save as over the old one.

## Where Markdown lives

Foundry's Compass overview and Notepad overview do not say Markdown is supported, and we are told Compass does not preview or edit Markdown out of the box. Not confirmed in the docs: check your enrollment. Two places hold `openspec/`:

| Content | Put it in | Why |
| --- | --- | --- |
| `openspec/` (specs, changes, glossary, `INDEX.md`, rulebook) | **A.** A Code Repository (recommended) | Markdown, history, branches, pull request review, and Checks if you add a gate (situations 2 to 4) |
| `openspec/` | **B.** A Compass folder of uploaded files | Works with no repository. No diff, no branch, no gate: situation 1 only. Set `Branch: none` in the context block (README) |
| The four skills | Pasted into AIP skills, saved in a Compass folder | Compass holds the saved skill, not a `.md` file. The `.md` files in `core/aip-skills/` stay the source of truth in Git |
| Company policy documents | Wherever the owners keep them | Digest them into `openspec/rulebook/` (`docs/rulebook.md`) |

Implications:

- In A, anyone who reviews or edits a spec, or a rulebook row, needs Code Repository access and a pull request. In B they need access to the Compass folder. Data governance and cloud security may not have it. Give them read access, or send them a rendered copy.
- Notepad is a rich-text editor for people. It is not a store for these files: no branches, no review, no checks, and an assistant cannot read it as a file. Use it for readable summaries if you like, never as the source.
- A copy of the glossary or rulebook outside the repository goes stale. Keep one copy, in the repository or the Compass folder.

## How the skills behave

- Explore reads the config, glossary, specs and open changes, and confirms each Ontology API name exists. It writes nothing.
- Propose creates `openspec/changes/<name>/` with `.openspec.yaml`, then writes proposal, open questions, specs, design, ontology, logic and tasks in that order, checking its own output against the validation rules.
- Apply works through `tasks.md`, ticks each box, commits and reads Checks.
- Archive asks for a clear yes, merges the delta specs into `openspec/specs/<capability>/spec.md` in the order RENAMED, REMOVED, MODIFIED, ADDED, then moves the change to `openspec/changes/archive/YYYY-MM-DD-<name>/`.

## Review by hand when no gate runs

If Checks run no tests on the specs (situation 1), nothing checks what AI FDE writes. A reviewer reads each change before merge and checks:

1. Every requirement has `SHALL` or `MUST` and at least one `#### Scenario:` (four `#`).
2. Every scenario has a `GIVEN` or `WHEN` line and a `THEN` line, in bold capitals, with exactly one `WHEN`.
3. The change has at least one spec file, or `.openspec.yaml` says `skip_specs: true`.
4. No forbidden synonym from `openspec/glossary.md` appears in a spec. Every glossary term has a definition.
5. Every `Ontology:` name, and every name in the glossary Ontology resources column, exists in Ontology Manager.
6. `ontology.md` has a "Design review" table filled in against `openspec/ontology-design.md`.
7. No row in `open-questions.md` is blocking and open before `tasks.md` or any code.
8. Every task has a `Verify:` line, and each task's checkbox is ticked only when its `Verify:` line was acted out.
9. A change that touches `openspec/specs/` or `openspec/changes/archive/` also changes `openspec/INDEX.md` in the same pull request (the diff shows it), with API names only. Check the `Last audited:` date: older than a month or a release, ask for the Explore skill's "Audit the index".
10. `design.md` has a `## Rulebook review` with one row per applicable rule in `openspec/rulebook/`. Spot-check two rows against the rule text. A `must` deviation has an answered open question. Every object type and dataset has a `classification:` line, and Access matches the classification map.

Items 1 to 4 and the index names in item 9 are what the automatic checks apply in the other situations. Add a gate later (situation 2, 3 or 4) and these four stop depending on a person.

## What to confirm in Foundry

- The menu names in step 2 to 6 in your enrolment.
- Any size limit on a skill. The longest skill here is 144 lines.
- That AI FDE can read Checks results and the commit's failing file and line.
- That AI FDE can move a folder and edit many files in one commit (Archive needs it). If it cannot, do the archive step by hand.
- Whether AI FDE can reach the Ontology tools the Explore skill names, or needs `openspec/ontology.json`.
