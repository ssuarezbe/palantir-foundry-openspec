# Open Questions

| ID | Stage | Question | Blocking | Affects | Owner | Status | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 | proposal | Which reasons are allowed? | yes | delay-reporting | Ops lead | answered | Weather, Customs, Breakdown, Other. Ops lead agreed on 2026-11-12. |
| Q2 | design | Must a delay also reach the Carrier's own system? | no | logic.md | Integration team | assumed | No for now. Revisit if Carriers ask. |
| Q3 | ontology | Can a Carrier user run `ReportDelay` for another Carrier's Shipment? | yes | logic.md, ontology.md | Security owner | answered | No. Only the Carrier on the Shipment, or a planner. |
