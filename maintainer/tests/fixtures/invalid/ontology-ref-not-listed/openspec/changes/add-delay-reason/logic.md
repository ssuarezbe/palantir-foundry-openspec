# Logic

## Actions

| API name | Glossary term | Edits (object and link types) | Parameters | Rules (create, modify, delete, link, function) | Submission criteria (who, what must be true) | Side effects (notification, webhook, schedule) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ReportDelay` | `Delay reason` | `Shipment` | `shipment: Shipment`, `reason: String` | modify `Shipment` | The user is a planner, or belongs to the Carrier on the Shipment; `reason` is one of the allowed reasons | None | new |

## Functions

None

## Writeback to other systems

None

## AIP Logic and agents

None
