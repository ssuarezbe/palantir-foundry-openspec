# Logic

<!-- The behavior this change adds, changes or reads. Read openspec/ontology-design.md first. If the change adds or changes no action, function or AIP Logic, replace everything below with "None" and one line saying why. Use API names. Write "None" under a heading with nothing to record. Keep the table headers as they are: the checks read them. -->

## Actions

| API name | Glossary term | Edits (object and link types) | Rules (create, modify, delete, link, function) | Status |
| --- | --- | --- | --- | --- |
| `<ActionApiName>` | `<term>` | `<ObjectType>` | modify `<ObjectType>` | new / changed / read |

<!-- One block per new or changed action. -->

- `<ActionApiName>`
  - Parameters: `<name>: <type>`, `<name>: <type>`
  - Submission criteria: <who may run it and what must be true>
  - Side effects: <notification, webhook, schedule, or none>

## Functions

| API name | Kind (rule, model, LLM, orchestration) | Reads | Edits (create, update, delete, link) | Used by | Status |
| --- | --- | --- | --- | --- | --- |
| `<functionName>` | rule | `<ObjectType>` | `<ObjectType>: update` | `<function-backed action, app, AIP Logic>` | new / changed / read |

<!-- One block per new or changed function. A function that edits takes effect only through the function-backed action named under "Used by". -->

- `<functionName>` (TypeScript / Python)
  - Inputs: `<name>: <type>`
  - Output: `<type>`

## Writeback to other systems

<!-- Changes that must reach an operational system outside Foundry. Write "None" if the Ontology is the only record. -->

| Action or function | Target system | Mechanism (webhook, change data capture, other) | If the target is down |
| --- | --- | --- | --- |
| `<ActionApiName>` | `<system>` | `<mechanism>` | `<retry, queue, fail>` |

## AIP Logic and agents

| Name | Tools it may call (functions, actions, Ontology queries) | Human review before write | Evaluation cases |
| --- | --- | --- | --- |
| `<name>` | `<tool>` | yes / no | scenario "<name>" of <capability> |

<!-- One block per new or changed logic function or agent. -->

- `<name>`
  - Input: `<type>`
  - Output: `<type>`
