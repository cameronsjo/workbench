# Development

Development workflow tools - logging agents, project checks, linting, and context loading.

## Commands

| Command | Description |
|---------|-------------|
| `/check` | Run project validation checks and fix errors |
| `/clean` | Fix all linting and formatting issues |
| `/context-prime` | Load project context from README and git files |

## Agents

| Agent | Description |
|-------|-------------|
| `add-logging` | Add storytelling-style structured logging |

## Installation

```bash
/plugin install development@cameronsjo
```

## Usage

### Check

Run project checks without committing:

```
/check
```

Auto-detects language and package manager (npm, pnpm, yarn, bun, Python, Go, Rust, Ruby).

### Clean

Fix all linting and formatting:

```
/clean
```

Runs appropriate formatters and linters for detected languages.

### Context Prime

Load project context after starting fresh:

```
/context-prime
```

### Add Logging Agent

The `add-logging` agent is invoked automatically when you ask Claude to add logging. It follows the "storytelling" philosophy:

**Core principle:** Debug at 3am without reading code.

Every significant operation logs:
1. **Beginning** - What's being attempted with all parameters
2. **Success** - What succeeded with duration
3. **Failure** - What failed with full context and stack trace

```
INFO  "Beginning ProcessPayment. User: u123, OrderId: o456, Amount: $99.00"
INFO  "Successfully ProcessPayment. User: u123, OrderId: o456, Duration: 234ms"
ERROR "Failed ProcessPayment. User: u123, OrderId: o456, Error: CardDeclined"
```

## Philosophy

Development tools should:
- Auto-detect project type and tooling
- Fix issues automatically when possible
- Provide complete context for debugging
- Work across multiple languages
