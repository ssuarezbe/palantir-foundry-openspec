# Ontology design rules

Read this before you write `ontology.md` or `logic.md`, and again when you review them. It condenses Palantir's public Ontology design pages (read 2026-11-12). Check it against your enrollment: Foundry changes. A rule you break needs a row in the "Design review" table of `ontology.md`, with the reason and the point at which you will revisit it.

## 1. Name for people

- Name for business users, not source systems. `lastInspectionDate`, not `dtLastInspMod`.
- Object types are singular, concrete nouns a domain expert recognizes. Properties are concise and free of type or system detail.
- Qualify ambiguous words (`monetaryValue`, not `value`). Use one date-naming convention across the Ontology.
- Name a link after the relationship, so it reads naturally from each side (an employee's `department`, a department's `employees`). Never `relatedTo`.
- Every object type, property and link has a display name and a one-sentence description. Agree the naming conventions before building.
- Use API names in specs, never RIDs. RIDs differ between environments.

## 2. Object types

- Model real-world entities and events, not source tables, APIs or spreadsheet tabs. Design the model before you map data.
- One entity per object type. Split a row that describes several entities (an order row holds an order, a customer and a product).
- Keep identity apart from observation: measurements and events about an entity are usually their own object types.
- One canonical type per entity. Merge copies by source system or department into one type, and control who sees what with security. Rule of three: one duplicate may pass, two is a warning, three means refactor.
- Expose only properties with business meaning. Keep ETL and technical columns in the backing dataset. Avoid wide types where most properties are null: move capability-specific properties to an interface or a linked extension type.
- Store each fact once, on the object where it belongs. Use a derived property for a value that depends on linked objects or on actions (a count of reports). Do not maintain counts by hand. Denormalize only as a recorded decision: the reason, the source of truth, how copies stay in step, and the scale at which you revisit it (derived properties are fine under about 10,000 objects per query).
- Keep history on one current object plus linked history or amendment types, time series properties or edit history. Never one object per version or per year.
- A type with no backing dataset is allowed when every object is created by an action.
- Status of a type or property is `experimental` (default), `active` or `deprecated`. Visibility is `prominent`, `normal` (default) or `hidden`. Hide technical types from default views.

## 3. Properties

- Primary key: prefer String, Integer or Short. Date, Timestamp, Boolean, Byte and Long are discouraged (collisions, two values, precision above 1e15). Float, Double, Decimal, Vector, Array, Struct, Marking and the media and series types cannot be a primary key.
- Byte, Float and Short properties cannot be used in action types. A Vector property has at most 2048 dimensions. An Array cannot hold nulls.
- Struct: groups related fields that describe one value (an address) or one result with its metadata (an AI output with confidence and sources). No nested structs. A field is never an array, though a struct property can hold an array of structs. At least one field, and name a main field. Only from datasets and restricted views. Each field is queried independently, so two entries can match a query neither satisfies alone.
- Shared property: one property used on several object types, so its metadata is managed once. The data is not shared.
- Value type: a semantic wrapper over a field type with constraints (for example a regular expression for an email), reused across properties and pipelines, versioned, and usable only in the space that defines it. Not available in the Default ontology.
- Type classes and render hints are metadata that applications read (Object Explorer, Quiver, Vertex, Map, actions). Record one only when an application needs it. They do not change storage, except `analyzer`.
- Semantic search: a Vector property holds an embedding of text tied to an object. Record the source text property and the embedding model.

## 4. Links

- A link answers a domain question ("this patient visited this facility"). Never create one only because two datasets share a foreign key. Link entities instead of embedding them as columns.
- One-to-one and one-to-many: a foreign key property on one type points at the primary key of the other. Many-to-many: a join dataset of key pairs, with columns mapped to each side.
- Each side has its own display name, API name and cardinality. Either side can be traversed, so do not add a reverse link type. Several link types may join the same two types if each side's API name is unique. A type may link to itself.
- Use a direct link when the relationship carries no data of its own. Use an object-backed link type when it has its own data (dates, role, status, allocation).
- No links across ontologies. Use a shared ontology for that.

