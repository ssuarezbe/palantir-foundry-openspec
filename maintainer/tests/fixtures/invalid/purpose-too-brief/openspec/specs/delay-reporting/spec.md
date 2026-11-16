# delay-reporting Specification

## Purpose
Delays.

## Requirements

### Requirement: Record delay
The system SHALL record a delay reason for a Shipment.

#### Scenario: Reason recorded
- **GIVEN** a Shipment is late
- **WHEN** the planner enters a reason
- **THEN** the reason is stored
