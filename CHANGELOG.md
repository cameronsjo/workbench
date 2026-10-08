# Changelog

All notable changes to the workbench marketplace registry are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Plugins carry no version numbers — the marketplace uses SHA-based cache invalidation
(see `docs/adr/0001-plugin-cache-versioning.md`), so this log tracks registry changes
rather than tagged releases.

## [Unreleased]

### Added

- Registered six Claude Code mods as `git-subdir` entries from the `cameronsjo/cadence`
  monorepo: `afk`, `board`, `guard-toast`, `herdr-bridge`, `sploot`, `verbs`. Each is
  pinned by a 40-character `sha`, because a mod runs its own code inside every session.
- `pins` workflow and `scripts/check-pins.py`: an allowlist over the whole catalog. It
  fails on a top-level key, an entry key or a source shape it does not list, and unless
  each of the six mods is pinned by commit. On a pull request the rule comes from the
  base branch, so a change cannot relax the rule it is judged by.
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

- Moved the pins of all six mods to cadence `bc367b6d`, the review follow-ups: `afk` registers
  no tools when `tools` is off in config; `herdr-bridge` gains an `identity` setting; `board` and
  `herdr-bridge` re-read the off switch before each acting call; a setting a mod does not
  recognise is shown by name only (cameronsjo/cadence#1659).
- Moved the pins of all six mods (`afk`, `board`, `guard-toast`, `herdr-bridge`, `sploot`,
  `verbs`) to cadence `5cb993a6`. Each gains a status reply on its command, `/<mod> on|off`
  for the session, an `enabled` setting, and a `/config` guard; `afk` gains `/afk in`,
  `/afk idle` and `/afk tools` (cameronsjo/cadence#1657).
- Moved the `sploot` pin to cadence `b37c048162de`: her frisbee is a ball (`/frisbee` is now
  `/ball`), she has more stretches and a lower bow, and her digging kicks soil low onto a pile
  (cameronsjo/cadence#1653).
- `go` entry description no longer states a command count; the plugin's
  command set changes with its own releases (cameronsjo/cadence#1375).
- Re-pointed the 12 cadence-ecosystem plugins to the `cameronsjo/cadence` monorepo via
  `git-subdir` sources, replacing their standalone `url` sources (#43).

### Removed

- Removed the `superpowers-chrome`, `superpowers-developing-for-claude-code`, and `double-shot-latte` entries, whose source repos no longer exist, and the `agent-pool` entry, whose repo is archived. None of the four could install. Part of cameronsjo/cadence-ecosystem#571.
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
