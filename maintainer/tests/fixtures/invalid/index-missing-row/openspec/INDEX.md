# Index

Start here. This file is the map of the specs, the Foundry resources and the open changes. It holds pointers, not schemas. For properties and live state, use the Ontology tools or Ontology Manager. For behavior, read the spec. For the reason a resource exists, read the change.

Read in this order:

1. This file: find the capability or resource.
2. `openspec/glossary.md`: the business term and the resources that represent it.
3. `openspec/specs/<capability>/spec.md`: the behavior.
4. The change in `openspec/changes/<name>/` (open) or `openspec/changes/archive/<date>-<name>/` (done): the model, the logic and the open questions.
5. The Ontology tools: confirm every API name before you use it.

Keep it true:

- Propose adds a row under In flight when it creates a change.
- Archive removes that row, then adds or updates the rows under Capabilities and Resources for what the change touched.
- Never delete a Resource row. When a resource is removed from Foundry, write `removed <date>` under Last changed.
- API names only, never RIDs. No properties, columns or parameters here.
- Size: one file works to roughly 300 rows. After that it splits per capability, with the root as a map. When Resources passes 300 rows, move the rows into `openspec/index/<capability>.md`, keep one row per capability here that links to its file, and keep every resource findable from this file.
- Rows whose first cell starts with `Example:` are samples. Checks skip them. Delete them when you add real rows.

## Capabilities

| Capability | Purpose | Resources | Open changes |
| --- | --- | --- | --- |
| Example: `batch-release` | Release a batch only when all tests pass. | `ApproveBatchRelease`, `Batch` | none |

## Resources

Kinds: object, link, action, function, automation, AIP Logic, dataset.

| API name | Kind | Glossary term | Cited by | Last changed | Implemented in |
| --- | --- | --- | --- | --- | --- |
| Example: `ApproveBatchRelease` | action | Batch release | `batch-release` | `2026-01-15-add-batch-release` | Ontology Manager |

## In flight

| Change | Capabilities | Resources touched | Blocking open questions |
| --- | --- | --- | --- |
| Example: `add-batch-release` | `batch-release` | `ApproveBatchRelease`, `Batch` | 0 |
