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

Three primary rhythms map to three primary plugins:

| Plugin | Repo | Rhythm | Description |
|---|---|---|---|
| cadence | cameronsjo/cadence | always-on | Everyday session-agnostic methodology — four-tier router, daily rhythm, capture, dispatch, everyday tuning |
| cadence-forge | cameronsjo/cadence-forge | dev sessions | Dev workflow — debugging, testing, polish, logging, review, dependency vetting |
| cadence-groundwork | cameronsjo/cadence-groundwork | enable, run, disable | Episodic ground-breaking — scaffolding archetypes, license selection, marketplace and hooks setup, CI/CD, plugin/rules authoring |

Domain satellites and shared infrastructure:

| Plugin | Repo | Description |
|---|---|---|
| cadence-voice | cameronsjo/cadence-voice | Communication and presence — prose craft, AI pattern detection, brand, data storytelling, conflict resolution |
| cadence-mcp | cameronsjo/cadence-mcp | MCP server development patterns |
| cadence-obsidian | cameronsjo/cadence-obsidian | Obsidian plugin development and vault workflows |
| cadence-palette | cameronsjo/cadence-palette | Image generation toolkit for Gemini |
| cadence-lab | cameronsjo/cadence-lab | Experimental — macOS integrations, tmux, MCP discovery |
| cadence-rules | cameronsjo/cadence-rules | 10 languages, security, quality, git, CI/CD, Docker, MCP, documentation |
| cadence-guardrails | cameronsjo/cadence-guardrails | Push/gh write guards, branch warnings, commit nudges |

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

### Skill Path Resolution

Paths inside `skills/<name>/SKILL.md` resolve **relative to SKILL.md**, not the plugin root. To reference assets at the repo root from a skill, use `../../<dir>/`. Do NOT duplicate the assets inside `skills/<name>/references/` — that drifts the moment the source updates.

**Gotcha**: a skill that ships `references/src/...` as its own copy of repo-level `src/` is the wrong layer. Reference up, don't duplicate down. Verify before commit: `grep -nE 'references/(src|live-spec|...)/' skills/<name>/SKILL.md` should return zero matches when the migration is clean.
