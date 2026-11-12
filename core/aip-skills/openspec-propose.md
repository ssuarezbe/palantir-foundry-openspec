Name: OpenSpec Propose
Description: Load when the user wants a new change written: proposal, specs, design and tasks in one pass. Works with no CLI. Use the OpenSpec Explore skill first if the idea is still unclear.

# OpenSpec Propose

Create one change with all its artifacts. Specs live in `openspec/` in the Code Repository. Paths are relative to the repository root.

## Before you start

1. Work on a branch of the Code Repository. If you are on main, make a branch first. Never commit to main.
2. Read `openspec/config.yaml`. Follow its `context:` and `rules:`.
3. Read `openspec/glossary.md`. Use every term verbatim. Never use a forbidden synonym.
4. Read the folders in `openspec/specs/` that relate to the idea. Read them in full.
5. Confirm every Ontology object type and action type the change touches exists. Use the Ontology tools you have, `openspec/ontology.json` if present, or ask the user. Stop on any name you cannot confirm.

## Several repositories

Use this when the feature touches more than one repository or Foundry resource (for example an action type, a TypeScript function, a Python function and an app).

- The repository that holds `openspec/` is the spec home. It keeps the specs for the whole product. Other repositories keep none. Write the change here, never in the other repositories.
- Name capabilities by business behavior (`batch-release`), not by repository.
- In a spec, add one line under a requirement that more than one place implements: `Implemented in: <ontology action, function, app>`. Name each place.
- In `tasks.md`, make one group per repository, ordered by dependency: Ontology first, then functions, then apps that use the regenerated SDK. Name the repository in the group heading.
- If your Foundry enrollment has Global Branching, use one Global Branch named like the change for every resource. If not, use a branch with the change name in each repository.

## Create the change

1. Pick a kebab-case name that says what the user gets, for example `add-delay-reason`. Ask if unsure.
2. If `openspec/changes/<name>/` exists, ask: continue it or pick another name. Do not overwrite.
3. Create the folder `openspec/changes/<name>/`.
4. Create `openspec/changes/<name>/.openspec.yaml` with exactly these lines (use today's date; ask the user if you do not know it):

```
schema: foundry-spec-driven
created: YYYY-MM-DD
```

If no spec behavior changes (pure refactor, tooling, docs), add the line `skip_specs: true` and write no spec files.

## Artifact order

Write in this order. Do not start an artifact before the ones it needs exist.

1. `proposal.md` (needs nothing)
2. `specs/<capability>/spec.md`, one per capability, and `design.md` (both need the proposal)
3. `tasks.md` (needs the specs and the design)

Check which files exist before each step. Skip files that already exist unless the user asks to rewrite them.

## proposal.md

Headings, in this order: `# Proposal`, `## Why`, `## What Changes`, `## Capabilities` with `### New Capabilities` and `### Modified Capabilities`, `## Glossary changes`, `## Impact`.

- Why: one or two sentences.
- Capabilities: one line each, `` `kebab-name`: what it covers ``. Name a lasting behavior, not the task.
- Glossary changes: each new or changed term with its definition and API name, or "None".
- Keep it to two pages.

## specs/<capability>/spec.md

Headings: `# Spec Delta`, then for a new capability `## Purpose` (one or two sentences, at least 50 characters), then `## ADDED Requirements`, `## MODIFIED Requirements`, `## REMOVED Requirements` or `## RENAMED Requirements`.

Each requirement:

```
### Requirement: <name>
The system SHALL <one behavior>.
Ontology: <ApiName>

#### Scenario: <name>
- **GIVEN** <context>
- **WHEN** <one trigger>
- **THEN** <outcome an observer can see>
- **AND** <more outcome>
```

Write every scenario in Gherkin form:

- One line per step. Keywords in bold capitals, in English (validation looks for them). The step text may be in any language.
- GIVEN is context. Exactly one WHEN. THEN is what someone sees: a status, a message, a recorded value. Continue a step with AND or BUT.
- One behavior per scenario. Business language and glossary terms. No clicks, field ids or function names.
- Same steps with different data: one scenario with `<placeholder>` in the steps and, right after the steps, an `**Examples**` table (a header row naming each placeholder, one row per case).
- No Background. Put shared context in the requirement text, or repeat the GIVEN.
- Cover the main path, each stated rule and at least one failure case.

Checklist. Every item must be true before you move on:

- [ ] Requirement text is 500 characters or fewer and contains SHALL or MUST.
- [ ] Every requirement has at least one `#### Scenario:` (exactly four `#`).
- [ ] Every scenario has GIVEN, one WHEN and THEN lines in bold capitals. Outlines have an Examples table with every placeholder as a column.
- [ ] The `Ontology:` line appears only where the requirement touches an Ontology resource. The name is exact and confirmed.
- [ ] Glossary terms are verbatim. No forbidden synonyms outside code spans.
- [ ] MODIFIED copies the whole existing requirement from `openspec/specs/<capability>/spec.md`, then edits it.
- [ ] REMOVED has **Reason** and **Migration** lines. RENAMED uses `FROM:` and `TO:`.
- [ ] No `## Purpose` in a delta for an existing capability.

Specs describe behavior, not code. No class names, no library choices.

## design.md

Headings: `# Design`, `## Context`, `## Goals / Non-Goals`, `## Decisions`, `## Foundry resources`, `## Risks / Trade-offs`. Add `## Migration Plan` and `## Open Questions` when needed.

Foundry resources lists datasets, transforms, object types, action types and functions the change adds, changes or reads, by API name. Write "None" if none. Skip the file only for a small change with no technical choices. Tell the user if you skip it.

## tasks.md

- `# Tasks`, then groups `## 1. <name>`, `## 2. <name>`.
- Every task is `- [ ] 1.1 <work>`, followed by one indented line: `  - **Verify:** GIVEN <state>; WHEN <action>; THEN <result>.` If a spec scenario already says it, cite it: `  - **Verify:** scenario "<name>" of <capability>.` A Verify line is not a checkbox.
- Order by dependency. Put each group's tests and docs in that group.
- Add a task to update `openspec/glossary.md` when the proposal lists glossary changes.

## Finish

1. Re-read every file against the checklists. Fix what fails.
2. Show the user the list of files created.
3. Commit on the branch. Read the Checks. If the OpenSpec or glossary check fails, open the file it names, fix it and commit again.
4. Tell the user: "Ready to implement. Load the OpenSpec Apply skill."
