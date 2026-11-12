# Glossary and Ontology

The Ontology is the business model. Specs do not redefine it. They name object types and action types by API name and use one agreed word for each domain noun.
Three things enforce this: rules in `openspec/config.yaml`, the table in `openspec/glossary.md` and the checks in `docs/setup.md`.
Tested here: all rules, on fixtures. Not tested here: a real Ontology export.

## Steps

1. Open `openspec/glossary.md`. It is a table: `Term | Definition | Ontology API name | Forbidden synonyms`.
2. Add one row per domain noun.
   - Term: the word as specs use it.
   - Definition: one sentence. Empty definitions fail the check.
   - Ontology API name: the object type API name, or `not modelled`.
   - Forbidden synonyms: comma-separated words that must not appear in specs.
3. Delete the two `Example:` rows. Checks skip them, but they are noise.
4. In a spec, use the term verbatim. When a requirement reads or changes an Ontology object type or action type, add one line under the requirement text: `Ontology: <ApiName>`. Use the exact API name. Leave the line out when no Ontology resource is involved.
5. A change that adds a noun adds its row in the same change. The proposal's `## Glossary changes` section lists it. The tasks include "update glossary".
6. Optional: add `openspec/ontology.json` (a JSON list of API names). Then every `Ontology:` line and every glossary API name must be in it.
7. Run the checks. A forbidden synonym in a spec fails with the file and line.

## Where each rule lives

- `core/project-template/openspec/schemas/foundry-spec-driven/`: the templates. Specs get an optional `Ontology:` line, proposals get Glossary changes, designs get Foundry resources.
- `core/project-template/openspec/config.yaml`: `context:` and `rules:` that every assistant reads.
- AIP skills and workspace prompts: Explore confirms API names before you propose.
- `addons/ci/`: the failing checks.

The schema lives only in the project template. There is no second copy to keep in step.

## What to confirm in Foundry

- How you export object type API names to `openspec/ontology.json`. The kit does not do this for you.
- Whether the Ontology tools in AI FDE and the Palantir MCP return API names in the same spelling as Ontology Manager.
- Who owns the glossary and who approves new terms.
