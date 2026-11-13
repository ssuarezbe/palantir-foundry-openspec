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
7. Prepare the repository: on a branch, add `openspec/` from `core/project-template/openspec/`. The skills expect `openspec/config.yaml` and `openspec/glossary.md`.
8. Work in this order: Explore, Propose, Apply, Archive. Each skill tells the assistant to use a branch, never commit to main and read Checks after each commit.
9. Update a skill when the kit changes: repeat step 2 with Save as over the old one.

## How the skills behave

- Explore reads the config, glossary, specs and open changes, and confirms each Ontology API name exists. It writes nothing.
- Propose creates `openspec/changes/<name>/` with `.openspec.yaml`, then writes proposal, open questions, specs, design, ontology, data, logic and tasks in that order, checking its own output against the validation rules.
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

Items 1 to 4 are what the automatic checks apply in the other situations. Add a gate later (situation 2, 3 or 4) and these four stop depending on a person.

## What to confirm in Foundry

- The menu names in step 2 to 6 in your enrolment.
- Any size limit on a skill. The longest skill here is 139 lines.
- That AI FDE can read Checks results and the commit's failing file and line.
- That AI FDE can move a folder and edit many files in one commit (Archive needs it). If it cannot, do the archive step by hand.
- Whether AI FDE can reach the Ontology tools the Explore skill names, or needs `openspec/ontology.json`.
