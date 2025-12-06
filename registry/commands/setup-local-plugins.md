---
description: Setup project-local plugin installation linked to a GitHub marketplace
allowed-tools: Bash, Read, Write, Edit
disable-model-invocation: true
---

# Setup Local Plugins

The user wants to configure project-local plugins that are linked to a GitHub marketplace repository.

## Task

1. Check if `.claude/settings.json` already exists in the current project
2. If it exists, read it and merge the new marketplace/plugins configuration
3. If it doesn't exist, create it with the marketplace configuration

## Configuration to Add

```json
{
  "extraKnownMarketplaces": {
    "cameronsjo": {
      "source": {
        "source": "github",
        "repo": "cameronsjo/claude-marketplace"
      }
    }
  },
  "enabledPlugins": {
    // Add plugins based on user input or suggest based on project type
  }
}
```

## Plugin Selection

Ask the user which plugins they want to enable from the marketplace. Common options:

- **core** - Core productivity (commit, check, clean, ready commands)
- **api** - API development tools
- **security** - Security review tools
- **obsidian** - Obsidian PKM workflows
- **obsidian-dev** - Obsidian plugin development
- **mcp** - MCP server development

## Steps

1. Create `.claude` directory if it doesn't exist: `mkdir -p .claude`
2. Check for existing settings: `cat .claude/settings.json 2>/dev/null || echo "{}"`
3. Ask user which plugins to enable
4. Write/merge the settings.json file
5. Inform user they'll need to restart Claude Code and trust the folder

Do NOT add plugins the user didn't request. Always confirm the selection before writing.
