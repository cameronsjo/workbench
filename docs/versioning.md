# Versioning and Release Management

This document describes the versioning strategy, update flow, and release automation for the Claude Marketplace.

## Versioning Strategy

### Mono-Repo Versioning

The marketplace uses **mono-repo versioning** - a single version number for the entire marketplace rather than individual plugin versions.

**Rationale:**

- Single maintainer with unified release cadence
- Simplifies update detection (one version check vs. many)
- All assets tested together as a cohesive unit
- Files on disk ARE the manifest - no separate tracking needed

**Trade-offs:**

- All users get all updates (no selective plugin updates)
- Any change bumps the whole marketplace version
- Acceptable for personal/small-team marketplaces

### Version Location

The canonical version lives in `marketplace.json`:

```json
{
  "metadata": {
    "version": "1.2.0"
  }
}
```

Individual `plugin.json` files MAY have version fields, but they're informational only. The marketplace version is the source of truth.

## Update Flow

### How Updates Work

```
┌─────────────────────────────────────────────────────────────────┐
│                       UPDATE DETECTION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. User runs: /plugin update check                             │
│                                                                 │
│  2. For each marketplace in known_marketplaces.json:            │
│     ├── git fetch origin (in installLocation)                   │
│     ├── Read remote marketplace.json version                    │
│     └── Compare with installedVersion                           │
│                                                                 │
│  3. If remote > installed:                                      │
│     └── Show "Update available: 1.0.0 → 1.2.0"                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       UPDATE EXECUTION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. User runs: /plugin update                                   │
│                                                                 │
│  2. For each marketplace with updates:                          │
│     ├── git pull origin main                                    │
│     ├── Re-copy all assets to ~/.claude/{commands,agents,skills}│
│     ├── Update installedVersion in known_marketplaces.json      │
│     └── Update lastUpdated timestamp                            │
│                                                                 │
│  3. Report: "Updated cameronsjo: 1.0.0 → 1.2.0"                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### known_marketplaces.json Schema

```json
{
  "cameronsjo": {
    "source": {
      "source": "github",
      "repo": "cameronsjo/claude-marketplace"
    },
    "installLocation": "~/.claude/plugins/marketplaces/cameronsjo",
    "installedVersion": "1.0.0",
    "lastUpdated": "2025-11-30T19:58:22.752Z"
  }
}
```

Key fields:

- `installedVersion` - The marketplace version when last installed/updated
- `lastUpdated` - Timestamp of last sync operation

## Release Automation

### Release Please

The marketplace uses [Release Please](https://github.com/googleapis/release-please) for automated versioning and changelog generation.

**How it works:**

1. Developers use conventional commits (`feat:`, `fix:`, `docs:`, etc.)
2. Release Please maintains a release PR that tracks unreleased changes
3. When merged, it:
   - Bumps version in `marketplace.json`
   - Generates/updates `CHANGELOG.md`
   - Creates a GitHub Release with tag

### Conventional Commits

| Prefix | Version Bump | Description |
|--------|-------------|-------------|
| `feat:` | MINOR | New feature (1.0.0 → 1.1.0) |
| `fix:` | PATCH | Bug fix (1.0.0 → 1.0.1) |
| `feat!:` or `BREAKING CHANGE:` | MAJOR | Breaking change (1.0.0 → 2.0.0) |
| `docs:` | PATCH | Documentation only |
| `chore:` | PATCH | Maintenance tasks |
| `refactor:` | PATCH | Code restructuring |

### Examples

```bash
# Adding a new command (MINOR bump)
git commit -m "feat(commands): add /deploy command for cloud deployments"

# Fixing a bug in an agent (PATCH bump)
git commit -m "fix(agents): correct python-expert type hint guidance"

# Breaking change (MAJOR bump)
git commit -m "feat!: restructure plugin directory layout

BREAKING CHANGE: Plugins now use flat structure instead of nested"
```

## Beta Channel

### Prerelease Versions

Beta versions use prerelease tags:

```
v1.3.0-beta.1
v1.3.0-beta.2
v1.3.0           # stable release
```

### Opting Into Beta

Users can opt into beta by specifying a branch or tag:

```bash
/plugin marketplace add cameronsjo/claude-marketplace@beta
```

Or manually editing `known_marketplaces.json`:

```json
{
  "cameronsjo": {
    "source": {
      "source": "github",
      "repo": "cameronsjo/claude-marketplace",
      "ref": "beta"
    }
  }
}
```

### Beta Workflow

1. Create `beta` branch from `main`
2. Merge experimental changes to `beta`
3. Release Please creates prerelease versions
4. When stable, merge `beta` → `main`
5. Stable release cuts automatically

## GitHub Actions Workflow

### .github/workflows/release.yml

The workflow handles:

1. **On push to main**: Release Please analyzes commits and updates release PR
2. **On release PR merge**: Creates GitHub Release with version tag
3. **Validates**: Ensures `marketplace.json` version matches release

### Manual Releases

For urgent fixes outside the normal flow:

```bash
# Tag manually (use sparingly)
git tag v1.2.1
git push origin v1.2.1
```

## Migration Notes

### From Pre-Versioning State

Existing installations without `installedVersion`:

1. On first update check, assume installed version is `0.0.0`
2. Any marketplace version > `0.0.0` triggers update prompt
3. After update, `installedVersion` is written correctly

### Individual Plugin Versions

Individual `plugin.json` version fields are deprecated for update detection. They remain for informational purposes only (e.g., showing in `/plugin list`).

## FAQ

**Q: Why not version each plugin separately?**
A: Complexity vs. benefit. For a single-maintainer marketplace, mono-repo versioning is simpler and sufficient. Multi-maintainer marketplaces might reconsider.

**Q: What if I only want updates for one plugin?**
A: Currently not supported. Updates are all-or-nothing per marketplace. Consider splitting into separate marketplaces if granular control is needed.

**Q: How do I roll back a bad update?**
A: Check out a previous tag in the marketplace repo:
```bash
cd ~/.claude/plugins/marketplaces/cameronsjo
git checkout v1.1.0
# Re-run plugin install
```

**Q: Can I pin to a specific version?**
A: Yes, set `ref` in the source config to a tag (e.g., `v1.2.0`).
