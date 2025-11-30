# GUI Installer

> Rejected - Out of scope, CLI-first tool.

## Request

Users asked for a graphical installer. "Point and click to install plugins."

## Decision

**Won't implement.**

## Reasoning

This is a CLI tool for CLI users:
1. Target audience lives in the terminal
2. Claude Code itself is a CLI
3. GUI adds massive complexity for minimal value
4. Platform-specific GUI code (macOS, Windows, Linux)

The plugin system is already simple:
```bash
/plugin install {name}
```

A GUI wouldn't make this meaningfully easier.

## Alternatives

1. **Web browser** - Browse plugins on GitHub, copy install command
2. **TUI** - Interactive terminal UI (lower priority idea)
3. **VS Code extension** - If demand warrants (unlikely)

## Related

- [Web-based Plugin Browser](../ideas.md) - Browse/preview without install GUI
