# Multi-repository projects

One product often spans an Ontology, TypeScript functions, Python functions and an app, each in its own repository. Keep one set of specs for the whole product in a single "spec home", and point every other repository at it with an OpenSpec store.
A feature then has one proposal, one set of specs and one task list, instead of four partial plans.
Tested here: the store flow on OpenSpec 1.16.0 (register, new change from a satellite, doctor, validate, fresh machine). Not tested here: anything in Foundry. Palantir feature statements below come from notes supplied to this project and were not checked against Foundry.

## Terms

- **Store**: an OpenSpec root that several repositories share. OpenSpec marks stores beta.
- **Spec home**: the repository whose `openspec/` is registered as the store.
- **Satellite**: any other repository. Its `openspec/config.yaml` has one line, `store: <id>`. It keeps no specs.

## Steps

1. Choose the spec home. Your decision. Two options:
   - The TypeScript functions repository. It already has the Jest gate and needs no new repository.
   - A dedicated `product-specs` repository. Cleaner, if you can get one approved.
2. Set up the spec home as in `docs/setup.md`: `addons/cli/` to `tools/openspec/`, `core/project-template/openspec/` to `openspec/`, the CI tests from `docs/setup.md`.
3. Register it on your machine. From the spec home root:
   `./tools/openspec/launchers/openspec store register . --id product-specs --yes`
4. Set up each satellite: create `openspec/config.yaml` with one line. Change the id if you chose another. Do not copy `tools/` or the CI tests there. (The tests skip themselves in a repo whose config has `store:`.)
   ```
   store: product-specs
   ```
5. Register the store on every machine that touches a satellite. The registry is a per-machine file that holds the absolute path of your local clone. On a machine that has not registered it, any command in a satellite stops with `Unknown store 'product-specs'`. Clone the spec home first, then run the step 3 command with its path.
6. Create changes from anywhere. Run `new change <name>` inside a satellite and the change lands in the spec home's `openspec/changes/`. Check with `doctor` and `context`.
7. Write specs by business capability (`specs/batch-release/`), not by repository. Where several places implement a requirement, add a line:
   ```
   ### Requirement: Approve a batch release
   The system SHALL let a QA approver release a batch only when all tests pass.
   Ontology: ApproveBatchRelease
   Implemented in: ontology action ApproveBatchRelease, ts-functions validateRelease, react-app release page
   ```
8. Write `tasks.md` with one group per repository, in dependency order: Ontology first, then TypeScript and Python functions, then the app that needs the regenerated SDK. Tick a group when that repository's work merges.
9. Branches. If your enrollment has Global Branching, use one Global Branch named like the change, so all resources move and merge together. If not, use a branch with the change name in each repository.
10. Archive only after every repository's work has merged. The Archive skill asks.
11. Gates. Run the spec and glossary checks in the spec home's CI. Satellites need no OpenSpec check.

## Who works where

| Who | Reach to the specs |
| --- | --- |
| AI FDE | The AIP skills read and write `openspec/` in the spec home. With Global Branching it can edit the other resources on the same branch. |
| Workspace on the spec home | Full CLI. |
| Workspace on a satellite | Probably cannot see the spec home, because a workspace opens one repository. If you cannot clone a second repository inside it, write specs from the spec home or AI FDE, and implement from the task list. |
| Laptop | Clone every repository, register the store, open the repositories together (OpenSpec worksets, beta, or `context --code-workspace`). |

## Limits

- Stores, references and worksets are beta. Commands and file formats may change between releases. Retest this flow on every upgrade (`maintainer/UPGRADE.md` in the source repository).
- OpenSpec never pulls or pushes. A stale checkout of the spec home shows stale specs.
- The workspace prompts and skills call `./tools/openspec/launchers/openspec`. That path exists only in the spec home. In a satellite, call the launcher by its full path, or add its folder to `PATH` and adapt the prompt. This kit does not do that for you.
- Ontology object types and action types edited in Ontology Manager have no repository. Specs name them by API name.

## Later: SuperRepo

Palantir's SuperRepo (beta, may not be on your enrollment) keeps Ontology as code, TypeScript functions and an app in one repository. One ordinary `openspec/` would then cover the product. The notes say its docs do not mention Python functions. Confirm before you plan around it.

## What to confirm in Foundry

- Whether a Foundry workspace can clone a second repository, and whether a registry file written in the workspace survives between sessions.
- Whether Checks in the spec home can run the gate and whether a satellite's Checks may stay free of OpenSpec.
- What Global Branching covers in your enrollment (repositories, functions, Ontology, Ontology Actions, OSDK apps) and its limits: the notes say TypeScript v2 and Python functions need a local Ontology SDK, and OSDK apps must install the SDK with npm and use Vite 6, 7 or 8.
- Who may merge into the spec home.

## Sources (as cited in the notes, not opened here)

- https://openspec.dev/docs/stores
- https://openspec.dev/docs/worksets
- https://palantir.com/docs/foundry/global-branching/overview/
- https://palantir.com/docs/foundry/global-branching/integrations/
- https://palantir.com/docs/foundry/superrepo/core-concepts/
