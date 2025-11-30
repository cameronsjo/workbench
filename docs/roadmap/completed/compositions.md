# Compositions

> Pre-configured plugin bundles for common workflows.

## Status

- **Priority**: p2
- **Effort**: small
- **Shipped**: v1.0

## Problem

Users had to manually figure out which plugins work well together. No guidance on "I want to do X, which plugins do I need?"

## Solution

`docs/compositions.md` - Documented bundles of plugins for specific use cases.

## Example Compositions

### Core Productivity
```bash
/plugin install core-productivity
```
Includes: commit, check, clean, todo management

### Full Stack Developer
```bash
/plugin install fullstack-dev
```
Includes: TypeScript expert, frontend developer, backend architect, code reviewer

### Security Focus
```bash
/plugin install security-bundle
```
Includes: Security auditor, code reviewer with security focus

## How It Works

Compositions are documented recommendations, not a separate install mechanism. Users can:
1. Read the composition docs
2. Install plugins individually
3. Or use a meta-plugin that depends on others (future enhancement)

## Related

- [Plugin Dependency Resolution](../research.md) - Would enable true composition installs
