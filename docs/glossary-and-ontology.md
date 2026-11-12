# Glossary and Ontology

The Ontology is the data model. The glossary is the business vocabulary. They are different: a glossary term (a business concept) can be represented by several object types and link types, and one object type can serve several terms. Specs are written in glossary terms and name the Ontology resources by API name. They do not redefine them.
Three things enforce this: rules in `openspec/config.yaml`, the table in `openspec/glossary.md` and the checks in `docs/setup.md`.
Tested here: all rules, on fixtures. Not tested here: a real Ontology export.

## Steps

1. Open `openspec/glossary.md`. It is a table: `Term | Definition | Ontology resources | Forbidden synonyms`.
2. Add one row per domain noun.
   - Term: the word as specs use it.
   - Definition: one sentence. Empty definitions fail the check.
   - Ontology resources: the API names of every object type, link type and action type that represents the term, separated by commas, or `not modelled`.
   - Forbidden synonyms: comma-separated words that must not appear in specs.
3. Delete the two `Example:` rows. Checks skip them, but they are noise.
4. In a spec, use the term verbatim. When a requirement reads or changes Ontology resources, add one line under the requirement text: `Ontology: <ApiName>, <ApiName>`. Use the exact API names. Leave the line out when no Ontology resource is involved.
5. A change that adds a noun adds its row in the same change. The proposal's `## Glossary changes` section lists it. The tasks include "update glossary".
6. Optional: add `openspec/ontology.json` (a JSON list of API names). Then every `Ontology:` name and every name in the glossary Ontology resources column must be in it. The list is flat: it does not say whether a name is an object, link or action type.
7. Run the checks. A forbidden synonym in a spec fails with the file and line.

## Ontology design rules

`openspec/ontology-design.md` (in the project template) holds the design rules: naming, object type granularity, property and primary key types, structs, links, interfaces, actions and functions, security, governance, the eight anti-patterns and how to validate a model. The `ontology` and `logic` artifacts tell the assistant to read it. `config.yaml` repeats the pointer, so Claude and Continue get it through `openspec instructions`, and the AIP skills (Explore, Propose, Apply, Archive) read it from the repository. Each change fills a "Design review" table in `ontology.md` with every rule it breaks, the reason and when to revisit it.

Source: the Foundry pages on Ontology overview, best practices, structural guidance, anti-patterns, design validation, object, property, struct, shared property, link and value types, type classes, groups, Marketplace packaging, actions (overview, rules, submission criteria, function-backed), functions, semantic search and architecture, read 2026-11-12. Many of those pages are overviews and link to detail pages that were read only where the rules needed them (object, property and link type metadata, action rules, submission criteria). Not read: API name format rules, limits, batched execution, side effects detail, object-backed link types, permissions pages. Semantic search does not say whether names or descriptions feed the embeddings.

Maintain the file by hand when Palantir's pages change. Nothing checks it against the platform.

## Concept and resource: one term, several resources

Example: the term `Shipment` is one business concept. The Ontology models it as the object types `Consignment` and `ShipmentLeg` and the link type `ShipmentToCarrier`. The glossary row lists all three. A spec says "the Shipment shows the delay reason" and adds `Ontology: Consignment, ShipmentLeg`.

- The glossary row is the one place that says which resources make up a term. `ontology.md` and `logic.md` repeat the term on each row, so the trace works both ways.
- A forbidden synonym may equal an API name (`Consignment` above). The synonym check skips the `Ontology:` and `Implemented in:` lines for that reason. Back-ticked text is skipped too.
- Not checked automatically: that a term's resources match the glossary row, or that each resource has a term. Review checks those. Only the names against `openspec/ontology.json` are checked.

## What the Foundry docs say, and how the kit uses it

Read from Palantir's public pages on 2026-11-12. Check them against your enrollment, because Foundry changes.

