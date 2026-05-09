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
| cadence-bootstrap | cameronsjo/cadence-bootstrap | Bootstrap-only skills — init, marketplace setup, license selection, onboarding, tidying. Enable briefly during setup |
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

### Skill Path Resolution

Paths inside `skills/<name>/SKILL.md` resolve **relative to SKILL.md**, not the plugin root. To reference assets at the repo root from a skill, use `../../<dir>/`. Do NOT duplicate the assets inside `skills/<name>/references/` — that drifts the moment the source updates.

**Gotcha**: a skill that ships `references/src/...` as its own copy of repo-level `src/` is the wrong layer. Reference up, don't duplicate down. Verify before commit: `grep -nE 'references/(src|live-spec|...)/' skills/<name>/SKILL.md` should return zero matches when the migration is clean.
