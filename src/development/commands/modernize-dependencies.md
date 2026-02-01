---
description: Audit, update, and modernize project dependencies with security-first approach
argument-hint: "[--security-only] [--major]"
allowed-tools: Bash, Read, Edit, WebFetch
---

# Modernize Dependencies

Audit and update project dependencies. Security fixes first, then minor updates, then major upgrades.

## Arguments

- `--security-only` - Only apply security patches
- `--major` - Include major version upgrades (requires careful review)

## Workflow

### 1. Detect Project Type

Check for package files and determine ecosystem:

| File | Ecosystem | Tools |
|------|-----------|-------|
| `package.json` | Node.js | npm, npx |
| `pyproject.toml` | Python (modern) | uv |
| `requirements.txt` | Python (legacy) | uv pip |
| `Cargo.toml` | Rust | cargo |
| `go.mod` | Go | go get |
| `composer.json` | PHP | composer |
| `Gemfile` | Ruby | bundle |

### 2. Security Audit

Run security checks first - these are non-negotiable:

```bash
# Node.js
npm audit

# Python
uv pip audit
# or: pip-audit

# Rust
cargo audit

# Go
govulncheck ./...
```

**If critical/high vulnerabilities found:** Fix these before any other updates.

```bash
# Node.js - auto-fix what's safe
npm audit fix

# For breaking fixes, review first
npm audit fix --dry-run
```

### 3. Check Outdated

```bash
# Node.js
npm outdated

# Python
uv pip list --outdated

# Rust
cargo outdated

# Go
go list -u -m all
```

### 4. Update Strategy

**Order matters:**

1. **Security patches** - Apply immediately
2. **Patch versions** (1.2.3 → 1.2.4) - Safe, bug fixes only
3. **Minor versions** (1.2.3 → 1.3.0) - New features, usually safe
4. **Major versions** (1.2.3 → 2.0.0) - Breaking changes, requires review

**Between each step:** Run tests, verify build.

### 5. Apply Updates

```bash
# Node.js - safe updates within semver
npm update

# Node.js - interactive major upgrades
npx npm-check-updates -i

# Python
uv pip compile --upgrade pyproject.toml -o requirements.txt
uv pip sync requirements.txt

# Rust
cargo update
```

### 6. Major Version Upgrades

For each major upgrade:

1. **Read the changelog** - WebFetch the release notes
2. **Check migration guide** - Most libraries provide one
3. **Identify breaking changes** - Search codebase for deprecated APIs
4. **Update incrementally** - One major upgrade at a time
5. **Run full test suite** - Catch regressions early

### 7. Verify

```bash
# Build
npm run build  # or equivalent

# Test
npm test

# Lint
npm run lint

# Type check (if applicable)
npm run typecheck
```

### 8. Commit Strategy

Commit updates in logical groups:

```
fix(deps): security patches for lodash, axios
chore(deps): minor dependency updates
feat(deps)!: upgrade react 18 → 19
```

## Lockfile Handling

**Always commit lockfiles** (`package-lock.json`, `uv.lock`, `Cargo.lock`, etc.)

If lockfile conflicts occur:
```bash
# Node.js - regenerate
rm package-lock.json && npm install

# Python
uv lock --upgrade
```

## Common Pitfalls

- **Don't update everything at once** - Hard to debug regressions
- **Don't ignore peer dependency warnings** - They cause runtime issues
- **Don't skip the changelog** - Breaking changes hide in minor versions too
- **Don't forget transitive dependencies** - `npm ls <package>` shows the tree

## Examples

```
/modernize-dependencies              # Full update cycle
/modernize-dependencies --security-only   # Just security fixes
/modernize-dependencies --major      # Include major upgrades
```
