# Session Continuity

Maintain context across Claude Code sessions using timeline logging and async inbox capture.

## Problem

Claude Code sessions are ephemeral. Context compacts, sessions crash, users forget. Without aggressive logging, work history is lost.

## Solution

A timeline file (Obsidian-compatible) that captures decisions, commits, blockers, and ideas in real-time. Plus an inbox for async capture from any device.

## Installation

```bash
/plugin install session-continuity@cameronsjo
```

## Setup

Set environment variable pointing to your timeline file:

```bash
export CLAUDE_TIMELINE_PATH="$HOME/Documents/Vault/claude-timeline.md"
```

Or in `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_TIMELINE_PATH": "/path/to/vault/claude-timeline.md"
  }
}
```

## Commands

| Command | Description |
|---------|-------------|
| `/session.init` | Create timeline file with proper structure |
| `/session.log` | Log an entry to the timeline |
| `/session.sync` | Sync current session state to timeline |

## Skills

### session-continuity

Core skill that triggers on significant actions. Logs decisions, commits, blockers automatically.

**Triggers:**
- Made a decision → Log immediately
- Committed code → Log the commit
- Hit a blocker → Log before context lost
- Had an insight → Capture now

## Timeline Format

```markdown
# Claude Code Timeline

## Inbox

> Async capture from any device. Claude reviews at session start.

- [ ] Look into CI failure
- [ ] Add rate limiting to API

## Work Log

### 2025-12-19

- 23:15 **Decision**: Using Traefik - better Docker integration
- 23:30 **Commit**: feat: add prometheus (abc123)
- 23:45 **Blocker**: OAuth not redirecting
- 00:10 **Resolved**: OAuth needed explicit redirect_uri
```

## Workflow

### Session Start

1. Read timeline from `$CLAUDE_TIMELINE_PATH`
2. Check Inbox for async items
3. Acknowledge: "Timeline loaded. Inbox: N items."

### During Session

Log immediately after:
- Decisions (with reasoning)
- Commits (with hash)
- Blockers (before context lost)
- Resolutions (how it was fixed)
- Ideas (insights worth preserving)

### Session End

Timeline already up-to-date (logged as we went).
