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
/plugin install core-productivity@cameronsjo

# Language-specific toolkits
/plugin install python-toolkit@cameronsjo
/plugin install typescript-toolkit@cameronsjo

# Specialty plugins
/plugin install security-suite@cameronsjo
/plugin install api-development@cameronsjo
```

## Recommended Plugin Combinations

### For Python Projects

```bash
/plugin install core-productivity@cameronsjo
/plugin install python-toolkit@cameronsjo
/plugin install security-suite@cameronsjo
```

### For TypeScript/React Projects

```bash
/plugin install core-productivity@cameronsjo
/plugin install typescript-toolkit@cameronsjo
/plugin install dx-tools@cameronsjo
```

### For API Development

```bash
/plugin install core-productivity@cameronsjo
/plugin install api-development@cameronsjo
/plugin install security-suite@cameronsjo
```

### For Full-Stack Development

```bash
/plugin install core-productivity@cameronsjo
/plugin install typescript-toolkit@cameronsjo
/plugin install python-toolkit@cameronsjo
/plugin install api-development@cameronsjo
/plugin install pr-workflow@cameronsjo
```

## Project Configuration

For team projects, configure plugins in `.claude/settings.json`:

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
  "enabledPlugins": [
    "core-productivity@cameronsjo",
    "python-toolkit@cameronsjo"
  ]
}
```

This ensures all team members have the same plugins available.

## Next Steps

- Read the [Plugin Guide](plugin-guide.md) to understand how plugins work together
- Check individual plugin documentation for detailed usage
- Explore the [docs/](.) folder for all available documentation
