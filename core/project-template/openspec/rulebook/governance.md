# Governance rules

Owner: Data governance
Source: <document name and version> (example)
Copied: <date>
ID prefix: GOV-

## Naming rules

| ID | Applies to | Rule | Level | Authority |
| --- | --- | --- | --- | --- |
| Example: GOV-001 | ontology.md Object types | Object type API names are singular PascalCase nouns. | must | Naming standard, section 2 |
| Example: GOV-002 | logic.md Actions | Action API names start with a verb. | should | Naming standard, section 4 |
| Example: GOV-003 | ontology.md Backing data | Dataset names are lowercase with underscores and end with a layer suffix (`_raw`, `_clean`). | must | Naming standard, section 6 |

## Decision guides

| ID | Question | Use it when | Do not use it when | Use instead | Authority |
| --- | --- | --- | --- | --- | --- |
| Example: GOV-D1 | Store the data as a dataset? | The data feeds the Ontology, needs history, or is read often. | The data is read rarely and already lives in a governed source. | A virtual table, if your enrollment has them. | Data architecture guide |

## Process rules

| ID | Applies to | Rule | Level | Authority |
| --- | --- | --- | --- | --- |
| Example: GOV-P1 | proposal.md, open-questions.md | A change that publishes data classified PII needs the data owner's approval before tasks are written. Record it as a blocking open question. | must | Data governance policy |
| Example: GOV-P2 | proposal.md | A change that removes or renames a published property is marked **BREAKING** and lists its consumers. | must | Change management policy |
