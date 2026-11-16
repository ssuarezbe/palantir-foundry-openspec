# Spec Delta

## Purpose

Records why a Shipment is late so that operations staff can act on it quickly.

## ADDED Requirements

### Requirement: Record delay reason
The system SHALL store a delay reason on a Shipment.
Ontology: Shipment

#### Scenario: Reason saved
- **WHEN** a Carrier reports a delay
- **THEN** the Shipment shows the delay reason
