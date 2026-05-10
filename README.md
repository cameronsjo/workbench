# Workbench

Hub registry for personal Claude Code plugins.

## Installation

```bash
# Register the marketplace
/plugin marketplace add cameronsjo/workbench

# Install what you need
/plugin install cadence@cameronsjo
/plugin install cadence-rules@cameronsjo
```

Or use the automated setup in `~/.claude/setup-marketplaces.sh`.

## Plugins

### Cadence Ecosystem

| Plugin | Description | Rhythm |
|---|---|---|
| cadence | Everyday session-agnostic methodology — four-tier router, daily rhythm, capture, dispatch, everyday tuning | always-on |
| cadence-forge | Dev workflow during a session — debugging, testing, polish, logging, review, dependency vetting | dev sessions |
| cadence-groundwork | Episodic ground-breaking — scaffolding archetypes, license selection, marketplace and hooks setup, CI/CD pipeline setup, plugin and rules authoring | enable, run, disable |
| cadence-voice | Communication and presence — prose craft, AI pattern detection, personal brand, data storytelling, conflict resolution | episodic |
| cadence-mcp | MCP server development patterns | episodic |
| cadence-obsidian | Obsidian plugin development and vault workflows | episodic |
| cadence-palette | Image generation toolkit for Gemini | episodic |
| cadence-lab | Experimental — macOS integrations, tmux, MCP discovery | as needed |
| cadence-rules | 10 languages, security, quality, git, CI/CD, Docker, MCP, documentation | always-on |
| cadence-guardrails | Push/gh write guards, branch warnings, commit nudges | always-on |

### Standalone

| Plugin | Description |
|---|---|
| agent-pool | Expert pool — mixture-of-experts routing with filesystem mail and contracts |
| artificer-design-system | Artificer design system — tokens, live spec, framework adapters, themes for Claude Code/Ghostty/VSCode/Obsidian |

## Architecture

Each plugin lives in its own GitHub repo. This registry's `marketplace.json` references them via URL sources. On the dev machine, local path overrides in `setup-marketplaces.sh` provide instant edit propagation.

## License

MIT
