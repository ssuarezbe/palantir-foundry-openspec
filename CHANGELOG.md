# Changelog

## 1.16.0-foundry.5 - 2026-11-12

Schema `foundry-spec-driven` version 2. The bundle did not change (same SHA-256). In-flight changes made with version 1 need `ontology.md`, `data.md`, `logic.md` and `open-questions.md` before `tasks.md`.

- New artifacts: `ontology.md` (object types, link types, access), `data.md` (datasets, transforms, data quality), `logic.md` (actions, functions, AIP Logic and agents), `open-questions.md` (knowledge gaps across every artifact).
- Graph: all four need the proposal, except `logic` which needs `ontology`. `tasks` now needs all of them. `apply` stops on a blocking open question.
- `design.md`: Foundry resources is a summary with pointers; its Open Questions section is gone (rows go to `open-questions.md`).
- `config.yaml` rules for each new artifact; the four AIP skills read, write and check the new files.
- Glossary and Ontology are separate: the glossary column is now `Ontology resources`, a comma-separated list of object, link and action type API names. `Ontology:` lines in specs accept several names. `ontology.md` and `logic.md` tag each row with its glossary term. Both ports validate each name in the list against `ontology.json` and skip the `Ontology:` and `Implemented in:` lines in the forbidden-synonym scan (an API name may equal a forbidden word). Fixtures `valid/concept-many`, `invalid/unmapped-concept-member`.
- Foundry docs review (`docs/glossary-and-ontology.md`): `ontology.md` gains display name, description, property units, how a link is stored (foreign key or join dataset) and "Questions this model must answer"; `logic.md` functions list their edits and the function-backed action. API names, never RIDs.
- Ontology architecture review: `ontology.md` gains Interfaces and who each access rule covers (users, groups, agents); `data.md` a kind column (dataset, virtual table, model); `logic.md` a function kind and a "Writeback to other systems" table.
- `openspec/ontology-design.md` in the project template: Palantir's Ontology design rules and anti-patterns, condensed (naming, granularity, primary keys and property types, structs, links and object-backed links, interfaces, action rules and submission criteria, function edits, security, governance, validation). The `ontology` and `logic` artifacts, `config.yaml` and all four AIP skills point to it. `ontology.md` gains Scope (space, private or shared, Marketplace, owner), a link side name for each side, object-backed links, shared properties, value types and a "Design review" table; `logic.md` actions gain rules and who may run them.
- Candidate artifacts not built (access, app, automation, rollout, integration): `docs/glossary-and-ontology.md`.

## 1.16.0-foundry.4 - 2026-11-11

Restructure. Every consumer path changed; the bundle did not (same SHA-256).

- Folders grouped by audience: `core/` (`project-template/`, `aip-skills/`), `addons/` (`cli/`, `workspace/`, `ci/`), `maintainer/` (`scripts/`, `tests/`, `upstream/`).
- `schema/` deleted: the schema has one copy in `core/project-template/openspec/schemas/`.
- `satellite-template/` deleted: the one-line config is in `docs/multi-repo.md`.
- `docs/` cut from seven guides to four (`setup.md`, `ai-fde.md`, `glossary-and-ontology.md`, `multi-repo.md`). The upgrade guide moved to `maintainer/UPGRADE.md`.
- `addons/workspace/` trimmed to four workflows (explore, propose, apply, archive) plus the `openspec-sync-specs` skill, which the archive skill runs inline. The `sync` and `update` entry points and the `update-change` skill are gone.
- `PIN.md` and the bundled-package licences moved next to the bundle in `addons/cli/`.
- `build.sh --release` builds a lean zip (top-level files, `docs/`, `core/`, `addons/`).

## 1.16.0-foundry.3 - 2026-11-11

- Gherkin: spec scenarios use GIVEN / WHEN / THEN / AND / BUT with optional `<placeholder>` and Examples tables. Each task has a `Verify:` line in Gherkin form or citing a scenario. Rules live in the schema instructions and templates, `config.yaml` and the AIP skills. No new gate.
- Python port: scenario needs a WHEN/GIVEN and a THEN step, as in the bundle.
- Fixtures: `valid/gherkin`, `invalid/scenario-no-then`.
- Build: the dependency tree is now pinned (`scripts/pinned/`, `npm ci`). Before this, a rebuild a day later gave a different bundle. New bundle SHA-256 in `upstream/PIN.md`. Run-all checks that PIN.md, `cli/SHA256SUMS` and the lock agree.

## 1.16.0-foundry.2 - 2026-11-10

- Multi-repository support: `docs/07-multi-repo.md`, `satellite-template/`. One spec home, other repositories declare `store: <id>`.
- Schema: optional `Implemented in:` line in specs; tasks grouped by repository in dependency order.
- AIP skills: multi-repository rules in Explore, Propose, Apply; Archive asks whether every repository's work has merged.
- CI tests skip themselves in a satellite repository.
- `tests/run-all.sh` section 8: store register, new change from a satellite, doctor, unregistered-store error. Now 83 checks.

## 1.16.0-foundry.1 - 2026-11-10

First release. Pins OpenSpec 1.16.0.

- Bundled CLI, launchers that disable telemetry, and checksums.
- `foundry-spec-driven` schema: adds Glossary changes, Ontology references and Foundry resources. Artifact order unchanged.
- Four AIP skills with no CLI calls: explore, propose, apply, archive.
- Workspace configs for Continue and Claude Code, pointed at the launcher.
- Project template with glossary and config.
- CI gate: Jest tests, and a standard-library Python port that agrees with the bundle on every fixture.
- `tests/run-all.sh`.
