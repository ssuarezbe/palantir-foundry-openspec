# Tasks

## 1. Data

- [ ] 1.1 Add the two columns to `shipments_clean`
  - **Verify:** the dataset preview shows `delayReason` and `delayReportedAt`, empty for existing rows.

## 2. Ontology

- [ ] 2.1 Add the two properties to `Shipment` in Ontology Manager
  - **Verify:** `Shipment` lists both properties and the backing dataset maps them.

## 3. Logic

- [ ] 3.1 Create the action `ReportDelay` with its submission criteria
  - **Verify:** scenario "Carrier reports a delay" passes for the Carrier on the Shipment.
- [ ] 3.2 Test the refusal
  - **Verify:** scenario "Another Carrier is refused" passes and the Shipment is unchanged.
