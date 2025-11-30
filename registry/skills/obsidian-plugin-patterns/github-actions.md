# GitHub Actions Templates for Obsidian Plugins

## CI Workflow (ci.yml)

```yaml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20.x"
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Build
        run: npm run build

      - name: Test
        run: npm test
```

## Release Please Workflow (release-please.yml)

```yaml
name: Release Please

on:
  push:
    branches:
      - main

permissions:
  contents: write
  pull-requests: write

env:
  PLUGIN_NAME: your-plugin-name  # Change this

jobs:
  release-please:
    runs-on: ubuntu-latest
    outputs:
      release_created: ${{ steps.release.outputs.release_created }}
      tag_name: ${{ steps.release.outputs.tag_name }}
      version: ${{ steps.release.outputs.version }}
      prs_created: ${{ steps.release.outputs.prs_created }}
      pr_branch: ${{ steps.release.outputs.pr && fromJson(steps.release.outputs.pr).headBranchName || '' }}
    steps:
      - uses: googleapis/release-please-action@v4
        id: release
        with:
          release-type: node
          token: ${{ secrets.GITHUB_TOKEN }}

  update-versions-json:
    needs: release-please
    if: ${{ needs.release-please.outputs.prs_created == 'true' && needs.release-please.outputs.pr_branch != '' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ needs.release-please.outputs.pr_branch }}
          fetch-depth: 0

      - name: Update versions.json
        run: |
          VERSION=$(jq -r '.version' package.json)
          MIN_VERSION=$(jq -r '.minAppVersion' manifest.json)

          if [ -n "$VERSION" ] && [ "$VERSION" != "null" ]; then
            jq --arg ver "$VERSION" --arg min "$MIN_VERSION" \
              '. + {($ver): $min}' versions.json > versions.json.tmp
            mv versions.json.tmp versions.json

            git config user.name "github-actions[bot]"
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git add versions.json
            git commit -m "chore: update versions.json for $VERSION" || true
            git push
          fi

  build-release:
    needs: release-please
    if: ${{ needs.release-please.outputs.release_created == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20.x"
          cache: "npm"

      - run: npm ci
      - run: npm run build

      - name: Package plugin
        run: |
          mkdir ${{ env.PLUGIN_NAME }}
          cp main.js manifest.json ${{ env.PLUGIN_NAME }}
          [ -f styles.css ] && cp styles.css ${{ env.PLUGIN_NAME }}
          zip -r ${{ env.PLUGIN_NAME }}.zip ${{ env.PLUGIN_NAME }}

      - name: Upload Release Assets
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh release upload ${{ needs.release-please.outputs.tag_name }} \
            ${{ env.PLUGIN_NAME }}.zip main.js manifest.json --clobber
          [ -f styles.css ] && gh release upload ${{ needs.release-please.outputs.tag_name }} styles.css --clobber

      - name: Clean up prereleases
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          VERSION="${{ needs.release-please.outputs.version }}"
          gh release list --limit 100 | grep -E "${VERSION}-(rc|beta)" | awk '{print $1}' | \
            while read tag; do
              gh release delete "$tag" --yes --cleanup-tag || true
            done
```

## Beta Release Workflow (beta-release.yml)

```yaml
name: Beta Release (BRAT)

on:
  push:
    branches:
      - main

permissions:
  contents: write
  pull-requests: read

env:
  PLUGIN_NAME: your-plugin-name  # Change this

jobs:
  check-and-version:
    runs-on: ubuntu-latest
    outputs:
      should_release: ${{ steps.check.outputs.should_release }}
      version: ${{ steps.version.outputs.version }}
      next_version: ${{ steps.version.outputs.next_version }}
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
          # Try to get version from release-please PR
          PR_BRANCH=$(gh pr list --state open --json headRefName,title \
            --jq '.[] | select(.title | startswith("chore(main): release")) | .headRefName' | head -1)

          if [ -n "$PR_BRANCH" ]; then
            git fetch origin "$PR_BRANCH" --depth=1
            NEXT_VERSION=$(git show "origin/$PR_BRANCH:package.json" | jq -r '.version')
          else
            NEXT_VERSION=$(jq -r '.version' package.json)
          fi

          SHORT_SHA=$(git rev-parse --short HEAD)
          LAST_STABLE=$(git tag -l --sort=-v:refname | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | head -1)

          if [ -n "$LAST_STABLE" ]; then
            COMMIT_COUNT=$(git rev-list --count ${LAST_STABLE}..HEAD)
          else
            COMMIT_COUNT=$(git rev-list --count HEAD)
          fi

          BETA_VERSION="${NEXT_VERSION}-beta.${COMMIT_COUNT}+${SHORT_SHA}"
          echo "version=$BETA_VERSION" >> $GITHUB_OUTPUT
          echo "next_version=$NEXT_VERSION" >> $GITHUB_OUTPUT

  build-and-release:
    needs: check-and-version
    if: needs.check-and-version.outputs.should_release == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20.x"
          cache: "npm"

      - run: npm ci
      - run: npm test
      - run: npm run build

      - name: Update manifest version
        run: |
          VERSION="${{ needs.check-and-version.outputs.version }}"
          jq --arg ver "$VERSION" '.version = $ver' manifest.json > tmp.json
          mv tmp.json manifest.json

      - name: Package plugin
        run: |
          mkdir ${{ env.PLUGIN_NAME }}
          cp main.js manifest.json ${{ env.PLUGIN_NAME }}
          [ -f styles.css ] && cp styles.css ${{ env.PLUGIN_NAME }}
          zip -r ${{ env.PLUGIN_NAME }}.zip ${{ env.PLUGIN_NAME }}

      - name: Create Beta Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          VERSION="${{ needs.check-and-version.outputs.version }}"
          NEXT="${{ needs.check-and-version.outputs.next_version }}"
          COMMIT_MSG=$(git log -1 --pretty=%B | head -1)

          gh release create "$VERSION" \
            --title "🧪 $VERSION" \
            --notes "**Beta release for BRAT users**

          Commit: \`$COMMIT_MSG\`
          Target: \`$NEXT\`

          ---
          Install via [BRAT](https://github.com/TfTHacker/obsidian42-brat)" \
            --prerelease \
            ${{ env.PLUGIN_NAME }}.zip main.js manifest.json

          [ -f styles.css ] && gh release upload "$VERSION" styles.css --clobber
```

