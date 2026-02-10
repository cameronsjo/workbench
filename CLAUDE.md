# Workbench

The Artificer's workshop. Where seedlings grow out of gear housings and ivy threads through brass armatures. Not a marketplace - a workshop.

Hub registry for all personal Claude Code plugins and curated obra/superpowers forks.

## Structure

```
├── index.json              # Plugin registry (all plugins via URL sources)
├── README.md               # Plugin directory with install instructions
└── docs/                   # Historical design docs
```

## Plugins (17)

### Personal

| Plugin | Repo | Description |
|---|---|---|
| essentials | cameronsjo/essentials | Core workflow: brainstorming, worktrees, enforcement hooks, session management |
| vibes | cameronsjo/vibes | Communication styles: hype, sass, roast, unhinged |
| rules | cameronsjo/rules | Language rules (Python, TS, JS, Go, Rust, Java, C#) + security |
| dev-toolkit | cameronsjo/dev-toolkit | Logging agents, project checks, release pipelines |
| session-continuity | cameronsjo/session-continuity | Cross-session context with timeline logging |
| mcp-toolkit | cameronsjo/mcp-toolkit | MCP server development patterns |
| obsidian | cameronsjo/obsidian | Vault management, markdown, Bases, plugin dev |
| homebridge-dev | cameronsjo/homebridge-dev | Homebridge plugin development |
| image-gen-toolkit | cameronsjo/image-gen-toolkit | Gemini image generation |
| homelab | cameronsjo/homelab | Homelab infrastructure context |

### Superpowers (obra forks)

| Plugin | Repo | Description |
|---|---|---|
| superpowers | cameronsjo/superpowers | TDD, debugging, collaboration patterns |
| superpowers-chrome | cameronsjo/superpowers-chrome | Chrome DevTools Protocol access |
| superpowers-lab | cameronsjo/superpowers-lab | Experimental: tmux, MCP CLI, dedup |
| superpowers-developing-for-claude-code | cameronsjo/superpowers-developing-for-claude-code | Plugin dev docs |
| episodic-memory | cameronsjo/episodic-memory | Conversation semantic search |
| double-shot-latte | cameronsjo/double-shot-latte | Auto-continue |
| elements-of-style | cameronsjo/the-elements-of-style | Strunk's writing guide |

## Plugin Repo Structure

Each plugin repo follows:

```
repo-root/
├── .claude-plugin/
│   ├── marketplace.json    # Declares repo as a standalone marketplace
│   └── plugin.json         # Plugin metadata
├── commands/               # Slash commands (.md)
├── agents/                 # Subagents (.md)
├── skills/                 # Skills with SKILL.md
├── README.md
├── LICENSE
└── .gitignore
```
