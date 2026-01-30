# ADR-0002: Lean Marketplace Philosophy

## Status

Accepted

## Date

2025-01-25

## Context

The marketplace grew to 23 plugins with ~55k lines. Most were "expert prompts" that duplicated Claude Code's built-in agents (python-expert, typescript-expert, security-auditor, mcp-expert, etc.).

At work, we converted everything to rules files. The plugin overhead provided no value over `~/.claude/rules/`.

Chezmoi doesn't play well with the `.claude` directory structure, making dotfiles management painful.

## Decision

**The marketplace only contains things that provide unique value beyond prompts.**

### Inclusion Criteria

A plugin MUST have at least one of:

1. **Running code** - Actual executables, MCP servers, CLI tools
2. **Unique UX** - Commands that provide ergonomic value (`/turbo` is better UX than editing a rules file)
3. **Non-trivial resources** - Templates/schemas that would take significant effort to recreate

A plugin MUST NOT be:

1. **An "expert" prompt** - Use built-in agents
2. **A wrapper around standard tools** - Use the tools directly (gitleaks, semgrep, spectral)
3. **Workflow-specific** - Put in your dotfiles, not a shared marketplace

### What Survived

| Plugin | Why it stays |
|--------|-------------|
| **core** | `/ready` wraps a CLI, modes (`/turbo`, `/roast`) are good UX |
| **essentials** | user-memory MCP is actual TypeScript that does something unique |
| **research** | conversation-search is actual TypeScript that does something unique |

### What Died

| Category | Examples | Use Instead |
|----------|----------|-------------|
| Expert prompts | python, typescript, mcp, cloud, data, obsidian | Built-in agents |
| Tool wrappers | security (OWASP scripts) | gitleaks, semgrep, trivy |
| Niche workflows | feature-flags, session-sync, executive-* | Your dotfiles |
| Meta tooling | meta, obsidian-dev | Not needed |

## Consequences

### Positive

- Marketplace is actually useful, not bloated
- Clear criteria for future additions
- Works better with dotfiles management (less `.claude` pollution)
- Forces real value creation, not prompt engineering theater

### Negative

- Breaking change for anyone using removed plugins
- Less "impressive" plugin count
- Some useful prompts are gone (but they belong in dotfiles)

### Neutral

- May add plugins back if they gain real code
- Philosophy may evolve as Claude Code evolves

## Future Direction

Consider converting this from a "plugin marketplace" to a "tools repository":

```
tools/
  user-memory/     # Standalone MCP server
  conversation-search/  # Standalone CLI tool
  claude-ready/    # Standalone CLI tool

rules/            # Example rules for dotfiles
  turbo.md
  roast.md
```

This would work better with chezmoi and make the value proposition clearer.
