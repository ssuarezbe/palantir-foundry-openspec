# Spec Delta

## Purpose

Records why a Shipment is late so that operations staff can act on it quickly.

## ADDED Requirements

### Requirement: Record delay reason
The system SHALL store a delay reason on a Shipment.
Ontology: Shipment
Implemented in: ontology action RecordDelay, ts-functions recordDelay, react-app shipment page

#### Scenario: Reason saved
- **GIVEN** a Shipment that is 2 hours late
- **AND** the user is a Carrier coordinator
- **WHEN** the user records the reason "port closed"
- **THEN** the Shipment shows the delay reason "port closed"
- **AND** the time of the entry is recorded

#### Scenario: Reason refused for an on-time Shipment
- **GIVEN** a Shipment that is on time
- **WHEN** the user records a delay reason
- **THEN** the system refuses the entry
- **BUT** the Shipment is left unchanged

#### Scenario: Reason by role
- **GIVEN** a user with role <role>
- **WHEN** the user records a delay reason on a late Shipment
- **THEN** the entry is <result>

**Examples**

| role | result |
| --- | --- |
| Carrier coordinator | accepted |
| Viewer | refused |
