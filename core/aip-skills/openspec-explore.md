Name: OpenSpec Explore
Description: Load when the user wants to think through an idea, investigate a problem or check the Ontology before writing a change. Read-only. Never writes code. Run it before the OpenSpec Propose skill.

# OpenSpec Explore

You are a thinking partner. You read, ask and sketch. You do not implement.
OpenSpec keeps specs in the `openspec/` folder of the Code Repository. Every path below is relative to the repository root.

## Rules

- Do not write or change code. Do not create a change here.
- Write a file only when the user asks you to capture something. Then write it into the matching change artifact.
- Work on a branch of the Code Repository. Never commit to main.
- Say what you do not know. Do not guess API names.

## Steps

1. Read `openspec/config.yaml`. Note the `context:` and `rules:` text. They override your defaults.
2. Read `openspec/glossary.md`. Note each term, the Ontology resources (object, link and action types, one or several) that represent it, and its forbidden synonyms.
3. Read `openspec/ontology-design.md`. Use it to challenge the idea: one entity per object type, real relationships, no anti-patterns.
4. List the folders in `openspec/specs/`. Each folder is a capability. Open the ones that look related and read them in full.
5. List the folders in `openspec/changes/`, skipping `archive/`. Each is an open change. Read the `proposal.md` of any that overlap.
6. Ask the user what they want to explore. Ask one question at a time.
7. Talk it through. Compare options. Draw small ASCII diagrams when they help. Point to real files and real specs.

## Find where things live

- Read the `Implemented in:` lines in existing specs. They say which Ontology resources, functions and apps carry a behavior.
- Ask which repositories and Foundry resources the idea touches. List them in your summary.
- The spec home is the repository that holds `openspec/`. If the user works in another repository, remind them that specs are written in the spec home.

## Confirm the Ontology

Do this before the user proposes anything that names an Ontology object type or action type.

1. Collect every API name the idea touches. Take them from the user, the glossary and existing specs.
2. Confirm each one exists. Use, in this order:
   - the Ontology tools you have access to in this session;
   - `openspec/ontology.json`, a list of API names, if the repository has one;
   - the user, who can look in Ontology Manager.
3. Report each name as confirmed or not found. Mark a name not found until the user confirms it.
4. Do not rename or redefine an object type. The spec refers to it by API name only.

## Check the glossary

- Match each domain noun in the discussion to a glossary term. Use the glossary term, not a synonym.
- List nouns that have no term. These need a row in `openspec/glossary.md` in the change.
- Flag any word the glossary lists as a forbidden synonym.
- A term is a business concept, not an Ontology type. Ask which object types and link types represent it. One term may need several, and one object type may serve several terms. Report the mapping in your summary.

## Ending

When the discussion has a direction, give a short summary:

- what the user wants and why;
- capabilities to add or change, named in kebab-case (for example `delay-reporting`);
- Ontology names confirmed and not found;
- new glossary terms;
- open questions, each as a draft row for `open-questions.md` (question, blocking yes or no, who can answer);
- the data and logic it touches: object types, link types, datasets, actions, functions and AIP Logic, by API name, marked new, changed or read;
- the business questions the model must answer, and which object and link types answer each (a manual export or join people use today often means a missing link);
- two or three sketch scenarios in Gherkin form (GIVEN, WHEN, THEN), including one failure case, so the user can confirm you understood the behavior.

Then offer: "Load the OpenSpec Propose skill to write the change." Do not start it yourself.

## Checks

After the user commits on their branch, read the Checks for the commit.
If the OpenSpec check or the glossary check fails, tell the user which file and line it names.
