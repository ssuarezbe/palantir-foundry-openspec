# Prompt: build `palantir-foundry-openspec`

Paste everything below the line into Claude Code (or another coding agent) on a **connected build machine** with Node 22.12+, npm, Bun and Python 3.11+. Fill in the three values in `<angle brackets>` first.

---

You are building **palantir-foundry-openspec**: an internal, curated packaging of OpenSpec for teams that build on Palantir Foundry inside a restricted network. The result is one Git repository that a team can bring into the company through an approved transfer, without npm access and without creating new Foundry repositories.

## Context

- Upstream: OpenSpec `@fission-ai/openspec` **1.16.0** (MIT), https://github.com/Fission-AI/OpenSpec. Pin this version everywhere.
- Target users work in three places:
  1. **AI FDE** in Foundry: no shell, no Node. Uses AIP skills (Name, Description, Markdown body) saved in a Compass folder. It edits Code Repositories on branches and reads their Checks.
  2. **Foundry VS Code workspaces**: remote terminal, Continue extension with Palantir models, Palantir MCP.
  3. **Laptops**: Windows, macOS, Linux, behind a VPN, Node may or may not be installed.
- TypeScript functions repositories run Jest tests in Checks on every commit. That is the CI gate.
- The Foundry Ontology is the business model. Specs refer to object types by API name; they don't redefine the model.
- Organisation: `<company name>`. Owner: `<team or person>`. Ontology export (optional): `<path to a JSON list of object type API names, or "none">`.

## Facts already verified (rely on them, re-check only if a step fails)

- `bun build node_modules/@fission-ai/openspec/bin/openspec.js --target=node --format=esm --outfile <dir>/dist/cli/openspec.mjs`, plus copying the package's `package.json` to `<dir>/` and `schemas/` to `<dir>/schemas/`, gives a working 2 MB CLI. Keep that layout: the CLI reads `package.json` two levels above itself. `bun build --compile` does **not** work (it can't find `package.json`).
- `openspec init --tools claude` writes 6 commands in `.claude/commands/opsx/` and 6 skills in `.claude/skills/openspec-*/`. `--tools continue` writes 6 prompts in `.continue/prompts/` and 6 skills in `.continue/skills/`.
- Templates and `schema.yaml` live in the package (`schemas/spec-driven/`), not in the project.
- Artifact order from `schema.yaml`: proposal → specs and design (both need proposal) → tasks (needs both) → apply (blocked until tasks exist).
- `openspec validate --all` errors (exit 1) on: a requirement with no `#### Scenario:`; a change with no delta (unless `.openspec.yaml` has `skip_specs: true`). A requirement without SHALL/MUST is only a **warning**; `--strict` makes warnings fail. Always use `--strict --no-interactive`.
- Telemetry goes to `edge.openspec.dev`; `OPENSPEC_TELEMETRY=0` turns it off.
- A Jest test that runs the bundle with `execFileSync(process.execPath, [cli, "validate", "--all", "--strict", "--no-interactive"])` passes on valid specs and fails with OpenSpec's message on invalid ones. It needs `"types": ["jest", "node"]` in `tsconfig.json`.

## Hard constraints

- No network access at runtime. Nothing in the repository downloads anything. Telemetry off in every launcher, test and doc example.
- No npm install scripts in anything shipped (`--ignore-scripts` when building). No new runtime dependencies beyond Node for Route A and Python standard library for the Python check.
- Keep OpenSpec's MIT licence text and copyright in `THIRD_PARTY_NOTICES.md`. Don't present this as an official OpenSpec or Palantir product. Note in the README that "Palantir" and "Foundry" are Palantir trademarks and the repository is internal; if it is ever published, rename it (for example `foundry-openspec-kit`).
- No Palantir proprietary content, customer data or credentials anywhere, including fixtures.
- Every AIP skill body must work with **no CLI**: zero `openspec` commands in `aip-skills/`. Enforce this with a test.
- Plain, short, imperative writing in all docs and skills. No marketing language.

