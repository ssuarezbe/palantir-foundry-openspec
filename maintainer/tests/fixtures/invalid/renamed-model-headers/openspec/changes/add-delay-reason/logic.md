# Logic

## Actions

| API name | Glossary term | Edits (object and link types) | Rules (create, modify, delete, link, function) | Status |
| --- | --- | --- | --- | --- |
| `ReportDelay` | `Delay reason` | `Shipment` | modify `Shipment` | new |

- `ReportDelay`
  - Parameters: `shipment: Shipment`, `reason: String`
  - Submission criteria: the user is a planner, or belongs to the Carrier on the Shipment; `reason` is one of the allowed reasons
  - Side effects: none

## Functions

None

## Writeback to other systems

None

## AIP Logic and agents

None
