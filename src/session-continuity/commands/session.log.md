---
description: Log an entry to the session timeline
argument-hint: "<type> <message>"
allowed-tools: Bash, Read, Edit
---

# Log Timeline Entry

Add an entry to the session timeline.

## Arguments

- `$ARGUMENTS` - Entry type and message
  - Format: `<type> <message>`
  - Types: `decision`, `commit`, `blocker`, `resolved`, `idea`, `state`

## Workflow

1. **Parse arguments**
   - Extract type (first word)
   - Extract message (rest)

2. **Read timeline** from `$CLAUDE_TIMELINE_PATH`

3. **Find today's section**
   - Look for `### YYYY-MM-DD` matching today
   - If not found, create new date section

4. **Append entry**
   - Format: `- HH:MM **Type**: message`
   - Use current time

5. **Save timeline**

## Entry Types

| Type | Display | Use For |
|------|---------|---------|
| `decision` | **Decision** | Choices with reasoning |
| `commit` | **Commit** | Git commits (include hash) |
| `blocker` | **Blocker** | Issues blocking progress |
| `resolved` | **Resolved** | How blockers were fixed |
| `idea` | **Idea** | Insights worth preserving |
| `state` | **State** | System state changes |

## Examples

```
/session.log decision Using Redis for caching - simpler than Memcached
/session.log commit feat: add auth middleware (abc123)
/session.log blocker TypeScript can't find module types
/session.log resolved Added @types/node to devDependencies
```
