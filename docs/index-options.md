# The index: `openspec/INDEX.md`

`openspec/INDEX.md` is one Markdown file that tells an agent where things are: the capabilities, the Foundry resources (objects, links, actions, functions, automations, AIP Logic, datasets) and the open changes. It holds pointers, not schemas. Foundry holds the live model; the specs hold behavior; the changes hold the reason.
This guide covers how it is kept true with no code, what to add when you have Python or Node, and the other ways to build the same thing so you can improve or replace it.
Not tested: any model using the index. It is worth keeping only if agents find things faster with it, so try it on a real change first.

## 1. It works with AI FDE only

- It is a plain Markdown file in `core/project-template/openspec/`. Every situation copies it, including situation 1 (no shell, no Node, Checks run no tests). `drop-in/situation-1/openspec/INDEX.md` has it.
- The skills maintain it with no CLI: Propose adds an In flight row, Archive moves it into Capabilities and Resources, Explore reads it first and can audit it. `run-all.sh` fails if a skill contains a CLI call or does not mention the index.
- Nothing about it needs a gate. The gates (situations 2 to 4) only add a drift check.

## 2. Keep it true: the ladder

Use the first rungs you have. Each rung adds to the one before.

| Rung | Needs | What it does |
| --- | --- | --- |
| 1. Skills | AI FDE | Propose adds the In flight row. Archive updates Capabilities and Resources in the same pull request. |
| 2. Review rule | A person | The review list in `docs/ai-fde.md` (item 9): a pull request that touches `openspec/specs/` or `changes/archive/` also changes `INDEX.md`. The Git diff shows it. No tool needed. |
| 3. Audit | AI FDE | Explore, "Audit the index": list folders and compare. Capabilities against `specs/`, In flight against `changes/`, Resources against every `Ontology:` line, Last changed against the archive folder names, names against the Ontology tools. Report first, fix on a yes, then set `Last audited:`. Run it every month and before each release. |
| 4. Date stamp | Nothing | The `Last audited:` line at the top. A reviewer sees how old the last audit is without running anything. |
| 5. Drift check | Jest or Python in Checks (situations 2 to 4) | Fails the commit when a main spec cites an `Ontology:` name that has no row under Resources. The check also reads `openspec/index/*.md` once the file is split. |
| 6. Generator | Python or Node on a laptop, workspace or CI | Optional. Section 4. |

What no rung catches: a row that exists but describes the wrong thing, and a stale Last changed. The audit and the review catch some. Only a reader catches the rest.

## 3. Size

One file works to roughly 300 rows. After that it splits per capability, with the root as a map. When Resources passes 300 rows, move the rows to `openspec/index/<capability>.md`, keep one row per capability in `INDEX.md` that links to its file, and keep every resource findable from the root. The drift check already reads `openspec/index/*.md`.

## 4. With Python or Node: improve it, enhance it or replace it

The kit ships no generator, to stay lean where AI FDE is the only tool. If you have an interpreter you can add one without changing anything else, because the inputs are fixed.

What a generator can read, all of it already parseable:

- `specs/<capability>/spec.md`: the Purpose (first line) and every `Ontology:` line.
- `changes/**/ontology.md` and `logic.md`: the tables whose header starts with `API name` (the checks require it), and the Automations table (header starts with `Name`).
- `changes/archive/` folder names: Last changed.
- `changes/*/open-questions.md`: the count of rows with Blocking `yes` and Status `open`.
- `glossary.md`: the term for each resource.

What to keep stable if you replace the file, so the kit's checks and skills keep working: the path `openspec/INDEX.md`, a `## Resources` table whose header starts with `API name`, API names in the first column (comma-separated when a row has several), and the `Example:` prefix rule.

## 5. Other options

| Option | Choose it when | Cost | Note |
| --- | --- | --- | --- |
| Keep `INDEX.md` as shipped | AI FDE is your only tool | Skills and a review rule | The default. |
| Generator (Python or Node) | Drift keeps happening, or you pass 300 rows | A script in a repo with a runtime, run on a laptop or in CI | Generate, commit the result; Checks run the existing drift check. Do not make AI FDE depend on it. |
| Split per capability | Resources passes 300 rows | Section 3 | No tooling needed. |
| `AGENTS.md` at the repository root | Several agents or tools open the repo | One line: "Start at `openspec/INDEX.md`." | Keep it short. Do not copy the index into it. |
| Live Ontology tools (the Palantir MCP for builders, Ontology MCP for consumers) | You need current types, properties or actions | Access and review under your policies | Complements the index. They hold live state and do not hold specs, history or reasons. Their coverage of properties and links was not confirmed in our reading of the Ontology MCP overview. |
| `ontology.json` export | You want a hard name list for the checks | A refresh step (`docs/setup.md`) | Names only. The index rows can feed it. |
| `llms.txt` | You publish documentation for outside readers | A file | Not for an internal repository: it points to documentation of dependencies, and the evidence of benefit is weak. |
| HTML view | People want to browse it | A renderer over the Markdown | Not for agents: more tokens, same facts. Render it from the Markdown, never edit it. |
| A catalogue inside Foundry (for example a dataset or object type of specs) | You want search and permissions in the platform | Pipeline and review work, not designed or tested here | Possible. The Markdown file stays the source until you trust the copy. |

## 6. What to confirm

- That AI FDE can read and edit `openspec/INDEX.md` the same way it edits other repository files.
- That the Explore audit finishes on your repository size. The audit lists folders and reads every spec, so a very large repository may need the split first.
- That the index helps: ask an agent a navigation question ("which specs and changes touch `Shipment`?") with and without it, and compare.
