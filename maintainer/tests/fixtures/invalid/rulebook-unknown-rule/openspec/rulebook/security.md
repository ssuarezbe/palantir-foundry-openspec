# Security rules

Owner: Cloud security
Source: Security standard v1 (invented for this example)
Copied: 2026-11-13
ID prefix: SEC-

## Classification map

| ID | Class | Marking | Access (read; act or edit) | Storage and retention | AI agents and approval |
| --- | --- | --- | --- | --- | --- |
| SEC-C1 | internal | `LOGI-Internal` | all employees; the Logistics team | the logistics space; 5 years | allowed; no approval |

## Access rules

| ID | Applies to | Rule | Level | Authority |
| --- | --- | --- | --- | --- |
| SEC-002 | logic.md Actions | An action that edits an internal property names the group that may run it. | must | Security standard, section 5 |
