# Changelog

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