## Repository to produce

```
palantir-foundry-openspec/
  README.md                      # what this is, which route to use, 10-minute quick start
  THIRD_PARTY_NOTICES.md         # OpenSpec MIT licence
  CHANGELOG.md
  VERSION                        # 1.16.0-foundry.1
  upstream/
    PIN.md                       # version, npm integrity hash, date, how it was built
    generated/                   # raw output of init --tools claude and --tools continue, untouched
  cli/
    openspec-1.16.0/             # the bundle: dist/cli/openspec.mjs, package.json, schemas/
    SHA256SUMS
    launchers/openspec           # sh: exec node "$(dirname "$0")/../openspec-1.16.0/dist/cli/openspec.mjs" "$@"
    launchers/openspec.cmd       # Windows equivalent, sets OPENSPEC_TELEMETRY=0
  schema/foundry-spec-driven/    # forked workflow (see below)
  aip-skills/                    # AI FDE versions, one file per skill
    openspec-explore.md
    openspec-propose.md
    openspec-apply.md
    openspec-archive.md
  workspace/
    .continue/                   # ready to copy into a Code Repository
    .claude/                     # for laptops with Claude Code
  project-template/
    openspec/config.yaml         # context and rules, glossary rule included
    openspec/glossary.md         # template
    openspec/specs/.gitkeep
    openspec/changes/archive/.gitkeep
  ci/
    typescript/openspec.test.ts  # runs the bundle
    typescript/glossary.test.ts  # glossary checks, pure TypeScript, no child process
    typescript/tsconfig.snippet.json
    python/test_openspec_rules.py  # standard-library port of the validation rules, for repos without Node
  scripts/
    build.sh                     # connected machine: npm install --ignore-scripts, bun build, copy, hash, zip
    sync-upstream.sh             # regenerate upstream/generated for a new version and show the diff
  tests/
    fixtures/valid/ ...          # small changes that must pass
    fixtures/invalid/ ...        # one fixture per rule: no scenario, no SHALL, no delta, forbidden synonym, unmapped term
    run-all.sh                   # runs every check below
  docs/
    01-routes.md                 # Route A (bundle), B (no Node, written rules), C (AI FDE)
    02-ai-fde-skills.md          # step by step: Compass folder, Create new skill, Save as, Manage skill set, Load skills, pre-fill links
    03-vscode-workspace.md       # terminal, Continue prompts, launcher, validate before commit
    04-ci-gate.md                # Jest gate, tsconfig, branch protection, what to confirm in Foundry
    05-glossary-and-ontology.md  # how rules, glossary and Ontology fit together
    06-upgrade.md                # moving to a new OpenSpec version
```

## Work steps

1. **Build the CLI** with `scripts/build.sh`. Record the npm integrity hash and SHA-256 of `openspec.mjs` in `upstream/PIN.md` and `cli/SHA256SUMS`. Run `npm audit signatures` and record the result; if it can't reach the registry keys, say so in `PIN.md`.
2. **Generate upstream output** into `upstream/generated/` with `init --tools claude` and `init --tools continue` in empty folders. Don't edit these files; they are the reference for diffs.
3. **Fork the workflow** with `openspec schema fork spec-driven foundry-spec-driven` (this command is experimental, so pin to 1.16.0). Change only the templates and instructions, not the artifact order:
   - spec template: each requirement may name the Ontology object type or action type it touches, as `Ontology: <ApiName>`; use glossary terms verbatim;
   - proposal template: add `## Glossary changes` (new or changed terms);
   - design template: add `## Foundry resources` (datasets, transforms, object types, action types, functions affected).
   Run `openspec schema validate foundry-spec-driven` and fix until clean.
