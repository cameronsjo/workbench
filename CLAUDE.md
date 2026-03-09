# Workbench

Hub registry for personal Claude Code plugins.

## Structure

```
├── marketplace.json        # Plugin registry (all plugins via URL sources)
├── README.md               # Plugin directory with install instructions
└── docs/                   # Historical design docs
```

## Plugins

### Cadence Ecosystem

| Plugin | Repo | Description |
|---|---|---|
| cadence | cameronsjo/cadence | Context management framework — four-tier workflow router, daily rhythm, session capture |
| cadence-forge | cameronsjo/cadence-forge | Development workflow — logging, dependency vetting, release pipelines, diagrams |
| cadence-mcp | cameronsjo/cadence-mcp | MCP server development patterns |
| cadence-obsidian | cameronsjo/cadence-obsidian | Obsidian plugin development and vault workflows |
| cadence-palette | cameronsjo/cadence-palette | Image generation toolkit for Gemini |
| cadence-lab | cameronsjo/cadence-lab | Experimental — macOS integrations, tmux, MCP discovery |

### Standalone

| Plugin | Repo | Description |
|---|---|---|
| rules | cameronsjo/rules | 10 languages, security, quality, git, CI/CD, Docker, MCP, documentation |
| git-guardrails | cameronsjo/git-guardrails | Push/gh write guards, branch warnings, commit nudges |
| pencil | cameronsjo/pencil | Design workflow for Pencil.dev — canvas design, .pen files |

## Plugin Repo Structure

Each plugin repo follows:

```
repo-root/
├── .claude-plugin/
│   ├── marketplace.json    # Declares repo as a standalone marketplace
│   └── plugin.json         # Plugin metadata
├── commands/               # Slash commands (.md)
├── agents/                 # Subagents (.md)
├── skills/                 # Skills with SKILL.md
├── README.md
├── LICENSE
└── .gitignore
```
