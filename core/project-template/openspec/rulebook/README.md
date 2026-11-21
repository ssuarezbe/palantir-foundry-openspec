# Rulebook

The company's rules for building on Foundry: naming, scope, storage, data classification, decision guides and process. Other teams write them. This folder holds them as short rows, each with a pointer to the source document, so an assistant can read them and a reviewer can cite them. It does not replace the source documents.

Every change records, in `design.md` under `## Rulebook review`, each rule that applies to it and whether it complies, deviates or needs an answer.

## Files

| File | Owner | ID prefix | Holds | Version and copy date |
| --- | --- | --- | --- | --- |
| `governance.md` | Data governance | `GOV-` | Naming rules, decision guides (for example when to use a dataset), process rules | see the file's `Source:` and `Copied:` lines |
| `security.md` | Cloud security | `SEC-` | Classification map, scope map (access by name), access rules | same |
| `infrastructure.md` | Infrastructure | `INF-` | Storage map, infrastructure rules | same |

Add, rename or remove files to match your company: `docs/rulebook.md` in the kit says how. Keep this table true.

## Precedence

When two rules conflict, the first wins: security, then governance, then infrastructure, then the kit's `openspec/ontology-design.md`. Change the order here if your company decides otherwise. A deviation is allowed only with a reason in the Rulebook review and, for a `must` rule, an answered open question.

## Classes

The classification map in `security.md` names the classes. This kit's examples use: public, internal, confidential, sensitive, PII. Replace them with yours. Every object type and every dataset in a change carries a `classification:` line naming one of these.

## How to read it

1. This file.
2. Only the owner files and sections whose `Applies to` matches the artifact you are writing.
3. Skip any row whose first cell starts with `Example:`. If every row is an example, the rulebook is not filled in: say "No rulebook" in the Rulebook review and tell the user.

## How to keep it true

- A rulebook file is copied from its owner. Update the `Source:` and `Copied:` lines each time. A copy older than the owner's latest version is stale: ask the user to refresh it.
- Never edit a rule here to make a change pass. Raise a deviation.
- IDs are never reused. A retired rule stays with `Level` set to `retired`.
- One file works to roughly 100 rows. After that it splits by section into `openspec/rulebook/<owner>-<topic>.md`, and this table lists each file.
- Rows whose first cell starts with `Example:` are samples. Checks skip them. Delete them when you add real rows.
