# Docker Validation - 2026-02-11

Clean-room validation of the full plugin setup from scratch in a containerized environment.

## Environment

- **Runtime**: Colima (`--cpu 2 --memory 4 --vm-type vz`)
- **Image**: `ubuntu:24.04`
- **Auth**: GitHub token passed via `gh auth token` with git `insteadOf` URL rewrite
- **Method**: Clone settings repo, validate setup script, verify all 17 plugin repos

## Checks Performed

| # | Check | Result |
|---|---|---|
| 1 | `setup-marketplaces.sh` bash syntax validation | PASS |
| 2 | All 17 plugin repos accessible via GitHub API | PASS |
| 3 | Valid `plugin.json` in each repo's `.claude-plugin/` | PASS |
| 4 | Rules plugin: no `javascript.md` (dropped, TS covers JS) | PASS |
| 5 | Rules plugin: no `golang.md` (renamed to `go.md`) | PASS |
| 6 | Rules plugin: `go.md` present with correct globs | PASS |
| 7 | Rules plugin: `rules-init.md` command (not `init.md`) | PASS |
| 8 | Essentials plugin: no `hype.md`/`roast.md`/`sass.md` (moved to vibes) | PASS |
| 9 | Obsidian plugin: no redundant `obsidian.` prefix on commands | PASS |
| 10 | `the-artificer.md` present in `~/.claude/rules/` | PASS |
| 11 | All plugin repos have LICENSE and .gitignore | PASS |

## What Was Validated

### Setup Script (`setup-marketplaces.sh`)

- Registers 3 marketplaces: `anthropics/claude-plugins-official`, `steveyegge/beads`, `cameronsjo/workbench`
- Local overrides all commented out (correct for non-dev machines)
- Auto-install logic reads `settings.json` `enabledPlugins` and installs missing

### Plugin Structure Consistency

Every plugin repo follows the standard layout:

```
.claude-plugin/
  plugin.json         # name, version, description, components
  marketplace.json    # standalone marketplace declaration
commands/             # slash commands (.md)
agents/               # subagents (.md)
skills/               # skills with SKILL.md
```

### Rules Plugin Specifics

- 6 language rules: `csharp.md`, `go.md`, `java.md`, `python.md`, `rust.md`, `typescript.md`
- 1 security rule: `security.md`
- Self-destructing `rules-init` command copies rules to `~/.claude/rules/`, deletes itself from cache
- Filename conflict detection: checks for `golang.md` vs `go.md`, `javascript.md` vs `typescript.md`, etc.

### Migration Completeness

- Vibes commands (`hype`, `roast`, `sass`, `unhinged`) removed from essentials, present in vibes
- Obsidian commands use clean names (`init.md`, `release.md`) not prefixed (`obsidian.init.md`)
- Session-continuity commands use clean names (`init.md`, `log.md`, `sync.md`)

## How to Reproduce

```bash
colima start --cpu 2 --memory 4 --vm-type vz
docker run -it --rm \
  -e GH_TOKEN="$(gh auth token)" \
  ubuntu:24.04 bash

# Inside container:
apt-get update && apt-get install -y git curl jq
git config --global url."https://x-access-token:${GH_TOKEN}@github.com/".insteadOf "https://github.com/"
git clone https://github.com/cameronsjo/claude-settings ~/.claude

# Validate setup script
bash -n ~/.claude/setup-marketplaces.sh

# Check all repos (example for one)
curl -sH "Authorization: token $GH_TOKEN" \
  https://api.github.com/repos/cameronsjo/essentials/contents/.claude-plugin/plugin.json \
  | jq -r '.content' | base64 -d | jq .
```
