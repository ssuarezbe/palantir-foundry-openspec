# Glossary

Domain terms used in specs. Use each term verbatim. Never use a forbidden synonym.
Add a row in the same change that introduces a new term.

- Term: the word as it appears in specs.
- Definition: one sentence.
- Ontology resources: the API names of every object type, link type and action type that represents the concept, separated by commas, or `not modelled`. One concept can need several; one resource can serve several concepts.
- Forbidden synonyms: words that must not appear in specs, separated by commas. Leave empty if none.

Rows whose term starts with `Example:` are samples. Checks skip them. Delete them when you add real terms.

| Term | Definition | Ontology resources | Forbidden synonyms |
| --- | --- | --- | --- |
| Example: Shipment | A load of goods moving from one site to another. | ExampleShipment, ExampleShipmentLeg, ExampleShipmentToCarrier | consignment, delivery |
| Example: Carrier | A company that moves a Shipment. | not modelled | haulier |
