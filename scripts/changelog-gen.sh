#!/usr/bin/env bash
# changelog-gen.sh — Generate CHANGELOG.md from conventional commits between tags
#
# Usage:
#   scripts/changelog-gen.sh                    # All ecosystem repos
#   scripts/changelog-gen.sh cadence            # Single repo
#   scripts/changelog-gen.sh --dry-run          # Show what would happen
#
# Requires at least 2 tags in a repo to generate a diff.
# Uses git log — no external dependencies.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKBENCH_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MARKETPLACE="$WORKBENCH_DIR/.claude-plugin/marketplace.json"
BASE_DIR="$HOME/Projects/claude-configurations"

DRY_RUN=false
TARGET_REPO=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help)
      echo "Usage: $(basename "$0") [repo-name] [--dry-run]"
      echo ""
      echo "Generate CHANGELOG.md from conventional commits between tags."
      echo "Without arguments, runs on all ecosystem repos."
      exit 0
      ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *) TARGET_REPO="$1"; shift ;;
  esac
done

# Build repo list
REPOS=()
if [[ -n "$TARGET_REPO" ]]; then
  REPOS+=("$TARGET_REPO")
else
  while IFS= read -r url; do
    REPOS+=("$(basename "$url" .git)")
  done < <(python3 -c "
import json
with open('$MARKETPLACE') as f:
    data = json.load(f)
for p in data.get('plugins', []):
    print(p['source']['url'])
")
  REPOS+=("cadence-hooks" "workbench")
fi

generate_changelog() {
  local dir="$1"
  local repo_name="$2"

  # Get sorted tags (semver order)
  local tags
  tags=$(git -C "$dir" tag -l 'v*' --sort=version:refname)
  local tag_count
  tag_count=$(echo "$tags" | grep -c 'v' || true)

  if [[ $tag_count -lt 2 ]]; then
    echo "  SKIP  $repo_name — needs at least 2 tags (has $tag_count)"
    return
  fi

  local changelog="$dir/CHANGELOG.md"
  local header="# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
"

  local entries=""

  # Process tags from newest to oldest
  local prev_tag=""
  while IFS= read -r tag; do
    if [[ -n "$prev_tag" ]]; then
      local date
      date=$(git -C "$dir" log -1 --format=%cs "$prev_tag")

      local section="## [$prev_tag] - $date

"
      # Group by conventional commit type
      for type_label in "feat:Added" "fix:Fixed" "refactor:Changed" "perf:Changed" "docs:Documentation" "test:Testing" "chore:Maintenance" "ci:CI"; do
        local prefix="${type_label%%:*}"
        local heading="${type_label##*:}"

        local commits
        commits=$(git -C "$dir" log --format="- %s" "$tag..$prev_tag" --grep="^${prefix}" --no-merges 2>/dev/null || true)

        if [[ -n "$commits" ]]; then
          section+="### $heading

$commits

"
        fi
      done

      entries+="$section"
    fi
    prev_tag="$tag"
  done < <(echo "$tags" | tac)

  if [[ -z "$entries" ]]; then
    echo "  SKIP  $repo_name — no conventional commits between tags"
    return
  fi

  if $DRY_RUN; then
    echo "  WOULD WRITE $repo_name/CHANGELOG.md ($tag_count tags)"
    return
  fi

  echo "${header}${entries}" > "$changelog"
  echo "  WROTE $repo_name/CHANGELOG.md"
}

echo "Generating changelogs..."
echo ""

for repo in "${REPOS[@]}"; do
  dir="$BASE_DIR/$repo"
  if [[ ! -d "$dir/.git" ]]; then
    echo "  SKIP  $repo — not found"
    continue
  fi
  generate_changelog "$dir" "$repo"
done

echo ""
echo "Done."
