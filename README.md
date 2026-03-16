# Workbench

Hub registry for personal Claude Code plugins.

## Installation

```bash
# Register the marketplace
/plugin marketplace add cameronsjo/workbench

# Install what you need
/plugin install cadence@cameronsjo
/plugin install rules@cameronsjo
```

Or use the automated setup in `~/.claude/setup-marketplaces.sh`.

## Plugins

### Cadence Ecosystem

| Plugin | Description |
|---|---|
| cadence | Context management framework — four-tier workflow router, daily rhythm, session capture |
| cadence-forge | Development workflow — logging, dependency vetting, release pipelines, diagrams |
| cadence-mcp | MCP server development patterns |
| cadence-obsidian | Obsidian plugin development and vault workflows |
| cadence-palette | Image generation toolkit for Gemini |
| cadence-lab | Experimental — macOS integrations, tmux, MCP discovery |

### Standalone

| Plugin | Description |
|---|---|
| rules | 10 languages, security, quality, git, CI/CD, Docker, MCP, documentation |
| git-guardrails | Push/gh write guards, branch warnings, commit nudges |
| pencil | Design workflow for Pencil.dev — canvas design, .pen files |

## Architecture

Each plugin lives in its own GitHub repo. This registry's `marketplace.json` references them via URL sources. On the dev machine, local path overrides in `setup-marketplaces.sh` provide instant edit propagation.

## License

MIT
