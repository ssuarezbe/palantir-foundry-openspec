# How it works

The four steps, the files a change holds, and where the rules are enforced. For setup, start at `docs/setup.md`.

## The four steps

Every change follows four steps. Each step is a skill (AI FDE) or a command (Claude Code, Continue):

| Step | Skill or command | What happens |
| --- | --- | --- |
| Explore | `OpenSpec Explore`, `/opsx:explore` | Read-only thinking. Starts at `INDEX.md`, names the company rules that will bind the idea, confirms Ontology API names, matches words to the glossary, sketches scenarios and open questions. Can audit the index. |
| Propose | `OpenSpec Propose`, `/opsx:propose` | Writes the change files (see "What a change contains" below) on a branch. Checks then validate them. |
| Apply | `OpenSpec Apply`, `/opsx:apply` | Builds the tasks one at a time, acts out each `Verify:` line and ticks the box. Stops on a blocking open question. |
| Archive | `OpenSpec Archive`, `/opsx:archive` | After the work merges, folds the spec changes into `openspec/specs/`, moves the change folder to `openspec/changes/archive/` and updates `openspec/INDEX.md`. The Foundry files stay in that folder with the change. |

In Continue the commands are written `/opsx-propose` and so on.

## Three ideas

Three ideas run through the kit:

- **The glossary is the business vocabulary; the Ontology is the data model.** Specs are written in glossary terms and name Ontology resources by API name.
- **Rules live in files an assistant reads**, because gates are hard to run in a regulated Foundry network. The only automatic check is OpenSpec's own validation.
- **Gaps are recorded, not guessed.** Unknowns go in a log that blocks the tasks until answered.


## What a change contains

The `foundry-spec-driven` schema gives every change these files. They live in `openspec/changes/<name>/`. Write `proposal.md` first. After it, `open-questions.md`, the specs, `design.md` and `ontology.md` can be written in any order. `logic.md` needs `ontology.md`. `tasks.md` needs all the others.

| File | Holds |
| --- | --- |
| `proposal.md` | Why, the capabilities, glossary changes (each term with its Ontology resources), and the Foundry resources touched, named once under Impact |
| `open-questions.md` | Every knowledge gap: ID, stage, question, blocking, affects, owner, status, answer. Started with the proposal; every later file adds rows |
| `specs/<capability>/spec.md` | Behavior in Gherkin and glossary terms, with `Ontology: <ApiName>, <ApiName>` lines |
| `design.md` | Technical approach: context, decisions, risks, migration, and the Rulebook review (each applicable company rule: complies, deviates or open) |
| `ontology.md` | The data model: scope (space, owner), object types, link types (each tagged with its glossary term, with units and how links are stored), interfaces and shared properties, value types, the questions the model must answer, backing data (datasets, transforms, data quality), access, and a design review. "None" with a reason when the change touches no Ontology resource |
| `logic.md` | Actions (rules, who may run them, side effects), functions (their edits and the function-backed action), automations (trigger, condition, effect), writeback to other systems, AIP Logic and agents with evaluation cases |
| `tasks.md` | Checklist in dependency order, each task with a `Verify:` line |

Files that sit outside a change, in `openspec/`:

| File | Holds | Who edits it |
| --- | --- | --- |
| `config.yaml` | The schema name, project context and per-artifact rules every assistant follows | The team, rarely |
| `INDEX.md` | The map for agents: capabilities, Foundry resources (objects, links, actions, functions, automations) and open changes, as pointers. Roughly 300 rows, then it splits per capability. Works with AI FDE only (`docs/index-options.md`) | Propose and Archive, in the change |
| `rulebook/` | The company's rules as short, citable rows, one file per owning team: naming, scope, storage, data classification, decision guides, process (`docs/rulebook.md`) | The owning teams' digest, refreshed by the team |
| `glossary.md` | Business terms, their Ontology resources and forbidden synonyms | The team, in the change that adds a term |
| `ontology-design.md` | Palantir's Ontology design rules and anti-patterns, condensed | The kit maintainer |
| `ontology.json` | Optional list of API names. Checks match every `Ontology:` name against it | The team, from an Ontology export |
| `schemas/foundry-spec-driven/` | The artifact graph, instructions and templates | The kit maintainer |
| `specs/`, `changes/` | Current specs, and open and archived changes | The team |

### Glossary, Ontology and design rules

A glossary term is a business concept, not an Ontology type. One term can be represented by several object types and link types, and one object type can serve several terms. The glossary row (`Ontology resources` column) lists all of them. `Ontology:` lines in a spec list the ones a requirement touches. Checks verify the names against `openspec/ontology.json`; whether the mapping is right is a review job. Details: `docs/glossary-and-ontology.md`.

The model in `ontology.md` and `logic.md` is checked against `openspec/ontology-design.md`, which condenses Palantir's design guidance: naming, one entity per object type, real relationships, interfaces, action design, security and eight anti-patterns. The "Design review" table in `ontology.md` records every rule a change breaks, why, and when to revisit it. No tool checks this. The assistant follows it and a reviewer reads it.

### Company rulebook

`openspec/rulebook/` holds the rules other teams own (data governance, cloud security, infrastructure), as rows with an ID, where they apply, the rule, a level and a pointer to the source document. It has four kinds of content: rules, decision guides (for example when to use a dataset), a classification map (what each data class such as PII or confidential allows) and maps (access by name, where things are stored). Every object type and dataset in a change carries a `classification:` line, Access is derived from the maps, and `design.md` records each applicable rule under `## Rulebook review`. A rule that needs an approval becomes a blocking open question, which the gate enforces. Where Jest or Python runs, the checks fail a change that cites an unknown rule or skips the review once the rulebook has real rows. The template ships invented `Example:` rows; replace them. How to fill it, and how to adapt it to your company or project: `docs/rulebook.md`.

### Open questions are a gate

No tasks are written, and `apply` does not start, while a row in `open-questions.md` is blocking and open. A row is never deleted. Its status changes to `answered`, `assumed` (the assumption is written down) or `dropped`. Archive asks before closing a change that still has open or assumed rows.

Other Foundry artifacts we considered but did not build (access, app, integration, rollout) are listed in `docs/glossary-and-ontology.md`.

## Where the rules are enforced

Nothing here needs a runner. The rules live in files that an assistant reads and follows.

| Layer | What it does | Who follows it |
| --- | --- | --- |
| `schemas/foundry-spec-driven/` | Templates and artifact instructions spell out the Foundry, Gherkin and design rules | Claude (CLI or MCP), Continue, anything that reads `openspec instructions` |
| `config.yaml` | `rules:` repeat them per artifact | Same |
| `core/aip-skills/` | Explore sketches, Propose writes, Apply acts out each `Verify:` line, Archive checks the scenarios still describe what was built | AI FDE, with no shell |
| OpenSpec validation (`--strict`, or its TypeScript or Python port) | Checks that each requirement has a scenario with a `WHEN`/`GIVEN` and a `THEN`. The glossary check adds forbidden synonyms, Ontology names, the open-questions gate (a change with `tasks.md` fails while a row is blocking and open) index drift (a main spec cites an `Ontology:` name with no row in `INDEX.md`) and the Rulebook review (a change cites an unknown rule or skips it). | CI, if you run it |

The limit is plain: validation does not check keyword order, a single `WHEN`, business wording, the `Examples` table, the design review or the quality of an answer. The assistant follows those rules and a reviewer checks them. No Cucumber or Behave runner is shipped. If a team later automates, each spec scenario maps one to one to a `.feature` scenario.
