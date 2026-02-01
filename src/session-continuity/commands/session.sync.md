---
description: Sync current session state to timeline
allowed-tools: Bash, Read, Edit
---

# Sync Session State

Capture current session context to timeline - useful before ending session or when context is getting long.

## Workflow

1. **Read timeline** from `$CLAUDE_TIMELINE_PATH`

2. **Gather session state**
   - Recent commits (last 3-5)
   - Open files / working directory
   - Current task in progress
   - Any pending decisions

3. **Check for uncommitted work**
   - Run `git status`
   - If uncommitted changes, log as state

4. **Append summary entry**

```markdown
- HH:MM **State**: Session sync
  - Working on: [current task]
  - Recent commits: [list]
  - Uncommitted: [files or "none"]
  - Next: [what to pick up]
```

5. **Review inbox**
   - Check if any inbox items were addressed
   - Remove completed items
   - Log what was done

## When to Use

- Before `/clear` or ending session
- When context is getting long
- Before switching to different task
- End of work session

## Example

```
/session.sync
```

Output:
```
Session synced to timeline:
- Working on: Adding rate limiting to API
- Recent commits: feat: add rate limiter (abc123), fix: token validation (def456)
- Uncommitted: src/middleware/rateLimit.ts
- Next: Write tests for rate limiter
```
