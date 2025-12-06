# ADR 0001: Flat File Architecture (No Symlinks or Central Registry)

- **Status:** Accepted
- **Date:** 2025-12-06
- **Decision Makers:** Cameron

## Context

The marketplace originally used a central `registry/` directory as the source of truth for all assets (agents, commands, skills). Plugins contained symlinks pointing back to the registry, enabling DRY maintenance - edit once in registry, all plugins get the update.

```
registry/                  # Source of truth
├── agents/foo.md
├── commands/bar.md
└── skills/baz/

plugins/my-plugin/
├── agents/foo.md -> ../../registry/agents/foo.md  # Symlink
└── commands/bar.md -> ../../registry/commands/bar.md
```

## Problem

**Claude Code does not follow symlinks when scanning for commands, agents, and skills.**

When users installed plugins via `/plugin install`, the symlinks were preserved but Claude Code couldn't resolve them. Commands wouldn't appear, agents wouldn't load, skills weren't available.

Additionally, when Claude Code clones plugins from GitHub via `git clone`, symlinks are preserved but point to non-existent paths (the registry doesn't exist in the cloned plugin directory).

## Decision

**Remove the central registry. Each plugin contains real files (copies, not symlinks).**

```
plugins/my-plugin/
├── agents/foo.md      # Real file
├── commands/bar.md    # Real file
└── skills/baz/        # Real directory
```

## Consequences

### Positive

- Plugins work correctly with Claude Code's scanning
- Git clones are self-contained and functional
- Simpler mental model - what you see is what you get
- No symlink-related cross-platform issues

### Negative

- **Duplication**: Assets shared across plugins are duplicated
- **Sync burden**: Updating a shared asset requires updating each plugin copy
- **Drift risk**: Plugin copies can diverge if not kept in sync

### Mitigation

1. **Document shared assets** - Track which plugins use which assets
2. **Use plugin-builder CLI** - `python scripts/plugin-builder.py usage` shows asset usage across plugins
3. **Accept some duplication** - For a marketplace this size, duplication is manageable
4. **Review on updates** - When updating an asset, check if other plugins need the same update

## Alternatives Considered

### Keep Registry with Manual Sync

Keep registry as source of truth, use plugin-builder to copy files to plugins on changes.

**Rejected because:** Still requires discipline to sync, adds tooling complexity, and the registry becomes dead weight that could mislead contributors.

### Hardlinks Instead of Symlinks

Use hardlinks which share the same inode.

**Rejected because:** Hardlinks don't work across filesystems, behave inconsistently on clone, and most tools treat them as regular files anyway.

### Git Submodules for Shared Assets

Use a separate repo for shared assets, include as submodule.

**Rejected because:** Adds significant complexity for minimal benefit at this scale.

## References

- Claude Code plugin documentation
- [GitHub issue or discussion if applicable]
