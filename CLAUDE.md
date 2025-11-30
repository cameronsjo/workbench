# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code plugin marketplace - a collection of agents, commands, and skills that extend Claude Code's capabilities. Plugins are distributed via GitHub and installed using `/plugin` commands.

## Architecture

### Registry-Based Plugin System

The marketplace uses a central registry with symlinks to populate plugins:

```
registry/               # Source of truth for all assets
├── agents/            # Agent prompts (.md files)
├── commands/          # Slash command prompts (.md files)
└── skills/            # Skill directories (SKILL.md + resources/)

plugins/               # Installable plugin packages
├── {plugin-name}/
│   ├── .claude-plugin/plugin.json  # Plugin metadata
│   ├── agents/        # Symlinks → registry/agents/
│   ├── commands/      # Symlinks → registry/commands/
│   └── skills/        # Symlinks → registry/skills/
```

Assets are added to the registry once, then symlinked into multiple plugins. This enables asset reuse across plugins while maintaining a single source of truth.

### Plugin Builder CLI

`scripts/plugin-builder.py` manages the marketplace:

```bash
# Show dashboard with stats and health
python scripts/plugin-builder.py dashboard

# List all assets in registry
python scripts/plugin-builder.py list

# Show which plugins use each asset
python scripts/plugin-builder.py usage

# Find orphaned (unused) assets
python scripts/plugin-builder.py orphans

# Add asset to a plugin (creates symlink)
python scripts/plugin-builder.py edit add {plugin} {asset} -t {commands|agents|skills}

# Validate all symlinks
python scripts/plugin-builder.py validate

# Interactive mode
python scripts/plugin-builder.py
```

### Marketplace Configuration

`.claude-plugin/marketplace.json` defines available plugins:
- Plugin name, description, version
- Source path pointing to `./plugins/{name}`
- Category and keyword tags

## Asset Formats

### Commands (registry/commands/*.md)

YAML frontmatter with description, category, and allowed-tools. Body contains the prompt template.

### Agents (registry/agents/*.md)

YAML frontmatter defining the agent persona. Body contains system prompt and behavioral guidelines.

### Skills (registry/skills/{name}/)

Directory structure:
- `SKILL.md` - Main skill definition with frontmatter
- `README.md` - Optional documentation
- `resources/` - Additional reference files

## Development Workflow

When adding new assets:
1. Create the asset in `registry/{type}/`
2. Use plugin-builder to add it to plugins: `python scripts/plugin-builder.py edit add {plugin} {asset} -t {type}`
3. Validate symlinks: `python scripts/plugin-builder.py validate`

When creating a new plugin:
1. `python scripts/plugin-builder.py create {name} -d "description"`
2. Add assets using `edit add` commands
3. Add entry to `.claude-plugin/marketplace.json`

## Key Files

- `.claude-plugin/marketplace.json` - Plugin registry for Claude Code
- `scripts/plugin-builder.py` - CLI for managing assets and plugins
- `docs/compositions.md` - Pre-configured plugin bundles for common workflows
