# delay-reporting Specification

## Purpose
Record why a Shipment was late so planners can act on the cause.

## Requirements

### Requirement: Record delay
The system SHALL record a delay reason for a Shipment.
Ontology: ReportDelay

#### Scenario: Reason recorded
- **GIVEN** a Shipment is late
- **WHEN** the planner enters a reason
- **THEN** the reason is stored
