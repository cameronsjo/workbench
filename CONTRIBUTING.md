# Contributing

Guide for adding a plugin to the workbench marketplace.

## The model

Workbench is a **registry**, not a source monorepo. It ships no plugin code of its own — its
`.claude-plugin/marketplace.json` is a list of entries, each pointing at a plugin that lives
**somewhere else**:

- A **standalone repo** — the plugin owns its own GitHub repository (`url` source).
- A **monorepo subdir** — the plugin lives under `plugins/<name>/` of a shared repo, currently
  `cameronsjo/cadence` (`git-subdir` source).

There is no `src/`, no `index.json`, and no version numbers. See
[Versioning](#versioning) below.

## Adding a plugin

### 1. Publish the plugin

The plugin lives in its own repo (or a `plugins/<name>/` subdir of a monorepo) with a
`.claude-plugin/plugin.json`. See [Plugin repo structure](#plugin-repo-structure).

### 2. Register it in `marketplace.json`

Add one entry to the `plugins` array in `.claude-plugin/marketplace.json`. Pick the source shape
that matches where the plugin lives.

**Standalone repo — `url` source:**

```json
{
  "name": "my-plugin",
  "description": "Brief description shown in /plugin discover",
  "source": {
    "source": "url",
    "url": "https://github.com/cameronsjo/my-plugin.git"
  }
}
```

**Monorepo subdir — `git-subdir` source:**

```json
{
  "name": "my-plugin",
  "description": "Brief description shown in /plugin discover",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/cameronsjo/cadence.git",
    "path": "plugins/my-plugin"
  }
}
```

### 3. Add a `README.md` row

Add the plugin to the appropriate table in `README.md` — the Cadence Ecosystem table for a
`cameronsjo/cadence` subdir, or the Standalone table for its own repo.

### 4. Open a PR

Submit against `cameronsjo/workbench`.

## Plugin repo structure

Each plugin follows:

```
repo-root/                    # or plugins/<name>/ in a monorepo
├── .claude-plugin/
│   └── plugin.json           # Required: metadata
├── commands/                 # Slash commands (.md)
│   └── my-command.md
├── agents/                   # Subagents (.md, optional)
│   └── my-agent.md
├── skills/                   # Skills with SKILL.md (optional)
│   └── my-skill/SKILL.md
├── README.md                 # Required: documentation
└── LICENSE
```

### plugin.json

```json
{
  "name": "my-plugin",
  "description": "Brief description for /plugin discover",
  "author": {
    "name": "your-github-username"
  },
  "keywords": ["relevant", "search", "terms"]
}
```

**Fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Plugin identifier (kebab-case) |
| `description` | Yes | One-line description |
| `author.name` | Yes | GitHub username or name |
| `keywords` | No | Search/discovery terms |

No `version` field — see [Versioning](#versioning).

## Command format

`commands/my-command.md`:

```yaml
---
description: Brief description shown in /help
category: workflow|code-analysis|context-loading
allowed-tools: Bash, Edit, Read, Glob, Grep
---

# Command Title

Instructions for Claude when this command is invoked.

## Steps

1. First, do this
2. Then do that

$ARGUMENTS
```

**Frontmatter fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | Shown in `/help` |
| `category` | No | Grouping for organization |
| `allowed-tools` | No | Restrict available tools |
| `disable-model-invocation` | No | Set `true` for personality commands |

**Tips:**

- End with `$ARGUMENTS` to receive user input
- Use `allowed-tools` to limit scope (security)
- Use `disable-model-invocation: true` for commands that modify Claude's behavior rather than spawning agents

## Agent format

`agents/my-agent.md`:

```yaml
---
name: my-agent
description: |
  When to use this agent.

  <example>
  user: "Help me with X"
  assistant: "I'll use my-agent to handle this."
  </example>

model: inherit
color: cyan
tools: ["Read", "Grep", "Glob", "Edit", "Write", "Bash"]
---

# Agent Instructions

What this agent does and how.

## Principles

- Key behavior 1
- Key behavior 2
```

**Frontmatter fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Agent identifier |
| `description` | Yes | When/why to invoke (with examples) |
| `model` | No | `inherit` (default), `sonnet`, `opus`, `haiku` |
| `color` | No | Terminal color for output |
| `tools` | No | Available tools (defaults to all) |

## PR checklist

- [ ] Plugin published with a valid `.claude-plugin/plugin.json` (name, description, author)
- [ ] README.md documenting commands/agents/skills
- [ ] All commands have `description` frontmatter
- [ ] All agents have `name` and `description` frontmatter
- [ ] Entry added to `marketplace.json` (`url` or `git-subdir` source)
- [ ] Row added to the `README.md` table

## Versioning

Plugins carry **no `version` field**. Workbench uses SHA-based cache invalidation — Claude Code
re-pins each installed plugin to its latest pushed commit at session start, so a version number
would be redundant bookkeeping. This is a deliberate design decision; see
`docs/adr/0001-plugin-cache-versioning.md`.

## Testing locally

For instant edit propagation on the dev machine, point the marketplace at a local checkout with a
path override in `~/.claude/setup-marketplaces.sh`. Edits to the local plugin source then take
effect without a push/re-pin cycle. Remove the override to fall back to the published source.

## Questions?

Open an issue on `cameronsjo/claude-configurations` (the ecosystem tracker) or check existing
entries in `marketplace.json` for examples.
