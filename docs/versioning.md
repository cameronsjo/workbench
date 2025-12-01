# Versioning

Automatic semantic versioning on push to main.

## How It Works

1. Push commit to `main`
2. Workflow parses conventional commit prefix
3. Bumps version in `marketplace.json`
4. Creates git tag and GitHub release

## Version Bumps

| Commit Prefix | Bump | Example |
|--------------|------|---------|
| `feat!:` or `BREAKING CHANGE` | MAJOR | 1.0.0 -> 2.0.0 |
| `feat:` | MINOR | 1.0.0 -> 1.1.0 |
| `fix:` | PATCH | 1.0.0 -> 1.0.1 |
| `chore:`, `docs:`, `refactor:` | none | no release |

## Examples

```bash
# New feature -> 1.0.0 -> 1.1.0
git commit -m "feat: add /deploy command"

# Bug fix -> 1.1.0 -> 1.1.1
git commit -m "fix: correct type hints in python-expert"

# Breaking change -> 1.1.1 -> 2.0.0
git commit -m "feat!: restructure plugin layout"

# No version bump
git commit -m "docs: update README"
git commit -m "chore: clean up scripts"
```

## Skipping CI

Add `[skip-ci]` to prevent version bumps (used internally by release workflow).

## Checking Updates

```bash
gh release list --repo cameronsjo/claude-marketplace --limit 1
```
