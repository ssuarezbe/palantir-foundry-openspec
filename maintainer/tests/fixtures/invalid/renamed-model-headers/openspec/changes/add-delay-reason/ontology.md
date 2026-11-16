# Ontology

## Scope

| Ontology (space) | Private or shared | Packaged in Marketplace | Core type owner |
| --- | --- | --- | --- |
| `LogisticsOntology` | private | no | Logistics team |

## Object types

| API name | Display name | Concept | Status | Primary key (type) | Backing dataset |
| --- | --- | --- | --- | --- | --- |
| `Shipment` | Shipment | `Shipment`, `Delay reason` | changed | `shipmentId` (String) | `shipments_clean` |

- `Shipment`: A load of goods moving between two sites.
  - `delayReason`: String, one of the allowed reasons (new)
  - `delayReportedAt`: Timestamp, UTC (new)

## Link types

| API name (each side) | Glossary term | From → To | Cardinality | Stored as | Status |
| --- | --- | --- | --- | --- | --- |
| `carrier` / `shipments` | `Shipment`, `Carrier` | `Shipment` → `Carrier` | one-to-many | foreign key `carrierId` on `Shipment` | read |

## Interfaces and shared properties

None

## Value types

None

## Questions this model must answer

| ID | Question | Object and link types used |
| --- | --- | --- |
| B1 | Which late Shipments are caused by Customs, and which Carriers carry them? | `Shipment`, `carrier` |

## Backing data

| Name | Kind (dataset, virtual table, model) | Status | Source (system or dataset) | Update cadence | Owner |
| --- | --- | --- | --- | --- | --- |
| `shipments_clean` | dataset | changed | `shipments_raw` | hourly | Logistics team |

- `shipments_clean`: `delayReason: String`, `delayReportedAt: Timestamp` (both new, empty for existing rows)

Transforms and pipelines: None (the action writes the properties; the existing pipeline carries them through).

Data quality:

| Dataset | Check | Threshold or rule |
| --- | --- | --- |
| `shipments_clean` | `delayReason` is one of the allowed reasons or empty | no other value |

## Access

Carrier users see only Shipments linked to their own Carrier (restricted view, unchanged). Planners see all. AI agents inherit the permissions of the user who runs them.

## Design review

No deviations