## Release Please Configuration

### release-please-config.json

```json
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
  "packages": {
    ".": {
      "release-type": "node",
      "bump-minor-pre-major": true,
      "bump-patch-for-minor-pre-major": true,
      "extra-files": ["manifest.json"]
    }
  },
  "separate-pull-requests": false
}
```

### .release-please-manifest.json

```json
{
  ".": "1.0.0"
}
```

## RC Release Workflow (rc-release.yml)

```yaml
name: Release Candidate

on:
  push:
    branches:
      - main

permissions:
  contents: write
  pull-requests: read

env:
  PLUGIN_NAME: your-plugin-name  # Change this

jobs:
  check-and-version:
    runs-on: ubuntu-latest
    outputs:
      should_release: ${{ steps.check.outputs.should_release }}
      version: ${{ steps.version.outputs.version }}
      next_version: ${{ steps.version.outputs.next_version }}
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
          PR_BRANCH=$(gh pr list --state open --json headRefName,title \
            --jq '.[] | select(.title | startswith("chore(main): release")) | .headRefName' | head -1)

          if [ -n "$PR_BRANCH" ]; then
            git fetch origin "$PR_BRANCH" --depth=1
            NEXT_VERSION=$(git show "origin/$PR_BRANCH:package.json" | jq -r '.version')
          else
            NEXT_VERSION=$(jq -r '.version' package.json)
          fi

          # Count existing RCs
          RC_COUNT=$(gh release list --limit 100 | grep -c "${NEXT_VERSION}-rc" || echo "0")
          RC_NUM=$((RC_COUNT + 1))

          RC_VERSION="${NEXT_VERSION}-rc.${RC_NUM}"
          echo "version=$RC_VERSION" >> $GITHUB_OUTPUT
          echo "next_version=$NEXT_VERSION" >> $GITHUB_OUTPUT

  build-and-release:
    needs: check-and-version
    if: needs.check-and-version.outputs.should_release == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20.x"
          cache: "npm"

      - run: npm ci
      - run: npm test
      - run: npm run build

      - name: Update manifest version
        run: |
          VERSION="${{ needs.check-and-version.outputs.version }}"
          jq --arg ver "$VERSION" '.version = $ver' manifest.json > tmp.json
          mv tmp.json manifest.json

      - name: Package plugin
        run: |
          mkdir ${{ env.PLUGIN_NAME }}
          cp main.js manifest.json ${{ env.PLUGIN_NAME }}
          [ -f styles.css ] && cp styles.css ${{ env.PLUGIN_NAME }}
          zip -r ${{ env.PLUGIN_NAME }}.zip ${{ env.PLUGIN_NAME }}

      - name: Clean up beta releases
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          NEXT="${{ needs.check-and-version.outputs.next_version }}"
          gh release list --limit 100 | grep "${NEXT}-beta" | awk '{print $1}' | \
            while read tag; do
              gh release delete "$tag" --yes --cleanup-tag || true
            done

      - name: Create RC Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          VERSION="${{ needs.check-and-version.outputs.version }}"
          NEXT="${{ needs.check-and-version.outputs.next_version }}"

          gh release create "$VERSION" \
            --title "🎯 $VERSION" \
            --notes "**Release Candidate**

          Target version: \`$NEXT\`

          This is a release candidate for testing before stable release.
          All beta releases have been cleaned up.

          ---
          Install via [BRAT](https://github.com/TfTHacker/obsidian42-brat)" \
            --prerelease \
            ${{ env.PLUGIN_NAME }}.zip main.js manifest.json

          [ -f styles.css ] && gh release upload "$VERSION" styles.css --clobber
```
