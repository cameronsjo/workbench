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
| cadence | Context management framework — four-tier router, daily rhythm, capture, dispatch | always-on |
| cadence-forge | Dev workflow — logging, dependency vetting, release pipelines, diagrams, checks | dev sessions |
| cadence-groundwork | Episodic ground-breaking — scaffolding, licenses, marketplace/hooks/CI setup, authoring | enable, run, disable |
| cadence-voice | Communication and presence — prose craft, AI pattern detection, brand, conflict resolution | episodic |
| cadence-mcp | MCP server development — architecture patterns, tools-as-code | episodic |
| cadence-obsidian | Obsidian plugin development and vault workflows | episodic |
| cadence-palette | Image generation toolkit — Gemini prompt engineering, composition specs | episodic |
| cadence-discovery | Feature ideation pipeline — usage-grounded discovery producing one attune-ready feature | episodic |
| cadence-metrics | JSONL event logging — cost-per-commit via Pre/PostToolUse hooks | always-on |
| cadence-rules | Language standards, security, quality, git, CI/CD, Docker, MCP, documentation | always-on |
| cadence-guardrails | Push/gh write guards, branch warnings, commit nudges | always-on |
| cadence-dev | Skills for building cadence itself — placement, skill-edit drills, model-tagged deferral | build repos (opt-in) |
| go | Terse one-shot slash commands for recurring instructions Cameron says once per turn | always-on |

### Mods

A mod runs its own code inside every Claude Code session, so each one is pinned to the exact commit that was reviewed. The `pins` check (`scripts/check-pins.py`) fails a change that leaves one unpinned.

| Plugin | Description |
|---|---|
| afk | `/afk` wraps up a session before you walk away and compacts it; optional idle trigger; session tools for Claude |
| board | Agent Board tools for Claude and an unread count |
| guard-toast | A toast and a Feedback button when a cadence-hooks guard refuses a tool call |
| herdr-bridge | herdr pane tools for Claude |
| sploot | A pixel-art corgi in a little yard above the prompt |
| verbs | Spinner words that say what is running |

### Standalone

| Plugin | Description |
|---|---|
| homelab | Homelab infrastructure context — Unraid server, media stack, Docker services |
| artificer-design-system | Artificer design system — tokens, live spec, framework adapters, themes for Claude Code/Ghostty/VSCode/Obsidian |
| artificer-voice | Portable communication preferences injected at SessionStart and SubagentStart (private repo) |
| bosun | GitOps CLI for Docker Compose on bare metal — Helm for home |
| llm-council | Multi-LLM deliberation web app with Council and Arena debate modes |
| media-mcp | MCP server enriching Obsidian vaults with book, movie, and TV metadata |
| mouse-mcp | Disney parks data MCP server — attraction wait times, dining info, fuzzy search |
| obaass | Headless Obsidian orchestrator — obsidi-headless, obsidi-backup, and obsidi-mcp via Docker Compose |
| obsidi-backup | Vault backup sidecar — file watching, AI commit messages, restic cloud storage |
| obsidi-claude | Obsidian plugin for chatting with Claude AI using the Anthropic Agent SDK |
| obsidi-mcp | Obsidian plugin exposing 28+ vault tools via MCP server with CLI bridge |

## Architecture

This repo is a **registry**, not a source monorepo — `marketplace.json` points at plugins that live
elsewhere, via two source models:

- The 13 cadence-ecosystem plugins live in the **`cameronsjo/cadence` monorepo** under
  `plugins/<name>/`, referenced with `git-subdir` sources.
- Standalone plugins each live in their own GitHub repo, referenced with `url` sources.

No plugin carries a `version` field — the marketplace uses SHA-based cache invalidation, so each
pushed commit re-pins at session start (see `docs/adr/0001-plugin-cache-versioning.md`). On the dev
machine, local path overrides in `setup-marketplaces.sh` provide instant edit propagation.

## License

MIT
