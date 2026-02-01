---
description: Initialize a new timeline file for session continuity
argument-hint: "[path]"
allowed-tools: Bash, Read, Write
---

# Initialize Timeline

Create a new timeline file for session continuity tracking.

## Arguments

- `$ARGUMENTS` - Optional path. Defaults to `$CLAUDE_TIMELINE_PATH` or prompts for location.

## Workflow

1. **Determine path**
   - Use `$ARGUMENTS` if provided
   - Fall back to `$CLAUDE_TIMELINE_PATH` env var
   - If neither, ask user for preferred location

2. **Check if exists**
   - If file exists, ask before overwriting
   - Offer to backup existing file

3. **Create timeline**

```markdown
# Claude Code Timeline

## Inbox

> Async capture from any device. Claude reviews at session start.

## Work Log

### YYYY-MM-DD

- HH:MM **State**: Timeline initialized
```

4. **Confirm**
   - Report file created
   - Remind to set `CLAUDE_TIMELINE_PATH` if not set

## Example

```
/session.init ~/Documents/Vault/claude-timeline.md
```
