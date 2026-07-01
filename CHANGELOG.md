# Changelog

All notable changes to the workbench marketplace registry are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Plugins carry no version numbers — the marketplace uses SHA-based cache invalidation
(see `docs/adr/0001-plugin-cache-versioning.md`), so this log tracks registry changes
rather than tagged releases.

## [Unreleased]

### Added

- Absorbed the attunements products as standalone `url` entries: `bosun`, `llm-council`,
  `media-mcp`, `mouse-mcp`, `obaass`, `obsidi-backup`, `obsidi-claude`, `obsidi-mcp` (#44).

### Changed

- Re-pointed the 12 cadence-ecosystem plugins to the `cameronsjo/cadence` monorepo via
  `git-subdir` sources, replacing their standalone `url` sources (#43).

### Removed

- Dropped `cadence-lab`, which split off into its own marketplace (#43).

---

History prior to this entry was inherited from the predecessor `claude-marketplace`
repository and did not reflect workbench's contents; it has been reset. Run
`scripts/changelog-gen.sh` to regenerate a fuller changelog from conventional commits
if a more detailed history is wanted.
