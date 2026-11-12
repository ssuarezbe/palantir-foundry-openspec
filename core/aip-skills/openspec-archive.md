Name: OpenSpec Archive
Description: Load when a change is implemented and reviewed and the user wants to finish it. Merges the change's spec deltas into openspec/specs/ and moves the change to openspec/changes/archive/. Works with no CLI.

# OpenSpec Archive

Finish a change. Merge its delta specs into the main specs, then move the change folder into the archive. Paths are relative to the Code Repository root.

## Before you start

1. Work on a branch of the Code Repository. Never commit to main.
2. Pick the change.
   - Use the name the user gave.
   - Otherwise list the folders in `openspec/changes/`, skipping `archive/`. Ask which one. Do not guess.
   - Say: "Using change: <name>".
3. Check the files. In `openspec/changes/<name>/` look for `proposal.md`, `specs/`, `design.md`, `ontology.md`, `data.md`, `logic.md`, `open-questions.md`, `tasks.md`.
   - If `.openspec.yaml` has no `skip_specs: true` and `specs/` has no `spec.md`, warn the user.
4. Count the boxes in `tasks.md`. `- [x]` is done. Anything else is open.
   - If any are open, list them. Ask: "Archive anyway?" Continue only on a clear yes.
5. Read `open-questions.md`. List every row that is still `open` or `assumed`. Ask: "Archive with these open?" Continue only on a clear yes, and say they stay in the archived folder. Stop if a blocking row is open.
6. Read `ontology.md`, `data.md` and `logic.md`. Ask: "Do these still match what was built?" Check the "Design review" table: every deviation still true, no new anti-pattern. If not, fix them first.
7. Read the scenarios in the delta specs. Ask: "Do these still describe what was built?" If the work changed the behavior, stop. Fix the delta first (back to the OpenSpec Propose skill), then archive.
8. Read `openspec/glossary.md`. If the proposal's Glossary changes list terms, confirm each is in the glossary. If not, stop and ask the user to add them in this change.

## Confirm the work has merged

Ask: "Has the work for every repository in this change merged to main (or the Global Branch merged)?"
Archive only after a clear yes. If the change has one task group per repository, name each repository when you ask. If the answer is no or unsure, stop.

## Confirm

Show the user a plan before you write anything:

- the change name;
- for each capability: the requirements to add, change, remove or rename, and whether the main spec is new;
- the archive path: `openspec/changes/archive/YYYY-MM-DD-<name>/`.

Ask: "Merge and archive?" Wait for a clear yes. On anything else, stop.

## Merge each delta

For each file `openspec/changes/<name>/specs/<capability>/spec.md`, the main spec is `openspec/specs/<capability>/spec.md`.

If the main spec does not exist:

1. The delta must have only ADDED requirements. If it has MODIFIED or RENAMED, stop. Say the capability does not exist yet.
2. Create `openspec/specs/<capability>/spec.md`:
   - title `# <capability> Specification`;
   - `## Purpose` copied from the delta;
   - `## Requirements`, then the ADDED requirement blocks.

If the main spec exists, edit it under `## Requirements`. Leave its Purpose and every other requirement exactly as they are.

- **ADDED**: append each block (the `### Requirement:` line, its text and all its scenarios). If a requirement with that name is already there, stop and report it.
- **MODIFIED**: find the requirement with the same name (ignore extra spaces). Replace the whole block with the delta's block. If none matches, stop and report it.
- **REMOVED**: find the requirement by name. Delete the whole block. If it was the last requirement, tell the user and ask whether to delete the spec folder.
- **RENAMED**: each `FROM:` / `TO:` pair. Change the heading text only. Keep the body.
- Apply RENAMED first, then REMOVED, then MODIFIED, then ADDED.

After merging, check each main spec you wrote:

- [ ] No `## ADDED Requirements`, `## MODIFIED Requirements`, `## REMOVED Requirements` or `## RENAMED Requirements` heading remains.
- [ ] Every requirement has SHALL or MUST and at least one `#### Scenario:`. Every scenario still has GIVEN, WHEN and THEN lines, and each Examples table is intact.
- [ ] No requirement name appears twice.
- [ ] `Ontology:` lines and glossary terms are unchanged from the delta.

If a check fails, fix the main spec. If you cannot, stop. Do not move the change.

## Move the change

1. Create `openspec/changes/archive/` if it does not exist.
2. Target name: `YYYY-MM-DD-<name>` with today's date. Ask the user for the date if you do not know it. If the name already starts with a date, do not add another.
3. If `openspec/changes/archive/<target>/` exists, stop. Ask the user to pick another date or rename the old one.
4. Move the whole folder `openspec/changes/<name>/` to `openspec/changes/archive/<target>/`. Do not leave a copy.

## Commit and Checks

1. Commit on the branch with a message like "Archive <name>".
2. Read the Checks for the commit.
3. If the OpenSpec check fails, open the file it names and fix it. If the glossary check fails, fix the term or the `Ontology:` name it names.
4. Commit again and read the Checks again until they pass. If you cannot fix a failure, tell the user the check, the file and the message.

## Finish

Report:

- the change name;
- the archive path;
- main specs created or updated;
- warnings you accepted (open tasks, missing files);
- Check results.
