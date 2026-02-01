# Claude Marketplace

Personal Claude Code plugin marketplace.

## Installation

```bash
# Add this marketplace
/plugin marketplace add cameronsjo/claude-marketplace

# Install plugins
/plugin install release-pipelines
/plugin install obsidian-dev
```

## Plugins

### release-pipelines

Three-stage release pipeline (Beta → RC → Stable) for Node/TypeScript projects.

**Commands:**
- `/setup-release-pipeline` - Generate GitHub Actions workflows for release automation

**Usage:**
```bash
git commit -m "feat: add feature [beta]"   # Beta prerelease
git commit -m "chore: prepare [rc]"        # Release candidate
# Merge release-please PR                  # Stable release
```

### obsidian-dev

Complete toolkit for Obsidian plugin development.

**Commands:**
- `/obsidian.init` - Scaffold new Obsidian plugin with modern tooling
- `/obsidian.release` - Trigger beta/RC/stable releases

**Agent:**
- `obsidian-plugin-expert` - TypeScript patterns, Obsidian API, esbuild config, BRAT integration

## License

MIT
