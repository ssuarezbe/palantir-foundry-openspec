# Ontology

<!-- The data model this change adds, changes or reads. Read openspec/ontology-design.md first. A glossary term (business concept) can map to several object types and link types, and one object type can serve several terms: give the term on every row. Use "not modelled" if there is none. Use API names exactly as in Ontology Manager, never RIDs. Do not redefine existing types: list them as "read". Write "None" under a heading with nothing to record. -->

## Scope

| Ontology (space) | Private or shared | Packaged in Marketplace | Core type owner |
| --- | --- | --- | --- |
| `<ontology name>` | private / shared | yes / no | `<team>` |

## Object types

| API name | Display name | Glossary term | Status | Primary key (type) | Backing dataset | Properties (API name: type, unit; mark derived or denormalized) | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<ObjectTypeApiName>` | <name users see> | `<term>` | new / changed / read | `<property>` (String) | `<dataset name>` | `<apiName>: <type>, <unit>` | <one sentence> |

## Link types

| API name (each side) | Glossary term | From | To | Cardinality | Stored as | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `<SideAApiName>` / `<SideBApiName>` | `<term>` | `<ObjectType>` | `<ObjectType>` | one-to-many / many-to-many / one-to-one | foreign key `<property>` on `<ObjectType>`, join dataset `<name>`, or object-backed type `<ObjectType>` | new / changed / read |

## Interfaces and shared properties

<!-- Interfaces: shapes that several object types implement. Shared properties: one property whose metadata is managed once. Write "None" if unused. -->

| API name | Kind (interface, shared property) | Requires or type | Used by |
| --- | --- | --- | --- |
| `<ApiName>` | interface | `<apiName>: <type>` | `<ObjectType>`, `<ObjectType>` |

## Value types

<!-- Reusable semantic types with constraints. Write "None" if unused. -->

| Name | Base type | Constraint in words | Used by |
| --- | --- | --- | --- |
| `<name>` | String | `<rule>` | `<ObjectType>.<apiName>` |

## Questions this model must answer

<!-- Business questions the model must let people and agents answer without a purpose-built app. Three steps each: the situation, the contributing factors, the impact. Each question is cited by at least one spec scenario. -->

| ID | Question | Object and link types used |
| --- | --- | --- |
| `<id>` | <question> | `<ObjectType>`, `<LinkApiName>` |

## Access

<!-- Markings, restricted views, row-level and column-level rules, roles. Say who is covered: users, groups and AI agents (agents inherit permissions from the user or project). Never duplicate an object type for security. Write "None" or "Unchanged". -->

## Design review

<!-- Check this model against openspec/ontology-design.md, including the anti-patterns. List every rule you break, why, and when you will revisit it. Write "No deviations" if none. -->

| Rule or anti-pattern | Deviation | Reason | Revisit when |
| --- | --- | --- | --- |
| <rule> | <what you did instead> | <why> | <trigger, such as a volume threshold> |
