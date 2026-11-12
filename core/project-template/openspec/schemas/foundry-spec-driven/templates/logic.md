# Logic

<!-- The behavior this change adds, changes or reads. Read openspec/ontology-design.md first. Use API names. Write "None" under a heading with nothing to record. -->

## Actions

| API name | Glossary term | Edits (object and link types) | Parameters | Rules (create, modify, delete, link, function) | Submission criteria (who, what must be true) | Side effects (notification, webhook, schedule) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<ActionApiName>` | `<term>` | `<ObjectType>` | `<name>: <type>` | `<rule>` | `<rule in words>` | | new / changed / read |

## Functions

| API name | Language | Kind (rule, model, LLM, orchestration) | Inputs | Output | Reads | Edits (create, update, delete, link) | Used by | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<functionName>` | TypeScript / Python | rule | `<name>: <type>` | `<type>` | `<ObjectType>` | `<ObjectType>: update` | `<function-backed action, app, AIP Logic>` | new / changed / read |

## Writeback to other systems

<!-- Changes that must reach an operational system outside Foundry. Write "None" if the Ontology is the only record. -->

| Action or function | Target system | Mechanism (webhook, change data capture, other) | If the target is down |
| --- | --- | --- | --- |
| `<ActionApiName>` | `<system>` | `<mechanism>` | `<retry, queue, fail>` |

## AIP Logic and agents

| Name | Input | Output | Tools it may call (functions, actions, Ontology queries) | Human review before write | Evaluation cases |
| --- | --- | --- | --- | --- | --- |
| `<name>` | `<type>` | `<type>` | `<tool>` | yes / no | scenario "<name>" of <capability> |
