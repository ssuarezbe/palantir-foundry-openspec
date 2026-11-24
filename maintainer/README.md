# Maintaining the kit

One person owns the kit (today: Optivia Labs). Work on a connected machine. The release zip is the only thing that crosses into the restricted network.

## The maintainer folder (in Git, not in the zip)

| Path | What it is for |
| --- | --- |
| `maintainer/scripts/` | `build.sh` (pinned dependency lock, `--release` zip with `drop-in/`), `make-dropin.sh`, `sync-upstream.sh`, `make-workspace.py`, `setup-test-env.sh`, `pinned/` |
| `maintainer/tests/` | `run-all.sh`, `fixtures/` (valid and invalid), `allowed-urls.txt`, `jest-env/` (ignored, about 58 MB) |
| `maintainer/upstream/` | Untouched `init` output used to build `addons/workspace/` and to diff on upgrade, and the upstream licence |
| `maintainer/UPGRADE.md` | How to move to a new OpenSpec version |

## Where to change what

| To change | Edit | Then |
| --- | --- | --- |
| A company rule (naming, scope, storage, classification) | `openspec/rulebook/` in the project, from the owning team | Refresh the `Source:` and `Copied:` lines. The kit's own template holds only invented examples |
| A rule for specs, tasks or a Foundry artifact | `core/project-template/openspec/schemas/foundry-spec-driven/` (instructions, templates), and the matching `rules:` in `config.yaml` | Update the same rule in `core/aip-skills/` by hand: the skills carry no CLI, so they do not read the schema |
| Ontology design guidance | `core/project-template/openspec/ontology-design.md` | Re-read Palantir's pages and keep the "read on" date in `docs/glossary-and-ontology.md`. Update the schema and skills only if a rule they repeat changed |
| A skill | `core/aip-skills/*.md` | Keep zero `openspec <command>` calls and 150 lines or fewer |
| Continue or Claude prompts | Never by hand. `addons/workspace/` is generated | Run `maintainer/scripts/make-workspace.py` |
| A check (Jest, TypeScript port, Python) | `addons/ci/typescript/` and `addons/ci/python/` together | Keep the messages the same in all three. Add a fixture in `maintainer/tests/fixtures/` with an `expected` file for bundle, jest and python |
| The bundle or OpenSpec version | Follow `maintainer/UPGRADE.md` | Rebuild and update `addons/cli/PIN.md` |

## Check the kit

`maintainer/tests/run-all.sh` runs every check and works offline. The Jest part needs `maintainer/scripts/setup-test-env.sh` once on a connected machine; `--no-jest` skips it.

## Release steps

1. Make the change. Run `maintainer/tests/run-all.sh`. All checks must pass.
2. Bump `VERSION`, then the version in `README.md` and `addons/cli/PIN.md` (`run-all.sh` fails if they disagree). Add a `CHANGELOG.md` entry.
3. If the artifact graph changed, raise `version:` in `schema.yaml` and say in the changelog what open changes must add. Adding an artifact changes the graph: agree it first.
4. Run `maintainer/scripts/build.sh --release`. It zips the top-level files, `docs/`, `core/` and `addons/`, and writes a `.sha256`. The zip cannot run `run-all.sh`. Check the zip against its `.sha256`, and the bundle against `SHA256SUMS`.
5. Send the zip and `.sha256` through the approved transfer. Tell teams to discard any earlier zip with the same version.

## Routine upkeep

| When | Do |
| --- | --- |
| Every quarter, and when Foundry ships a notable Ontology change | Re-read the Palantir pages listed in `docs/glossary-and-ontology.md`. Update `ontology-design.md` and the changelog |
| A new OpenSpec release | Follow `maintainer/UPGRADE.md`. Do not skip the diff of the generated skills |
| A team reports a rule the assistant ignores | Add a fixture if a check can catch it. Otherwise tighten the instruction, and say so in the changelog |
| Foundry or AI FDE changes names or menus | Fix `docs/ai-fde.md` and `docs/setup.md` ("What to confirm in Foundry") |
| A new artifact is requested (access, app, automation, rollout) | See `docs/glossary-and-ontology.md`. A new artifact changes the graph |

## Rules this kit keeps

- Nothing downloads anything at runtime. Telemetry is off in every launcher and test.
- No install scripts. No dependencies beyond Node (the bundled CLI) and the Python standard library (the Python check). The TypeScript port needs neither.
- The artifact order is fixed: proposal, then open questions, specs, design and ontology, then logic (after ontology), then tasks, then apply.
- No Palantir proprietary content, customer data or credentials.
- Specs and task checks are written in Gherkin. The assistant follows the rules; validation checks only the basics.
