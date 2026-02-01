# Release Pipelines Plugin

Three-stage release pipeline (Beta → RC → Stable) for Node/TypeScript projects using release-please and commit keywords.

## Installation

This plugin is installed locally at `~/.claude/plugins/local/release-pipelines/`.

To install from GitHub:
```bash
/plugin install cameronsjo/claude-plugin-release-pipelines
```

## Commands

### `/setup-release-pipeline`

Sets up a complete CI/CD pipeline in your Node/TypeScript project:

```bash
cd my-project
/setup-release-pipeline
```

**Generated files:**
- `.github/workflows/ci.yml` - Lint, type-check, test on push/PR
- `.github/workflows/beta-release.yml` - Triggered by `[beta]` keyword
- `.github/workflows/rc-release.yml` - Triggered by `[rc]` keyword
- `.github/workflows/release-please.yml` - Stable releases via PR merge
- `release-please-config.json` - Release-please configuration
- `.release-please-manifest.json` - Version tracking

## Release Flow

```
feat: add feature [beta]     →  1.2.0-beta.5+abc123  (prerelease)
         ↓
chore: prepare release [rc]  →  1.2.0-rc.1           (prerelease, cleans up betas)
         ↓
Merge release-please PR      →  1.2.0                (stable, cleans up RCs)
```

## Usage

### Beta Release (for testing)

```bash
git commit -m "feat: add new feature [beta]"
git push
```

Creates `X.Y.Z-beta.N+sha` prerelease.

### Release Candidate (final testing)

```bash
git commit -m "chore: prepare release [rc]"
git push
```

Creates `X.Y.Z-rc.N` prerelease and deletes all betas.

### Stable Release

1. Wait for release-please to create a PR titled "chore(main): release X.Y.Z"
2. Review the PR (changelog, version bump)
3. Merge the PR

Creates stable `X.Y.Z` release and cleans up all prereleases.

## Requirements

- Node/TypeScript project with `package.json`
- GitHub repository
- Uses conventional commits (`feat:`, `fix:`, `chore:`, etc.)

## Related

- [Release Please](https://github.com/googleapis/release-please)
- [Conventional Commits](https://www.conventionalcommits.org/)

## For Obsidian Plugins

Use the `obsidian-dev` plugin instead, which includes:
- `/obsidian.init` - Scaffold new Obsidian plugin with release pipeline
- `/obsidian.release` - Trigger beta/RC/stable releases
- Obsidian-specific files: `manifest.json`, `versions.json`, BRAT support
