# Getting Started

This guide walks you through installing and using the Claude Code Marketplace.

## Prerequisites

- Claude Code CLI installed and configured
- GitHub account (for marketplace access)

## Installation

### Step 1: Add the Marketplace

Add this marketplace to your Claude Code installation:

```bash
/plugin marketplace add cameronsjo/claude-marketplace
```

### Step 2: Browse Available Plugins

List all available plugins:

```bash
/plugin
```

### Step 3: Install Plugins

Install the plugins you need:

```bash
# Core productivity tools (recommended for everyone)
/plugin install core-productivity@cameron-tools

# Language-specific toolkits
/plugin install python-toolkit@cameron-tools
/plugin install typescript-toolkit@cameron-tools

# Specialty plugins
/plugin install security-suite@cameron-tools
/plugin install api-development@cameron-tools
```

## Recommended Plugin Combinations

### For Python Projects

```bash
/plugin install core-productivity@cameron-tools
/plugin install python-toolkit@cameron-tools
/plugin install security-suite@cameron-tools
```

### For TypeScript/React Projects

```bash
/plugin install core-productivity@cameron-tools
/plugin install typescript-toolkit@cameron-tools
/plugin install dx-tools@cameron-tools
```

### For API Development

```bash
/plugin install core-productivity@cameron-tools
/plugin install api-development@cameron-tools
/plugin install security-suite@cameron-tools
```

### For Full-Stack Development

```bash
/plugin install core-productivity@cameron-tools
/plugin install typescript-toolkit@cameron-tools
/plugin install python-toolkit@cameron-tools
/plugin install api-development@cameron-tools
/plugin install pr-workflow@cameron-tools
```

## Project Configuration

For team projects, configure plugins in `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "cameron-tools": {
      "source": {
        "source": "github",
        "repo": "cameronsjo/claude-marketplace"
      }
    }
  },
  "enabledPlugins": [
    "core-productivity@cameron-tools",
    "python-toolkit@cameron-tools"
  ]
}
```

This ensures all team members have the same plugins available.

## Next Steps

- Read the [Plugin Guide](plugin-guide.md) to understand how plugins work together
- Check individual plugin documentation for detailed usage
- Explore the [docs/](.) folder for all available documentation
