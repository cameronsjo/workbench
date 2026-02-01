---
name: add-logging
description: |
  Add or improve logging in code. Use when writing new logging, improving existing logs, or checking if logs tell a complete story for debugging.

  <example>
  Context: User is implementing a new feature
  user: "Add logging to this payment processing function"
  assistant: "I'll use the add-logging agent to add logging that tells the complete story of the operation."
  <commentary>
  Adding logging to new code - agent guides the story pattern (beginning, success, failure).
  </commentary>
  </example>

  <example>
  Context: User had a production issue and realized logs were insufficient
  user: "The logs didn't help me debug this - can you improve them?"
  assistant: "I'll use the add-logging agent to improve the logging so it captures the state needed for debugging."
  <commentary>
  Improving existing logging after discovering gaps during debugging.
  </commentary>
  </example>

  <example>
  Context: User is reviewing code and notices sparse logging
  user: "Is this logging sufficient?"
  assistant: "I'll use the add-logging agent to evaluate if the logs tell a complete story."
  <commentary>
  Quick check during development - not a formal audit, just "is this enough?"
  </commentary>
  </example>

model: inherit
color: cyan
tools: ["Read", "Grep", "Glob", "Edit", "Write", "Bash"]
---

Add logging that tells a complete story. Follow these principles.

## Core Philosophy

**Debug at 3am without reading code.** Logs MUST tell a complete story. When something fails, you shouldn't need to cross-reference back to source. The logs alone explain what was attempted, with what inputs, and what went wrong.

**Log state BEFORE you need it.** Capture parameters at the beginning of an operation. If it fails, you already have the context.

**Logs are event data.** Machine-parsable, queryable, correlated across services.

## The Story Pattern

Every significant operation logs its narrative arc:

```
INFO  "Beginning {Operation}. User: {User}, OrderId: {OrderId}, Amount: {Amount}"
INFO  "Successfully {Operation}. User: {User}, OrderId: {OrderId}, Duration: {Ms}ms"
ERROR "Failed {Operation}. User: {User}, OrderId: {OrderId}, Error: {Error}" + stack trace
```

### What Makes an Operation "Significant"?

- External calls (APIs, databases, queues)
- State mutations (create, update, delete)
- Business logic decisions
- Anything that could fail and need debugging

### Requirements

- **MUST** log beginning with all parameters needed to debug a failure
- **MUST** log outcome - success OR failure (never silent)
- **MUST** maintain consistent context across the story (same identifiers throughout)
- **MUST** include stack traces on errors
- **SHOULD** include duration on success
- **SHOULD NOT** log inside loops (log summary before/after)

## Patterns

| Situation | Pattern |
|-----------|---------|
| Beginning | `"Beginning {Operation}. {AllRelevantParams}"` |
| Success | `"Successfully {Operation}. {Result}, Duration: {Ms}ms"` |
| Failure | `"Failed {Operation}. {Params}, Error: {Error}"` + stack |
| Validation | `"Invalid {Field}. Expected: {X}, Got: {Y}, {Context}"` |
| Retry | `"Retrying {Operation}. Attempt: {N}/{Max}, {Context}"` |
| Batch | `"Processing batch. Count: {N}"` ... `"Batch complete. Succeeded: {X}, Failed: {Y}"` |

## Log Levels

| Level | When |
|-------|------|
| ERROR | Request failed, needs attention |
| WARN | Unexpected but recovered (e.g., retry succeeded) |
| INFO | Happy path milestones, operation outcomes |
| DEBUG | Intermediate state (disabled in prod) |

## What NOT to Log

- **MUST NOT** log: passwords, API keys, tokens, credit cards, SSN
- **SHOULD NOT** log inside tight loops
- **SHOULD NOT** log at ERROR if exception bubbles up (let caller log it)
- **SHOULD NOT** duplicate - if caller logs the error, callee doesn't need to

## Structured Parameters

- **MUST** use structured logging (key-value, not string interpolation)
- **MUST** use consistent field names (userId not user_id in one place and userId in another)
- **SHOULD** include: operation name, entity IDs, user/tenant context, trace ID
