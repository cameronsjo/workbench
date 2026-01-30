# Claude Code Marketplace

Three plugins. That's it.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Plugins

| Plugin | What It Is | Lines of Code |
|--------|-----------|---------------|
| **core** | Workflow modes (`/turbo`, `/roast`) + tool wrappers (`/ready`) | ~1500 |
| **essentials** | User memory MCP server - persists context across sessions | ~800 TypeScript |
| **research** | Conversation search - indexes and searches past Claude sessions | ~1200 TypeScript |

## Install

```bash
/plugin marketplace add cameronsjo/claude-marketplace
/plugin install core@cameronsjo
/plugin install essentials@cameronsjo
```

## Philosophy

See [ADR-0002](docs/adr/0002-lean-marketplace-philosophy.md).

**TL;DR:** This marketplace only contains things with actual running code or unique UX value.

### What's NOT here

| Category | Use Instead |
|----------|-------------|
| "Be a Python expert" | Built-in `python-expert` agent |
| "Be a security expert" | Built-in `security-auditor` agent |
| OWASP/secret scanning | gitleaks, semgrep, trivy |
| OpenAPI validation | spectral, openapi-generator |
| Feature flags | Your own tooling |

If it's a prompt that tells Claude to be good at something, use a built-in agent or put it in your dotfiles.

## Commands (core plugin)

| Command | What It Does |
|---------|-------------|
| `/turbo` | Maximum speed mode - parallelize everything |
| `/roast` | Maximum scrutiny mode - thorough analysis |
| `/hype` | Encouragement mode |
| `/sass` | Personality mode |
| `/ready` | Commit, push, create PR (wraps `claude-ready` CLI) |
| `/check` | Run project checks |
| `/clean` | Fix linting/formatting |
| `/catchup` | Read uncommitted changes after `/clear` |
| `/context-prime` | Load project context |

## Tools (essentials + research plugins)

### User Memory MCP

Persists user preferences and context across Claude Code sessions.

```bash
/plugin install essentials@cameronsjo
# Configure MCP server in settings
```

### Conversation Search

Indexes past Claude sessions for semantic search.

```bash
/plugin install research@cameronsjo
cd ~/.claude/plugins/cache/.../research
npm install && npm run build
```

## License

MIT
