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

## Automations

| Name | Trigger (time, object set change, threshold) | Condition | Effect (action, notification, function) | Status |
| --- | --- | --- | --- | --- |
| `Notify planner of delay` | object set change: a `Shipment` gets a Delay reason | the reason is Customs or Breakdown | notification to the planners group | new |

## Writeback to other systems

None

## AIP Logic and agents

None
