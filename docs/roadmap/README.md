# Roadmap

This directory is the single source of truth for what this project does, what's planned, and what we decided against.

## Active Work

| File | Purpose |
|------|---------|
| [ideas.md](ideas.md) | Prioritized backlog ready to build |
| [research.md](research.md) | Topics under investigation |

## Implemented

Features that have shipped. Each doc explains **what** it does, **why** we built it, and **how** it works.

Browse [completed/](completed/) or see highlights:

- [Registry Architecture](completed/registry-architecture.md) - Central registry with symlinks to plugins
- [Plugin Builder CLI](completed/plugin-builder-cli.md) - Dashboard, validation, asset management

## Rejected

Decisions we made **not** to do something. Check here before proposing something new - it may have been considered.

Browse [rejected/](rejected/) or see highlights:

- [Cloud Sync](rejected/cloud-sync.md) - Git handles this
- [GUI Installer](rejected/gui-installer.md) - CLI-first tool

## How This Works

```
ideas.md ──────→ (branch/PR) ──→ completed/{feature}.md
     ↓
research.md ───→ ideas.md      rejected/{feature}.md
```

1. **Ideas** are prioritized (p0-p4) and estimated (small/medium/large)
2. **Research** items need investigation before they can be estimated
3. When work ships, it moves to **completed/** with full documentation
4. Rejected ideas go to **rejected/** with reasoning

Git blame provides all date tracking. No metadata to maintain.

## For Agents & Automation

- Search `completed/` to understand existing functionality
- Search `rejected/` before suggesting previously-declined features
- Use `ideas.md` and `research.md` for current planning state
- All files are markdown - grep-friendly, LLM-friendly
