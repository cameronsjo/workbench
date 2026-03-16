#!/usr/bin/env bash
# epoch-tag.sh — Tag all ecosystem repos at a shared version
#
# Usage:
#   scripts/epoch-tag.sh                    # Tag all repos at current epoch
#   scripts/epoch-tag.sh --version 0.5.0    # Tag at specific version
#   scripts/epoch-tag.sh --dry-run          # Show what would happen
#
# Reads the plugin list from marketplace.json, adds cadence-hooks,
# and tags each repo at HEAD.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKBENCH_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MARKETPLACE="$WORKBENCH_DIR/.claude-plugin/marketplace.json"
BASE_DIR="$HOME/Projects/claude-configurations"

# Defaults
VERSION=""
DRY_RUN=false

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --version) VERSION="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help)
      echo "Usage: $(basename "$0") [--version X.Y.Z] [--dry-run]"
      echo ""
      echo "Tags all ecosystem repos at a shared version."
      echo "Reads plugin list from marketplace.json + cadence-hooks."
      echo ""
      echo "Options:"
      echo "  --version X.Y.Z   Version to tag (default: prompt)"
      echo "  --dry-run          Show what would happen without doing it"
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$VERSION" ]]; then
  echo "Error: --version is required" >&2
  echo "Usage: $(basename "$0") --version 0.4.0 [--dry-run]" >&2
  exit 1
fi

if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Error: '$VERSION' is not valid semver (expected X.Y.Z)" >&2
  exit 1
fi

TAG="v${VERSION}"

# Build repo list from marketplace.json + extras
REPOS=()

# Extract repo names from marketplace plugin URLs
while IFS= read -r url; do
  name=$(basename "$url" .git)
  REPOS+=("$name")
done < <(python3 -c "
import json, sys
with open('$MARKETPLACE') as f:
    data = json.load(f)
for p in data.get('plugins', []):
    print(p['source']['url'])
")

# Add repos not in marketplace
REPOS+=("cadence-hooks" "workbench")

echo "Ecosystem epoch tag: $TAG"
echo "Repos: ${#REPOS[@]}"
echo ""

TAGGED=0
SKIPPED=0
ERRORS=0

for repo in "${REPOS[@]}"; do
  dir="$BASE_DIR/$repo"

  if [[ ! -d "$dir/.git" ]]; then
    echo "  SKIP  $repo — not found at $dir"
    ((SKIPPED++))
    continue
  fi

  # Check if tag already exists
  if git -C "$dir" rev-parse "$TAG" >/dev/null 2>&1; then
    echo "  EXISTS $repo — $TAG already exists"
    ((SKIPPED++))
    continue
  fi

  if $DRY_RUN; then
    echo "  WOULD TAG $repo at $TAG (HEAD: $(git -C "$dir" rev-parse --short HEAD))"
    ((TAGGED++))
    continue
  fi

  # Tag and push
  if git -C "$dir" tag "$TAG" && git -C "$dir" push origin "$TAG" 2>/dev/null; then
    echo "  TAGGED $repo at $TAG"
    ((TAGGED++))
  else
    echo "  ERROR  $repo — failed to tag or push"
    ((ERRORS++))
  fi
done

echo ""
if $DRY_RUN; then
  echo "Dry run complete: $TAGGED would be tagged, $SKIPPED skipped, $ERRORS errors"
else
  echo "Done: $TAGGED tagged, $SKIPPED skipped, $ERRORS errors"
fi

[[ $ERRORS -eq 0 ]] || exit 1
