# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code plugin marketplace - a collection of agents, commands, and skills that extend Claude Code's capabilities. Plugins are distributed via GitHub and installed using `/plugin` commands.

## Architecture

### Flat File Structure

Plugins contain real files (not symlinks) because Claude Code doesn't follow symlinks when scanning. Each plugin is self-contained.

```
plugins/
├── {plugin-name}/
│   ├── .claude-plugin/plugin.json  # Plugin metadata
│   ├── agents/                     # Agent prompts (.md files)
│   ├── commands/                   # Slash command prompts (.md files)
│   └── skills/                     # Skill directories (SKILL.md + resources/)
```

> **Why no central registry?** See [ADR 0001: Flat File Architecture](docs/adr/0001-flat-file-architecture.md) for the decision record. TL;DR: Claude Code doesn't follow symlinks, so we use real files with accepted duplication.

### Duplication is Intentional

Some assets appear in multiple plugins. This is by design - it keeps plugins self-contained and avoids symlink issues. When updating a shared asset, check if other plugins need the same update.

### Marketplace Configuration

`.claude-plugin/marketplace.json` defines available plugins:

- Plugin name, description, version
- Source path pointing to `./plugins/{name}`
- Keywords for discovery

## Asset Formats

### Commands (`commands/*.md`)

YAML frontmatter with description and allowed-tools. Body contains the prompt template.

```yaml
---
description: Brief description of what the command does
argument-hint: "[optional-args]"
allowed-tools: Bash, Read, Write, Edit
disable-model-invocation: true  # Optional: keeps out of context
---
```

### Agents (`agents/*.md`)

YAML frontmatter defining the agent persona. Body contains system prompt and behavioral guidelines.

### Skills (`skills/{name}/`)

Directory structure:

- `SKILL.md` - Main skill definition with YAML frontmatter (`name`, `description`)
- `README.md` - Optional documentation
- `resources/` - Additional reference files

## Development Workflow

### Adding a New Asset

1. Create the asset directly in the plugin's directory
2. If the asset should be shared, copy it to other relevant plugins

### Creating a New Plugin

1. Create directory: `plugins/{name}/`
2. Add `.claude-plugin/plugin.json` with metadata
3. Add agents, commands, and/or skills
4. Add entry to `.claude-plugin/marketplace.json`

### Updating Shared Assets

1. Edit the asset in one plugin
2. Copy the updated file to other plugins that use it
3. Use `grep` or search to find other copies if unsure

## Versioning

Auto-versioning on push to main via conventional commits:

| Commit Prefix | Bump | Example |
|--------------|------|---------|
| `feat!:` or `BREAKING CHANGE` | MAJOR | 1.0.0 -> 2.0.0 |
| `feat:` | MINOR | 1.0.0 -> 1.1.0 |
| `fix:` | PATCH | 1.0.0 -> 1.0.1 |
| `chore:`, `docs:`, `refactor:` | none | no release |

The workflow updates `marketplace.json`, creates a git tag, and publishes a GitHub release.

## Key Files

- `.claude-plugin/marketplace.json` - Plugin registry for Claude Code
- `.github/workflows/release.yml` - Auto-versioning workflow
- `docs/adr/` - Architecture decision records
- `docs/compositions.md` - Pre-configured plugin bundles for common workflows
