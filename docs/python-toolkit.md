# Python Toolkit Plugin

Python development expertise with modern tooling (uv), async patterns, and testing best practices.

## Installation

```bash
/plugin install python-toolkit@cameronsjo
```

## Commands

### `/test-gen`

Generate comprehensive tests using the python-expert agent.

**Usage:**
```bash
/test-gen
```

**Features:**
- Generates pytest test suites
- Creates fixtures and mocks
- Covers edge cases
- Follows testing best practices

## Agents

### python-expert

Advanced Python patterns, async programming, decorators, and testing expertise.

**Capabilities:**
- Type hints and mypy compliance
- Async/await patterns
- Decorator design
- Context managers
- Metaclasses and descriptors
- Performance optimization
- Testing strategies (pytest, fixtures, mocking)

**Best Practices Enforced:**
- Uses `uv` for package management (not pip)
- Lazy logging: `logger.debug("val=%s", val)` not f-strings
- Type hints on all functions
- No magic strings/numbers
- Prefer `getattr()` with default over `hasattr()`

## Skills

### python-development

Python best practices and patterns reference.

**Covers:**
- Project structure
- Dependency management with uv
- Testing patterns
- Async programming
- Error handling
- Logging best practices
- Type annotations

## Example Usage

### Generate Tests

```bash
/test-gen
```

Claude will analyze your code and generate comprehensive pytest tests.

### Get Python Expertise

```
"Review this async implementation using the python-expert agent"
"Help me design a decorator for caching using python-expert patterns"
```

### Use Python Patterns

```
"Following python-development skill patterns, set up a new service module"
```

## Works Well With

- **core-productivity** - Git workflows and code review
- **security-suite** - Security vulnerability detection
- **api-development** - Building Python APIs
- **data-science** - Data engineering and ML pipelines
