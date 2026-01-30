# Claude Code Marketplace (Archived)

**This repository has been deprecated.** Content has moved to [cameronsjo/claude-settings](https://github.com/cameronsjo/claude-settings).

## What Happened

The marketplace concept didn't pan out. Most plugins were just prompts that duplicated Claude Code's built-in agents. The valuable content has been moved to dotfiles.

## New Home

```
~/.claude/
├── commands/     # /turbo, /roast, /ready, etc.
├── rules/        # Code standards, language-specific rules
└── tools/        # Actual code: user-memory MCP, conversation-search
```

See [cameronsjo/claude-settings](https://github.com/cameronsjo/claude-settings).

## Lessons Learned

1. **Prompts aren't plugins** - If it just tells Claude to be good at something, use built-in agents
2. **Dotfiles > marketplaces** - Rules files work better for personal configuration
3. **Only ship actual tools** - MCP servers, CLI tools, things that run

## License

MIT