4. **Write `project-template/openspec/config.yaml`** with `schema: foundry-spec-driven`, a `context:` that says specs use terms from `openspec/glossary.md` verbatim and add any new domain noun there in the same change, and `rules:` per artifact for the glossary and the Ontology references.
5. **Write the glossary template** as a Markdown table: `Term | Definition | Ontology API name (or "not modelled") | Forbidden synonyms`. Include two fake example rows clearly marked as examples.
6. **Write the four AIP skills.** Start from `upstream/generated/.claude/skills/`. For each one:
   - First lines: `Name:` and `Description:`. The description says *when* to load the skill.
   - Replace every CLI call with written steps: create the folder; check which files exist; follow the artifact order; paste the template headings inline; apply the validation rules as a checklist; on archive, ask the user to confirm, merge ADDED/MODIFIED/REMOVED/RENAMED blocks into `openspec/specs/<capability>/spec.md`, and move the change to `openspec/changes/archive/YYYY-MM-DD-<name>/`.
   - Add: work on a branch of the Code Repository; never commit to main; after committing, read Checks; if the OpenSpec or glossary check fails, fix the named file and commit again.
   - Add: use Exploration mode to confirm that every `Ontology:` reference exists before proposing.
   - Keep each skill under about 150 lines.
7. **Prepare `workspace/`**: copy the generated `.continue/` and `.claude/` folders and change their CLI calls to use the launcher in `cli/launchers/` (or the `node .../openspec.mjs` path) with telemetry off.
8. **Write the CI checks.**
   - `openspec.test.ts`: the verified Jest test, with the repository root found from `__dirname`, and a clear error message.
   - `glossary.test.ts`: parse `openspec/glossary.md`; fail if a term has no definition; fail if a forbidden synonym appears in `openspec/specs/**` or open changes (whole word, case-insensitive, ignore code blocks); if an Ontology export JSON exists in the repo, fail on any `Ontology:` reference or glossary API name not in it.
   - `test_openspec_rules.py`: standard-library port of the same validation rules (scenario required, SHALL/MUST required, at least one delta per change unless `skip_specs: true`) plus the glossary rules, for Python repositories.
9. **Prove the checks** with fixtures. `tests/run-all.sh` must:
   - run the bundle's `validate --all --strict` on every fixture and compare pass/fail with the expected result;
   - run the Jest tests against a copy of each fixture tree;
   - run the Python port on the same fixtures and confirm it agrees with the bundle on every fixture (parity);
   - grep `aip-skills/` and fail if it contains `openspec ` commands;
   - check that no file in the repository contains a URL other than the documentation links, and that every launcher sets `OPENSPEC_TELEMETRY=0`.
10. **Write the docs.** Each doc starts with a three-line summary, then numbered steps, then "What to confirm in Foundry". Mark clearly what was tested here and what can only be tested inside Foundry: the Node version Checks uses, whether Checks allow a child process, whether the repository's `tsconfig` accepts Node types, and any AIP skill size limit.
11. **Package**: `scripts/build.sh --release` creates `palantir-foundry-openspec-1.16.0-foundry.1.zip` and its SHA-256, ready for the approved transfer process.

## Acceptance criteria

- [ ] `tests/run-all.sh` passes from a clean clone with no network access (disconnect or block outbound traffic to prove it).
- [ ] Every invalid fixture fails for the expected reason, in the bundle, in Jest and in the Python port.
- [ ] `aip-skills/` contains no CLI calls, and each skill has `Name:` and `Description:` lines.
- [ ] `openspec schema validate foundry-spec-driven` is clean.
- [ ] A fresh project made from `project-template/` plus `workspace/.continue/` runs `validate --all --strict` successfully on its empty specs.
- [ ] README quick start takes a new user from zip to first validated change in under 10 minutes, for each route.
- [ ] `THIRD_PARTY_NOTICES.md`, `PIN.md` and `SHA256SUMS` are complete.

## How to report back

When you finish, give me: the file tree; the result of `tests/run-all.sh`; the hashes; anything you couldn't verify; and every place where you departed from this prompt and why. Ask me before changing the artifact order, adding a dependency, or making any network call outside the build step.
