# The rulebook: `openspec/rulebook/`

The rulebook holds the company's rules for building on Foundry: naming, scope (who can access what, by name), storage, data classification, decision guides (for example when to use a dataset) and process. Other teams own those rules. The rulebook keeps them as short, citable rows with a pointer to the source document, so an assistant reads them and a reviewer can check a change against them.
It is a project-level artifact like the glossary, not a per-change file. It does not change the artifact graph. Each change records its compliance in one table, `## Rulebook review` in `design.md`.
Not tested: any model applying the rules. The template rows are invented examples (they start with `Example:`) and claim nothing about Foundry or your company.

## 1. What is in it

| File | Owner (example) | Sections |
| --- | --- | --- |
| `README.md` | whoever owns the rulebook in the repository | the file table, precedence, class names, how to read and keep it |
| `governance.md` | data governance | Naming rules, Decision guides, Process rules (prefix `GOV-`) |
| `security.md` | cloud security | Classification map, Scope map, Access rules (prefix `SEC-`) |
| `infrastructure.md` | infrastructure | Storage map, Infrastructure rules (prefix `INF-`) |

Four kinds of row, all with an `ID` first column:

| Kind | Columns | Use it for |
| --- | --- | --- |
| Rule | ID, Applies to, Rule, Level (`must`, `should`, `retired`), Authority | naming, storage, access, process |
| Decision guide | ID, Question, Use it when, Do not use it when, Use instead, Authority | "dataset or not", "action or function" |
| Classification map | ID, Class, Marking, Access, Storage and retention, AI agents and approval | what each data class allows |
| Map | ID, Name pattern or resource kind, Location or space, Marking or rule, Groups | access by name, where things live |

## 2. How a change uses it

1. Explore and Propose read `rulebook/README.md`, then only the rows whose `Applies to` fits the artifact being written.
2. Every object type and dataset in `ontology.md` carries a `classification:` line naming a class. Access is derived from the classification map and the scope map, with rule IDs cited.
3. A rule that needs an approval or a decision (publishing PII, for example) becomes a blocking row in `open-questions.md`. The existing gate then stops `tasks.md` and `apply` until someone answers it.
4. `design.md` ends its review with `## Rulebook review`: one row per applicable rule (`complies`, `deviates` with a reason, or `open` with a question).
5. Apply follows the review. Archive confirms each row still matches what was built.

## 3. Fill it in (the digest)

The owning teams probably publish documents, not rows. Someone has to turn them into rows.

- **Option A (best).** Give each team the file template and ask them to publish rows. Accuracy is highest. It needs their agreement.
- **Option B (start here).** Your team writes the rows from their documents. Keep each rule to one sentence, give it an ID and put the document and section in `Authority`. Ask the owning team to review the file once.
- Rules a reader cannot check against an artifact ("be secure") do not belong. Rewrite them or leave them in the source document.
- Set the `Source:` and `Copied:` lines when you copy a file. A copy older than the owner's latest version is stale: refresh it and bump the line.
- Delete every `Example:` row when you add real ones. Until a file has a real row, the checks skip the rulebook.

## 4. Customize it

What you can change freely, and what you must keep so the checks and skills keep working.

| You want to | Change | Keep |
| --- | --- | --- |
| Use your own owner teams | Rename, add or delete files; update the table in `rulebook/README.md` | One ID prefix per file; files other than `README.md` in `openspec/rulebook/` |
| Use your own class names | Rows in the classification map and the `Classes` line of the README | A `classification:` line per object type and dataset |
| Change who wins a conflict | The `Precedence` section of the README (and the same line in `config.yaml`) | One stated order |
| Add a rule kind (for example retention, regulatory) | A new section with an `ID` first column in the owner's file | The `ID` header and the ID format `<2-5 capitals>-<letters or digits>` |
| Add a rule for one project only | A file `project.md` with prefix `PRJ-`, listed in the README | A project rule may tighten a company rule, never loosen it. Say so in the README |
| Add a regulated area (GxP, finance) | A section or a file with its own prefix and a `Applies to` of the artifacts it touches | Approval rules become blocking open questions |
| Rename `Applies to` values | The column values | Use the artifact file and section names (`ontology.md Access`) so a reader can filter |
| Skip the rulebook for a small team | Leave only `Example:` rows, or delete the folder | The skills then write "No rulebook" in the Rulebook review. Nothing fails |
| Make a rule checkable by a gate | Add a `Pattern` column (a regular expression) and a check of your own | The kit's checks do not read it today |
| Pass 100 rows in one file | Split by section into `<owner>-<topic>.md` and list each file in the README | IDs never change or get reused |
| Use it across several repositories | Keep it in the spec home only (`docs/multi-repo.md`); satellites carry none | One copy, one stamp |

What the checks read (only where a gate runs): the folder `openspec/rulebook/`, rows whose first cell is an ID under a header named `ID`, the `Example:` prefix, and in each change that has `tasks.md`: `design.md` has `## Rulebook review` with a table whose header starts with `Rule`, every ID exists in the rulebook, every result is `complies`, `deviates` or `open`, and a deviation or open row has a reason. Keep those names if you rename anything else.

## 5. Keep it true

- **Review.** A pull request that changes a rule in a company document should also refresh the matching file. Reviewers check the `Copied:` date against the source version.
- **Audit.** Ask Explore to compare each file's `Source:` line with the owner's current version. It cannot read the owner's document unless you give it, so the user supplies the current version.
- **Gate.** In situations 2 to 4 the checks catch a change that cites a rule that does not exist or skips the review. They cannot catch a wrong row.
- **Size.** About 50 rules fit in three files. Past 100 rows in one file, split it.

## 6. Other options

| Option | Choose it when | Cost |
| --- | --- | --- |
| This folder, copied into the spec home (default) | AI FDE is your only tool | A digest and refresh steps |
| OpenSpec `references:` to a rulebook store | Node is available and you want one live source | The CLI and a per-machine registry. A reference names a store, not a version, and AI FDE cannot use it |
| One store with code owners per folder | One team owns everything | Couples all reviews |
| A "Company Standards" AIP skill kept in Compass by governance | Governance already owns Compass skills | Repo reviewers and checks cannot see it. The skill size limit is not confirmed |
| Machine-readable policies (ODRL), data contracts (ODCS) | You exchange data with other organizations in a data space | A separate project. Not covered here, and not checked against Foundry |
| A generator that builds the files from the source documents | The source is structured and Node or Python is available | A script you maintain. Keep the folder format so the checks keep working |

## 7. What to confirm

- That each owning team accepts the rows as a faithful digest of their documents.
- That your classification names match the ones your security team uses.
- That an assistant applies the rows: take ten real rules, seed a change that breaks two, and see whether the Rulebook review catches them.
- Whether AI FDE can read every file in the folder within its context. If not, split by owner and read only the ones that apply.
