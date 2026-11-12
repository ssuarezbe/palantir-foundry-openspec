Name: OpenSpec Apply
Description: Load when the user wants to implement the tasks of an existing change. Reads the change files, does the work task by task, ticks each box and stops on blockers. Works with no CLI.

# OpenSpec Apply

Implement a change that already has `proposal.md`, specs, `design.md` and `tasks.md`. Paths are relative to the Code Repository root.

## Before you start

1. Work on a branch of the Code Repository. If you are on main, make a branch first. Never commit to main.
2. Pick the change.
   - Use the name the user gave.
   - Otherwise list the folders in `openspec/changes/`, skipping `archive/`. If there is one, use it. If there are several, ask which one.
   - Say: "Using change: <name>".
3. Check the files in `openspec/changes/<name>/`.
   - `tasks.md` must exist. If it does not, stop. Tell the user to load the OpenSpec Propose skill first.
   - If `.openspec.yaml` has `skip_specs: true`, there are no spec files. That is fine.
4. Read, in full: `proposal.md`, every `specs/**/spec.md`, `design.md` if it exists, and `tasks.md`.
5. Read `openspec/config.yaml` and `openspec/glossary.md`. Use glossary terms verbatim in code names, comments and messages where the domain noun appears.
6. Count the boxes in `tasks.md`. `- [x]` is done. Anything else is open. Tell the user: "<done>/<total> tasks done."
   - All done: say so and offer the OpenSpec Archive skill. Stop.

## Work loop

For each open task, in file order:

1. Say which task you are doing, for example "Task 2.1: add the delay reason field".
2. Make the smallest change that does the task. Follow `design.md` for approach and the specs for behavior.
3. Verify the task with its `Verify:` line. Act out the GIVEN, WHEN and THEN: run the test, read the output, or check the result in Foundry. If the line cites a scenario, open that scenario in the spec and check every step of it. If you cannot run it yourself, say so and ask the user to confirm.
4. Change that task's `- [ ]` to `- [x]` in `tasks.md`. Change nothing else in the line.
5. Go to the next task.

Rules:

- Touch only what the task needs.
- Where an Ontology resource is involved, use the API name from the spec's `Ontology:` line. Confirm it exists before you code against it.
- If the work shows the spec or design is wrong, stop. Say what is wrong. Offer to fix the artifact first. Do not silently change the specs.
- If a task is unclear, a decision is missing, or an error blocks you, stop. Say which task and why. Ask the user. Do not guess.
- Pause after a group if the user asked for that.
- If the change adds a domain noun, make sure the glossary task is done in this change.

## Several repositories

If `tasks.md` has one group per repository:

- Do one group at a time, in file order. That order is the dependency order.
- Do each group's work in its own repository, on the branch named like the change. Never commit to main.
- Tick the group's boxes only when its work is done and verified. Say which groups still wait for a merge.
- If an earlier group changed the Ontology, check that the SDK or types your next group needs are available before you start it. If they are not, stop and tell the user.

## Commit and Checks

1. Commit on the branch, with a message that names the change and the task group.
2. Read the Checks for the commit.
3. If the OpenSpec check fails, open the file it names and fix it. Typical causes: a requirement with no `#### Scenario:`, a requirement without SHALL or MUST, a change with no spec delta.
4. If the glossary check fails, read the message. Replace a forbidden synonym with the glossary term, add a missing definition, or fix an `Ontology:` name that is not in the Ontology.
5. Commit again and read the Checks again. Repeat until they pass. If you cannot fix a failure, stop and tell the user the check name, the file and the message.
6. If a build or test Check fails, fix the code the same way.

## Finish

Before the summary, walk every scenario in the change's specs. For each, say how it was shown (test, output, user confirmation) or that it was not. Do not call the change complete while a scenario is unshown.

Show a short summary:

- the change name;
- tasks done this session and tasks left;
- files changed;
- Check results.

If all tasks are done, say: "All tasks complete. Ready to archive. Load the OpenSpec Archive skill after the branch is reviewed."
If tasks remain, say which one is next and why you stopped.
