# Session Summary: Release Pipeline Plugin Development

**Date:** 2026-01-31
**Purpose:** Create skills/commands for three-stage release pipeline automation

---

## What We Built

### 1. `/setup-release-pipeline` Command

**Location:** `release-pipelines/commands/setup-release-pipeline.md`

A Claude Code command that generates GitHub Actions workflows for any Node/TypeScript project:

| Workflow | Trigger | Creates |
|----------|---------|---------|
| `ci.yml` | Push/PR to main | Lint, type-check, test, build |
| `beta-release.yml` | `[beta]` in commit | `X.Y.Z-beta.N+sha` prerelease |
| `rc-release.yml` | `[rc]` in commit | `X.Y.Z-rc.N` prerelease, cleans betas |
| `release-please.yml` | Merge release PR | Stable `X.Y.Z`, cleans all prereleases |

**Usage:**
```bash
cd my-node-project
/setup-release-pipeline
```

### 2. Preserved `obsidian-dev` Plugin

**Location:** `obsidian-dev/`

Rescued from `~/.claude/plugins/cache/cameronsjo/obsidian-dev/1.0.0/` before potential cache wipe.

**Contents:**
- `/obsidian.init` - Scaffold new Obsidian plugin with full tooling
- `/obsidian.release` - Trigger beta/RC/stable releases for Obsidian plugins
- `obsidian-plugin-expert` agent - TypeScript patterns, Obsidian API, esbuild, BRAT

---

## Design Decisions

### Separation of Concerns

| Plugin | Scope | Why Separate |
|--------|-------|--------------|
| `release-pipelines` | Generic Node/TS projects | Framework-agnostic, no manifest.json/versions.json |
| `obsidian-dev` | Obsidian plugins specifically | Knows about manifest.json, versions.json, BRAT, esbuild for Obsidian |

### Three-Stage Release Flow

```
Developer commits with [beta] keyword
         ↓
Beta prerelease created (X.Y.Z-beta.N+sha)
         ↓ (repeat as needed)
Developer commits with [rc] keyword
         ↓
RC created, all betas deleted (X.Y.Z-rc.N)
         ↓ (fix issues, create more RCs if needed)
Merge release-please PR
         ↓
Stable release, all prereleases cleaned up (X.Y.Z)
```

### Version Calculation

- **Beta:** Counts commits since last stable tag, appends short SHA
- **RC:** Counts existing RCs for this version, increments
- **Stable:** Uses release-please's conventional commit analysis

---

## Source Material

Templates extracted from `saved-reddit-exporter` Obsidian plugin:
- `.github/workflows/beta-release.yml`
- `.github/workflows/rc-release.yml`
- `.github/workflows/release-please.yml`
- `.github/workflows/ci.yml`
- `release-please-config.json`
- `esbuild.config.mjs`

---

## Files Added This Session

```
claude-marketplace/
├── index.json                                    # Marketplace manifest
├── README.md                                     # Updated with plugin docs
├── release-pipelines/
│   ├── .claude-plugin/plugin.json
│   ├── README.md
│   └── commands/setup-release-pipeline.md        # The main command
├── obsidian-dev/
│   ├── .claude-plugin/plugin.json
│   ├── agents/obsidian-plugin-expert.md
│   └── commands/
│       ├── obsidian.init.md
│       └── obsidian.release.md
└── docs/
    └── 2026-01-31-release-pipeline-session-summary.md  # This file
```

---

## Related Files (in ~/.claude/)

Design documents saved to `~/.claude/docs/plans/`:
- `2026-01-31-release-pipeline-skills-design.md` - Original brainstorming design
- `2026-01-31-release-pipelines-plugin.md` - Implementation plan

---

## Cleanup Needed

These redundant items should be deleted:
- `~/Projects/claude-plugins/` - Intermediate monorepo (superseded)
- `github.com/cameronsjo/claude-plugins` - Intermediate repo (superseded)
- `github.com/cameronsjo/claude-plugin-release-pipelines` - Standalone repo (merged here)

---

## Usage After Merge

```bash
# Add marketplace
/plugin marketplace add cameronsjo/claude-marketplace

# Install plugins
/plugin install release-pipelines
/plugin install obsidian-dev

# Use commands
/setup-release-pipeline          # In any Node/TS project
/obsidian.init my-plugin         # Create new Obsidian plugin
/obsidian.release beta           # Trigger Obsidian plugin release
```
