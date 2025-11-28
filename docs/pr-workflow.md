# PR Workflow Plugin

Multi-perspective pull request reviews and automation.

## Installation

```bash
/plugin install pr-workflow@cameronsjo
```

## Commands

### `/review.pr`

Conduct comprehensive PR review from multiple perspectives (PM, Developer, QA, Security).

**Usage:**
```bash
/review.pr
/review.pr 123          # Review PR #123
/review.pr https://...  # Review PR by URL
```

**Perspectives:**
- **PM**: Business impact, requirements, user experience
- **Developer**: Code quality, architecture, patterns
- **QA**: Test coverage, edge cases, regression risks
- **Security**: Vulnerabilities, auth, data exposure

### `/review.pr-fix`

Fix issues identified in a PR review manifest.

**Usage:**
```bash
/review.pr-fix 123
```

### `/setup-labels`

Setup PR review and issue labels for your repository.

**Usage:**
```bash
/setup-labels
```

Creates standard labels:
- `type:bug`, `type:feature`, `type:refactor`
- `priority:high`, `priority:medium`, `priority:low`
- `status:ready`, `status:wip`, `status:blocked`
- `review:approved`, `review:changes-requested`

## Example Usage

### Review a PR

```bash
# Review current branch's PR
/review.pr

# Review specific PR
/review.pr 42
```

### Setup Repository Labels

```bash
/setup-labels
```

### Fix PR Issues

```bash
# After /review.pr identifies issues
/review.pr-fix 42
```

## Works Well With

- **core-productivity** - `/ready` to create PRs
- **security-suite** - Security perspective in reviews
- **api-development** - API review perspective
