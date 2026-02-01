---
description: Set up three-stage release pipeline (Beta → RC → Stable) with GitHub Actions and release-please
category: project-setup
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Setup Release Pipeline

Set up a complete three-stage release pipeline for Node/TypeScript projects.

## Release Flow

```
[beta] keyword → X.Y.Z-beta.N+sha prerelease (for testing)
       ↓
[rc] keyword → X.Y.Z-rc.N release candidate (cleans up betas)
       ↓
Merge release-please PR → Stable X.Y.Z release (cleans up RCs)
```

## Process

### 1. Pre-flight Checks

Verify this is a Node/TypeScript project:

```bash
# Check for package.json
if [ ! -f package.json ]; then
  echo "❌ No package.json found. This command requires a Node/TypeScript project."
  exit 1
fi

# Extract project name
PROJECT_NAME=$(jq -r '.name' package.json)
echo "Project: $PROJECT_NAME"

# Check for existing workflows
if [ -d .github/workflows ]; then
  echo "⚠️  .github/workflows already exists"
  ls -la .github/workflows/
fi
```

### 2. Create Workflow Directory

```bash
mkdir -p .github/workflows
```

### 3. Generate CI Workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]
    steps:
      - uses: actions/checkout@v4
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm run lint --if-present
      - run: npm run type-check --if-present
      - run: npm test --if-present
      - run: npm run build --if-present
```

### 4. Generate Beta Release Workflow

Create `.github/workflows/beta-release.yml`:

```yaml
name: Beta Release

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: read

env:
  PROJECT_NAME: {{PROJECT_NAME}}

