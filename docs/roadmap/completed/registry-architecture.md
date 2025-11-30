# Registry Architecture

> Central registry with symlinks enabling asset reuse across plugins.

## Status

- **Priority**: p0
- **Effort**: large
- **Shipped**: Initial release

## Problem

Assets (commands, agents, skills) were duplicated across plugins. Changes required updating multiple copies. No single source of truth.

## Solution

A central registry holds all assets once. Plugins contain symlinks pointing to registry assets.

```
registry/               # Source of truth
├── agents/
├── commands/
└── skills/

plugins/{name}/         # Installable packages
├── agents/    → symlinks to registry/agents/
├── commands/  → symlinks to registry/commands/
└── skills/    → symlinks to registry/skills/
```

## How It Works

1. Assets are added to `registry/{type}/` once
2. `plugin-builder.py edit add {plugin} {asset}` creates symlinks
3. Plugins can share assets without duplication
4. Updates to registry assets propagate to all plugins automatically

## Key Files

- `registry/` - All asset source files
- `plugins/` - Plugin packages with symlinks
- `scripts/plugin-builder.py` - CLI for managing assets and plugins

## Trade-offs

**Pros:**
- Single source of truth
- No duplication
- Easy asset sharing

**Cons:**
- Symlinks can be fragile on some systems
- Requires tooling to manage

## Related

- [Plugin Builder CLI](plugin-builder-cli.md)