## 5. Interfaces

- Define an interface when several types share properties, links or actions. Base it on a capability (`Inspectable`, `Schedulable`) or on a taxonomy (a category used for aggregation). Compose and extend interfaces. Do not build deep inheritance chains or combination types such as `SchedulableBuilding`.
- Build actions, functions and apps against interfaces where the platform supports it.

## 6. Actions and functions

- An action is one transaction made for a human or agent decision. Design it around a business operation (`Transfer Employee`), with optional parameters. Not one action per property (action sprawl).
- Choose the tool for the job: actions for decisions, pipelines for batch and streaming data work, automations for reacting to events, functions for live complex logic. Not one hammer for all (golden hammer).
- Rules: create, modify, delete object; create, delete link (many-to-many only); the same for interfaces; function rule; side effects (notification, webhook, schedule). Several rules compile into one edit per object, so their order matters. Modify and delete cannot reference an object created in the same action. A function rule cannot be combined with other rules. To change a one-to-many or one-to-one link, modify the foreign key property.
- Use a function-backed action when rules are not enough: several linked objects change together, a value is computed from several objects, or several types and links are created.
- Submission criteria decide whether an action may run: the user (id, groups, attributes), parameters, or the execution context. Each root condition has its own failure message. Do not use NOT on group, marking or organization membership: a scoped token may lack the attribute and the condition then passes.
- Notifications show the Ontology state from before the edits. A webhook runs before or after the edits.
- A function that edits changes nothing by itself. It takes effect only through a function-backed action. Automate does not apply edits returned by a function.
- Consolidate repeated logic in one shared function or interface.

## 7. Security

- Say what is protected and for whom, in domain terms. Least privilege. Start restrictive and open on purpose.
- Combine row-level (which objects) and column-level (which properties) control. Draw boundaries along domain boundaries and enforce them with Ontology security, not code filters.
- Never duplicate an object type to implement security. One type, well-designed policies.
- A new link, type or property must not widen access to restricted data. Ask whether the workflow needs the data at all.
- Agents inherit permissions from the user or project.

## 8. Governance

- One ontology per space (1:1 with the space). Most organizations need one private ontology. A second team is not a reason for a second ontology: grant roles on projects.
- Each core type has one owner. Do not let several teams edit it. Lock the essential structure of production types, design for extension, and extend instead of modifying.
- Involve stakeholders from several teams. Treat Ontology changes like production releases.
- Marketplace packaging carries object types, link types, shared properties, interfaces and datasets. It does not carry objects or action edits, nor Cipher, Geo time or Vector properties.
- Prefer incremental improvement to a rewrite. Never compromise on naming, semantics or security. Implementation detail can be simplified: name the tradeoff and when you will revisit it.

## 9. Anti-patterns to reject

| Anti-pattern | What it is | Instead |
| --- | --- | --- |
| System silos | One type per source system for the same entity | One type, a pipeline that merges the sources with precedence rules |
| Department silos | A "Customer" type per department | One shared type, department properties and links, restricted views |
| Kitchen sink | Every source column imported as a property | Only properties with business meaning |
| God object | One type for several entities (an `Asset` holding cars, licences and buildings) | One type per entity, an interface for shared traits |
| Golden hammer | One tool for every job | Match the tool to the job (section 6) |
| Action sprawl | Many one-property actions | Actions that follow business operations |
| Time machine | An object per version, or a type per year | One current object, linked history, time series or edit history |
| Misnomer | `Item`, `value`, `type`, `relatedTo` | Specific, qualified names with descriptions |

## 10. Validate the model

Test it against real business questions, not only structure. Write each question as situation, contributing factors, impact. Try it with experts and newer users using general tools, then with AIP Analyst or AI FDE. Repeated confusion about one type or link is a design problem. Keep the questions as a standing test set. In a change, they go in the "Questions this model must answer" table of `ontology.md`, each covered by a spec scenario.
