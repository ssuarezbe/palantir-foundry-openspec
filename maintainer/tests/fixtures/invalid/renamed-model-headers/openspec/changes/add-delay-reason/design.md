# Design

## Context

Shipments already exist in the Ontology. Staff read them in an operations view. Late Shipments are known from the planned and actual arrival dates.

## Goals / Non-Goals

**Goals:**
- Store one Delay reason per late Shipment and show it where staff already look.

**Non-Goals:**
- Notify the Carrier's own system (Q2).
- Predict delays.

## Decisions

- Store the reason as two properties on `Shipment`, not as a new object type. One reason per Shipment, no history needed yet. Alternative: a `DelayReport` object type; rejected until history is required.
- One action, `ReportDelay`, edits the properties through a rule. No function needed.

## Foundry resources

Object type `Shipment` (changed) and dataset `shipments_clean` (changed) in `ontology.md`; action `ReportDelay` (new) in `logic.md`.

## Risks / Trade-offs

A second report overwrites the first. Accepted until Q2 or a history need appears.

## Migration Plan

None. The properties start empty; nothing is backfilled.
