# Spec Delta

## Purpose

Record why a Shipment is late so that operations staff can act on the cause without phoning the Carrier.

## ADDED Requirements

### Requirement: Report a Delay reason
The system SHALL let the Carrier on a Shipment, or a planner, report a Delay reason for a late Shipment.
Ontology: Shipment, ReportDelay, CancelShipment

#### Scenario: Carrier reports a delay
- **GIVEN** a Shipment is late and its Carrier is signed in
- **WHEN** the Carrier reports the Delay reason <reason>
- **THEN** the Shipment shows the Delay reason <reason>
- **AND** the time of the report

**Examples**

| reason |
| --- |
| Weather |
| Customs |

#### Scenario: Another Carrier is refused
- **GIVEN** a Shipment carried by Carrier A
- **WHEN** a user of Carrier B reports a Delay reason
- **THEN** the report is refused
- **BUT** the Shipment is not changed
