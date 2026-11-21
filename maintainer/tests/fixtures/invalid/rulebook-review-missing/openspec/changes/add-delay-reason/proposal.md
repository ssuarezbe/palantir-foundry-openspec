# Proposal

## Why

Operations staff cannot see why a Shipment is late, so they phone the Carrier. A recorded Delay reason lets them act without calling.

## What Changes

A Carrier or planner reports a Delay reason on a Shipment. Staff see it on the Shipment and can filter late Shipments by reason.

## Capabilities

### New Capabilities
- `delay-reporting`: record and show the Delay reason of a late Shipment

## Glossary changes

New term: Delay reason (maps to `Shipment` and the action `ReportDelay`).

## Impact

Object type `Shipment` gains two properties (dataset `shipments_clean` changes with it). New action `ReportDelay` and automation `Notify planner of delay`. No change to other Ontology resources. Detail in `ontology.md` and `logic.md`.
