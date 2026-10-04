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

- `go` entry description no longer states a command count; the plugin's
  command set changes with its own releases (cameronsjo/cadence#1375).
- Re-pointed the 12 cadence-ecosystem plugins to the `cameronsjo/cadence` monorepo via
  `git-subdir` sources, replacing their standalone `url` sources (#43).

### Removed

- Removed the `auditing-claude-md` entry. Claude Code now ships a built-in CLAUDE.md audit (`/doctor prompt-audit`), and the `cameronsjo/auditing-claude-md` repo is archived. If a machine still has it installed, run `claude plugin uninstall auditing-claude-md@workbench`; for a project-scope install, run it from that project's directory.
- Removed the `homebridge-dev` entry. The skill and its `homebridge-explorer` agent now live as repo skills in `cameronsjo/homebridge`, the only repo that used them, and the `cameronsjo/homebridge-dev` repo is retired. It may still be installed at project scope (recorded against the old `~/Projects/homebridge` path); remove the `homebridge-dev@workbench` entry from that profile's `plugins/installed_plugins.json`, since `claude plugin uninstall` needs the original project directory.
- Removed the `cadence-canon` entry — the plugin is retired and its session hook wiring now ships in `cadence` (cadence-ecosystem ADR-0030 Phase 2). On every machine, run `claude plugin uninstall cadence-canon@workbench`; until you do, that machine fires each session hook twice (harmless — the hooks are idempotent — but nudge text and the SessionStart block appear doubled).
- Removed the `cadence-kanban` entry — the board was retired and the plugin deleted
  upstream (#51).
- Dropped `cadence-lab`, which split off into its own marketplace (#43).

---

History prior to this entry was inherited from the predecessor `claude-marketplace`
repository and did not reflect workbench's contents; it has been reset. Run
`scripts/changelog-gen.sh` to regenerate a fuller changelog from conventional commits
if a more detailed history is wanted.
