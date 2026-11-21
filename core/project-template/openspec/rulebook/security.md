# Security rules

Owner: Cloud security
Source: <document name and version> (example)
Copied: <date>
ID prefix: SEC-

## Classification map

| ID | Class | Marking | Access (read; act or edit) | Storage and retention | AI agents and approval |
| --- | --- | --- | --- | --- | --- |
| Example: SEC-C1 | internal | `<marking name>` | all employees; owning team | any project in the domain space; 5 years | allowed; no approval |
| Example: SEC-C2 | confidential | `<marking name>` | the owning team and named groups; owning team | the domain's restricted project; 3 years | allowed inside the platform; security approval for any external model |
| Example: SEC-C3 | PII | `<marking name>` | named groups only; named groups only | the PII project only; per the retention policy | not allowed unless the data owner approves; data owner approval before publish |

## Scope map

| ID | Name pattern or domain | Space or project | Marking | Groups (read; act) |
| --- | --- | --- | --- | --- |
| Example: SEC-S1 | `hr_*`, human resources | `<HR space>` | `<HR marking>` | `<hr-readers>`; `<hr-operators>` |
| Example: SEC-S2 | `logistics_*`, logistics | `<logistics space>` | `<logistics marking>` | `<logistics-readers>`; `<logistics-operators>` |

## Access rules

| ID | Applies to | Rule | Level | Authority |
| --- | --- | --- | --- | --- |
| Example: SEC-001 | ontology.md Access | Never duplicate an object type to separate access. Use markings or restricted views. | must | Security standard, section 3 |
| Example: SEC-002 | logic.md Actions | An action that edits a confidential or PII property names the group that may run it. | must | Security standard, section 5 |