| Finding | Used in the kit |
| --- | --- |
| Ontology design validation: a model is checked against real business questions (situation, contributing factors, impact), tried by experts and newer users with general tools, then by AIP Analyst or AI FDE. Duplicate concepts, unclear names, units or dates, and missing or misdirected links are the usual failures. Links should reflect real relationships, not source-system joins. | `ontology.md` has display name, description, units and a "Questions this model must answer" table. Each question needs a spec scenario. |
| Ontology SQL: tables are object types and many-to-many links, addressed by RID. Columns use property API names. Many-to-many links need join tables. One-to-one and one-to-many links are joined directly. Read-only, 10,000 rows, 20 second timeout, Object Storage v2 only. | Specs and tables use API names, never RIDs. The link "Stored as" column names the foreign key or join dataset, and `data.md` lists the join dataset. Plan large reads outside Ontology SQL. |
| Function edits: functions create, modify and delete objects and add or remove links. They take effect only through a function-backed action. Automate does not apply edits from function effects. Object set queries inside the function read pre-edit values. | `logic.md` lists the edits per object type and the function-backed action. Rules: write through actions. |
| Ontology API basics: object types, properties, link types and action types form the object graph. Changes are eventually consistent: a new Ontology can return `OntologyNotFound` for a few minutes. | Confirm names with a retry before you call one missing. |
| Ontology architecture: the Language (objects, links, properties, actions, automations, logic), the Engine (reads by SQL, subscriptions and materializations; writes as transactions, batch mutations, streams and change data capture to operational systems) and the Toolchain (OSDK, DevOps). Data sources include datasets, virtual tables and models. Logic is a rule, a model, an LLM-driven function or an orchestration. Security covers rows, columns and agents, which inherit from users or projects. Interfaces describe a shape shared by object types. | `ontology.md` has Interfaces and who each access rule covers. `data.md` has a kind column. `logic.md` has function kind and a "Writeback to other systems" table. Apps that use the regenerated SDK come last in the task order. |

Not verified: palantir.com/platforms/ontology is rendered by script and returned only its title, so this section uses the docs pages for the Ontology overview and system architecture instead. The "dynamic" layer and object storage details are not described there. The Towards AI article returned an error (403), so nothing in the kit relies on it. The Ontology basics page did not define `apiName` versus RID in detail. Palantir's pages do not describe validation rules for actions or functions.

## Foundry files in a change

| File | Records | Rule |
| --- | --- | --- |
| `ontology.md` | Object types (term, key, backing dataset, properties with units), link types (term, stored as), questions the model must answer, access | API names exact. Glossary term on every row. Status `new`, `changed` or `read`. Never redefine an existing type. |
| `data.md` | Datasets, transforms, data quality checks | Every dataset behind an object type is here. No credentials or customer data. |
| `logic.md` | Actions, functions, AIP Logic and agents | AIP Logic that writes goes through an action. Evaluation cases cite spec scenarios. |
| `open-questions.md` | Every knowledge gap | A blocking, open row stops `tasks` and `apply`. Rows are never deleted. |

Every `Ontology:` name in a spec is an existing resource or is listed in `ontology.md` or `logic.md`. Each file says "None" under a heading with nothing to record, so a missing file always means "not done".

## Other artifacts we considered

Not built. Add one only when a team needs it, and ask first: a new artifact changes the schema graph. Names of Foundry features are from general knowledge; check them against your enrollment.

| Candidate | Would record | Priority |
| --- | --- | --- |
| `access.md` | Markings, restricted views, object and property security, project roles, who may run each action | High in regulated work. Today a short Access section in `ontology.md`. |
| `app.md` | Workshop modules or OSDK apps: pages, variables, the actions and object types each uses, who uses it | Next, once apps are in scope. Today a task group per app. |
| `automation.md` | Automate rules, schedules, notifications, webhooks and calls to external systems | Next. Today side effects are a column in `logic.md`. |
| `rollout.md` | Branch or proposal flow, ordering of deploys, migration of existing objects, rollback | Medium. Today `design.md` "Migration Plan". |
| `integration.md` | Sources, egress, external APIs, virtual tables | Low. Overlaps `data.md`. |
| evaluation cases | AIP Evals test sets for AIP Logic and agents | Not a file: they are a column in `logic.md` that cites scenarios. |

## Where each rule lives

- `core/project-template/openspec/schemas/foundry-spec-driven/`: the templates. Specs get an optional `Ontology:` line, proposals get Glossary changes, designs get Foundry resources, and the schema adds `ontology.md`, `data.md`, `logic.md` and `open-questions.md`.
- `core/project-template/openspec/config.yaml`: `context:` and `rules:` that every assistant reads.
- AIP skills and workspace prompts: Explore confirms API names before you propose.
- `addons/ci/`: the failing checks.

The schema lives only in the project template. There is no second copy to keep in step.

## What to confirm in Foundry

- How you export object type API names to `openspec/ontology.json`. The kit does not do this for you.
- Whether the Ontology tools in AI FDE and the Palantir MCP return API names in the same spelling as Ontology Manager.
- Who owns the glossary and who approves new terms.
