# Versioning System

**Status:** Completed
**Priority:** P1
**Effort:** Large

## Summary

Implemented mono-repo versioning with Release Please automation for the Claude Marketplace.

## Implementation

### Design Decisions

1. **Mono-repo versioning** - Single version for entire marketplace rather than per-plugin
   - Simpler update detection (one check vs many)
   - All assets tested together as cohesive unit
   - Acceptable trade-off for single-maintainer marketplace

2. **No known_plugins.json** - Track only marketplace version in `known_marketplaces.json`
   - Files on disk ARE the manifest
   - `installedVersion` field added to track what's installed

3. **Release Please automation** - Conventional commits drive version bumps
   - `feat:` → MINOR bump
   - `fix:` → PATCH bump
   - `feat!:` or `BREAKING CHANGE:` → MAJOR bump

4. **Beta channel** - Via prerelease tags (`v1.3.0-beta.1`)

### Files Created

- `docs/versioning.md` - Full documentation of SDLC and update flow
- `.github/workflows/release.yml` - Release Please workflow
- `release-please-config.json` - Configuration with extra-files for marketplace.json
- `.release-please-manifest.json` - Version manifest starting at 1.0.0

### How It Works

1. Developer makes changes using conventional commits
2. Release Please maintains a release PR with changelog
3. When PR is merged:
   - Version bumped in `marketplace.json`
   - CHANGELOG.md updated
   - GitHub Release created with tag
4. Users can check for updates and pull new version
