# Plugin Builder CLI

> Dashboard, validation, and asset management for the marketplace.

## Status

- **Priority**: p1
- **Effort**: medium
- **Shipped**: v1.0

## Problem

Managing the registry and plugins manually was error-prone. Needed tooling to:
- See what assets exist
- Track which plugins use which assets
- Validate symlinks aren't broken
- Find orphaned assets

## Solution

`scripts/plugin-builder.py` - A CLI for marketplace management.

## Usage

```bash
# Dashboard with stats and health
python scripts/plugin-builder.py dashboard

# List all assets in registry
python scripts/plugin-builder.py list

# Show which plugins use each asset
python scripts/plugin-builder.py usage

# Find orphaned (unused) assets
python scripts/plugin-builder.py orphans

# Add asset to a plugin (creates symlink)
python scripts/plugin-builder.py edit add {plugin} {asset} -t {type}

# Validate all symlinks
python scripts/plugin-builder.py validate

# Interactive mode
python scripts/plugin-builder.py
```

## Key Features

- **Dashboard**: Quick health check of the marketplace
- **Validation**: Ensures symlinks point to real files
- **Usage tracking**: See asset adoption across plugins
- **Orphan detection**: Find assets not used by any plugin

## Related

- [Registry Architecture](registry-architecture.md)
