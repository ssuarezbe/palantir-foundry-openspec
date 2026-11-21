# Infrastructure rules

Owner: Infrastructure
Source: <document name and version> (example)
Copied: <date>
ID prefix: INF-

## Storage map

| ID | Resource kind | Location pattern | Rule | Authority |
| --- | --- | --- | --- | --- |
| Example: INF-S1 | dataset | `/<domain>/<layer>/<dataset name>` with layers `raw`, `clean`, `curated` | Raw data is never read by an application. | Platform standard, section 2 |
| Example: INF-S2 | transform or pipeline | next to its output dataset | One pipeline owns each output dataset. | Platform standard, section 3 |

## Infrastructure rules

| ID | Applies to | Rule | Level | Authority |
| --- | --- | --- | --- | --- |
| Example: INF-001 | ontology.md Backing data | Every dataset behind an object type has an owner and an update cadence. | must | Platform standard, section 4 |
| Example: INF-002 | ontology.md Backing data | Every dataset behind an object type has at least one data quality check. | should | Platform standard, section 5 |
