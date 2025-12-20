# Session Sync Plugin

Cross-device session continuity via Obsidian timeline. Aggressive accountability logging.

## Features

- **Inbox**: Async capture from any device (phone, tablet, Obsidian mobile)
- **Work Log**: Real-time one-liners as things happen
- **MCP + Fallback**: Uses Obsidian MCP if available, falls back to filesystem

## Installation

```bash
/plugin install session-sync@cameronsjo
```

## Configuration

### Required Environment Variable

Set `CLAUDE_TIMELINE_PATH` to your timeline file location:

```bash
# In your shell profile (.zshrc, .bashrc, etc.)
export CLAUDE_TIMELINE_PATH="~/Documents/The Compendium/Claude Code Timeline.md"
```

Or in `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_TIMELINE_PATH": "~/Documents/The Compendium/Claude Code Timeline.md"
  }
}
```

## Commands

| Command | Description |
|---------|-------------|
| `/session.init` | Create a new timeline file |
| `/session.sync` | Add end-of-session summary |
| `/session.log <type> <message>` | Quick work log entry |

### Log Types

```bash
/session.log decision Using Redis - better pub/sub
/session.log commit feat: add auth (abc123)
/session.log blocker OAuth not redirecting
/session.log resolved OAuth needed callback URL
/session.log idea Could use webhooks
/session.log state Prometheus on :9090
```

## Timeline Structure

```markdown
# Claude Code Timeline

## Inbox

> Async capture from any device. Claude reviews at session start.

## Work Log

### 2025-12-19

- 23:15 **Decision**: Using Traefik - better Docker integration
- 23:30 **Commit**: feat: add prometheus (abc123)
```

## Philosophy

**Log early, log often.** The Work Log is just timestamped one-liners. Don't overthink it.
