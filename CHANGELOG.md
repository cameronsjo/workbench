# Changelog

All notable changes to the workbench marketplace registry are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Plugins carry no version numbers — the marketplace uses SHA-based cache invalidation
(see `docs/adr/0001-plugin-cache-versioning.md`), so this log tracks registry changes
rather than tagged releases.

## [Unreleased]

### Added

- Registered `go` as a `git-subdir` entry from the `cameronsjo/cadence` monorepo
  (`plugins/go`) — six terse one-shot slash commands, consolidating eight prior
  commands split across an unmanaged user-level dir and the `cadence` plugin
  (cameronsjo/cadence#1370).
- Registered `cadence-dev` as a `git-subdir` entry from the `cameronsjo/cadence`
  monorepo (#48).
- Registered `cadence-data` as a `git-subdir` entry from the `cameronsjo/cadence`
  monorepo (#49).
- Registered `artificer-voice` as a private `url` source (#50).
- Absorbed the attunements products as standalone `url` entries: `bosun`, `llm-council`,
  `media-mcp`, `mouse-mcp`, `obaass`, `obsidi-backup`, `obsidi-claude`, `obsidi-mcp` (#44).

### Changed

- Re-pointed the 12 cadence-ecosystem plugins to the `cameronsjo/cadence` monorepo via
  `git-subdir` sources, replacing their standalone `url` sources (#43).

### Removed

- Removed the `cadence-canon` entry — the plugin is retired and its session hook wiring now ships in `cadence` (cadence-ecosystem ADR-0030 Phase 2). On every machine, run `claude plugin uninstall cadence-canon@workbench`; until you do, that machine fires each session hook twice (harmless — the hooks are idempotent — but nudge text and the SessionStart block appear doubled).
- Removed the `cadence-kanban` entry — the board was retired and the plugin deleted
  upstream (#51).
- Dropped `cadence-lab`, which split off into its own marketplace (#43).

---

History prior to this entry was inherited from the predecessor `claude-marketplace`
repository and did not reflect workbench's contents; it has been reset. Run
`scripts/changelog-gen.sh` to regenerate a fuller changelog from conventional commits
if a more detailed history is wanted.