jobs:
  check-and-version:
    runs-on: ubuntu-latest
    outputs:
      should_release: ${{ steps.check.outputs.should_release }}
      version: ${{ steps.version.outputs.version }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check for [beta] keyword
        id: check
        run: |
          COMMIT_MSG=$(git log -1 --pretty=%B)
          if [[ "$COMMIT_MSG" =~ \[beta\] ]]; then
            echo "should_release=true" >> $GITHUB_OUTPUT
          else
            echo "should_release=false" >> $GITHUB_OUTPUT
          fi

      - name: Determine version
        id: version
        if: steps.check.outputs.should_release == 'true'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Try release-please PR first
          PR_BRANCH=$(gh pr list --state open --json headRefName,title --jq '.[] | select(.title | startswith("chore(main): release")) | .headRefName' | head -1)

          if [ -n "$PR_BRANCH" ]; then
            git fetch origin "$PR_BRANCH" --depth=1
            NEXT_VERSION=$(git show "origin/$PR_BRANCH:package.json" | jq -r '.version')
          fi

          if [ -z "$NEXT_VERSION" ] || [ "$NEXT_VERSION" = "null" ]; then
            NEXT_VERSION=$(jq -r '.version' package.json)
          fi

          BASE_VERSION=$(echo "$NEXT_VERSION" | sed -E 's/^([0-9]+\.[0-9]+\.[0-9]+).*/\1/')
          SHORT_SHA=$(git rev-parse --short HEAD)
          LAST_STABLE=$(git tag -l --sort=-v:refname | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | head -1)

          if [ -n "$LAST_STABLE" ]; then
            COMMIT_COUNT=$(git rev-list --count ${LAST_STABLE}..HEAD)
          else
            COMMIT_COUNT=$(git rev-list --count HEAD)
          fi

          echo "version=${BASE_VERSION}-beta.${COMMIT_COUNT}+${SHORT_SHA}" >> $GITHUB_OUTPUT

  build-and-release:
    needs: check-and-version
    if: needs.check-and-version.outputs.should_release == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20.x'
          cache: 'npm'
      - run: npm ci
      - run: npm test --if-present
      - run: npm run build --if-present

      - name: Create Beta Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          VERSION="${{ needs.check-and-version.outputs.version }}"
          gh release create "$VERSION" \
            --title "🧪 $VERSION" \
            --notes "**Beta release for testing**" \
            --prerelease \
            dist/* 2>/dev/null || echo "No dist/ to upload"
```

### 5. Generate RC Release Workflow

Create `.github/workflows/rc-release.yml`:

```yaml
name: Release Candidate

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: read

jobs:
  check-and-version:
    runs-on: ubuntu-latest
    outputs:
      should_release: ${{ steps.check.outputs.should_release }}
      version: ${{ steps.version.outputs.version }}
      base_version: ${{ steps.version.outputs.base_version }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check for [rc] keyword
        id: check
        run: |
          COMMIT_MSG=$(git log -1 --pretty=%B)
          if [[ "$COMMIT_MSG" =~ \[rc\] ]]; then
            echo "should_release=true" >> $GITHUB_OUTPUT
          else
            echo "should_release=false" >> $GITHUB_OUTPUT
          fi

      - name: Determine version
        id: version
        if: steps.check.outputs.should_release == 'true'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          PR_BRANCH=$(gh pr list --state open --json headRefName,title --jq '.[] | select(.title | startswith("chore(main): release")) | .headRefName' | head -1)

          if [ -n "$PR_BRANCH" ]; then
            git fetch origin "$PR_BRANCH" --depth=1
            NEXT_VERSION=$(git show "origin/$PR_BRANCH:package.json" | jq -r '.version')
          fi

          if [ -z "$NEXT_VERSION" ] || [ "$NEXT_VERSION" = "null" ]; then
            NEXT_VERSION=$(jq -r '.version' package.json)
          fi

          BASE_VERSION=$(echo "$NEXT_VERSION" | sed -E 's/^([0-9]+\.[0-9]+\.[0-9]+).*/\1/')
          RC_COUNT=$(gh release list --limit 100 | grep -c "${BASE_VERSION}-rc" || echo "0")
          RC_NUM=$((RC_COUNT + 1))

          echo "version=${BASE_VERSION}-rc.${RC_NUM}" >> $GITHUB_OUTPUT
          echo "base_version=${BASE_VERSION}" >> $GITHUB_OUTPUT

  build-and-release:
    needs: check-and-version
    if: needs.check-and-version.outputs.should_release == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20.x'
          cache: 'npm'
      - run: npm ci
      - run: npm test --if-present
      - run: npm run build --if-present

      - name: Delete beta prereleases
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          BASE="${{ needs.check-and-version.outputs.base_version }}"
          gh release list --limit 100 | grep "${BASE}-beta" | awk '{print $1}' | while read tag; do
            gh release delete "$tag" --yes --cleanup-tag || true
          done

      - name: Create RC Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          VERSION="${{ needs.check-and-version.outputs.version }}"
          gh release create "$VERSION" \
            --title "🚀 $VERSION" \
            --notes "**Release Candidate** - Ready for final testing" \
            --prerelease \
            dist/* 2>/dev/null || echo "No dist/ to upload"
```

### 6. Generate Release Please Workflow

Create `.github/workflows/release-please.yml`:

```yaml
name: Release Please

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    outputs:
      release_created: ${{ steps.release.outputs.release_created }}
      tag_name: ${{ steps.release.outputs.tag_name }}
      version: ${{ steps.release.outputs.version }}
    steps:
      - uses: googleapis/release-please-action@v4
        id: release
        with:
          release-type: node
          token: ${{ secrets.GITHUB_TOKEN }}

  build-release:
    needs: release-please
    if: ${{ needs.release-please.outputs.release_created == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20.x'
          cache: 'npm'
      - run: npm ci
      - run: npm run build --if-present

      - name: Upload Release Assets
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          if [ -d dist ]; then
            gh release upload ${{ needs.release-please.outputs.tag_name }} dist/* --clobber
          fi

      - name: Clean up prereleases
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          VERSION="${{ needs.release-please.outputs.version }}"
          gh release list --limit 100 | grep "${VERSION}-rc" | awk '{print $1}' | while read tag; do
            gh release delete "$tag" --yes --cleanup-tag || true
          done
          gh release list --limit 100 | grep "${VERSION}-beta" | awk '{print $1}' | while read tag; do
            gh release delete "$tag" --yes --cleanup-tag || true
          done
```

### 7. Create Release Please Config

Create `release-please-config.json`:

```json
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
  "separate-pull-requests": false,
  "packages": {
    ".": {
      "release-type": "node",
      "bump-minor-pre-major": true,
      "bump-patch-for-minor-pre-major": true,
      "draft": false,
      "prerelease": false,
      "changelog-path": "CHANGELOG.md"
    }
  }
}
```

### 8. Create Release Please Manifest

Create `.release-please-manifest.json` with current version from package.json:

```bash
VERSION=$(jq -r '.version' package.json)
echo "{\".\": \"$VERSION\"}" > .release-please-manifest.json
```

## Output Summary

After completion, display:

```
✅ Release pipeline configured!

📁 Created files:
   - .github/workflows/ci.yml
   - .github/workflows/beta-release.yml
   - .github/workflows/rc-release.yml
   - .github/workflows/release-please.yml
   - release-please-config.json
   - .release-please-manifest.json

🚀 Usage:
   Beta:   git commit -m "feat: add feature [beta]" && git push
   RC:     git commit -m "chore: prepare release [rc]" && git push
   Stable: Merge the release-please PR when ready

📋 Next steps:
   1. Commit these files
   2. Push to GitHub
   3. Use conventional commits (feat:, fix:, etc.)
```
