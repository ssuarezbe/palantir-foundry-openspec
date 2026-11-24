# Gherkin scenarios and tasks

Specs and tasks are written in Gherkin: `GIVEN` (context), `WHEN` (one trigger), `THEN` (a result someone can see), `AND` / `BUT` to continue a step, and an `**Examples**` table when the same steps run with different data. It is a plain-language format that business, QA and developers can all read.

It is written inside the normal OpenSpec Markdown, not in separate `.feature` files. OpenSpec already requires every requirement to have `#### Scenario:` blocks with a `WHEN`/`GIVEN` and a `THEN` line, so Gherkin fits with no change to the validator and no new tool.

In a spec (`openspec/changes/<name>/specs/<capability>/spec.md`):

```
### Requirement: Approve a batch release
The system SHALL let a QA approver release a batch only when all tests pass.
Ontology: ApproveBatchRelease

#### Scenario: Release blocked by a failed test
- **GIVEN** a batch with a failed test
- **WHEN** the user approves the release
- **THEN** the system rejects the approval
- **BUT** the batch status stays In Review

#### Scenario: Release by role
- **GIVEN** a user with role <role>
- **WHEN** the user approves the release of a passed batch
- **THEN** the approval is <result>

**Examples**

| role | result |
| --- | --- |
| QA approver | accepted |
| Operator | rejected |
```

In `tasks.md`, each task has one indented `Verify:` line, in Gherkin or citing a scenario. The line is not a checkbox, so progress counting is unchanged:

```
- [ ] 1.1 Add the validateRelease function
  - **Verify:** GIVEN a batch with a failed test; WHEN validateRelease runs; THEN it returns an error.
- [ ] 2.1 Show the rejection on the release page
  - **Verify:** scenario "Release blocked by a failed test" of batch-release.
```

Rules the assistant follows: one behavior per scenario, exactly one `WHEN`, business language and glossary terms (no clicks, field ids or function names), cover the main path, each stated rule and at least one failure case. There is no `Background`: put shared context in the requirement text or repeat the `GIVEN`. Keep the keywords in English, because validation looks for them. The step text can be in any language.
