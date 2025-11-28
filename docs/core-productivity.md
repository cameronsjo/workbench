# Core Productivity Plugin

Essential productivity tools for every project. This is the foundation plugin that should be installed in all projects.

## Installation

```bash
/plugin install core-productivity@cameron-tools
```

## Commands

### `/commit`

Create well-formatted git commits with conventional commit messages.

**Usage:**
```bash
/commit
```

**Features:**
- Analyzes staged changes
- Generates conventional commit message
- Includes Co-Authored-By for AI attribution

### `/ready`

Commit changes logically, push, and create/update a PR with automated review trigger.

**Usage:**
```bash
/ready                    # Create PR
/ready --draft           # Create draft PR
/ready --open            # Open PR in browser after creation
```

### `/check`

Run project checks and fix any errors without committing.

**Usage:**
```bash
/check
```

**Features:**
- Runs linting, tests, type checking
- Attempts to fix issues automatically
- Reports remaining problems

### `/clean`

Fix all linting and formatting issues across the codebase.

**Usage:**
```bash
/clean
```

### `/turbo`

Maximum speed execution mode - parallelize everything, minimize hesitation.

**Usage:**
```bash
/turbo
```

### `/catchup`

Read all uncommitted changes back into context after `/clear`.

**Usage:**
```bash
/catchup
```

### `/context-prime`

Load project context by reading README.md and exploring relevant project files.

**Usage:**
```bash
/context-prime
```

### `/explore`

Launch Explore agent for codebase investigation.

**Usage:**
```bash
/explore
```

## Agents

### code-reviewer

Expert code review specialist that proactively reviews code for quality, security, and maintainability.

**Capabilities:**
- Code quality assessment
- Security vulnerability detection
- Performance analysis
- Best practices recommendations
- Maintainability scoring

**When to use:**
- After writing significant code
- Before committing changes
- During pull request reviews

## Skills

### prompt-engineering

Effective LLM prompt design patterns for building AI features.

### skill-builder

Create and optimize Claude Skills with proper structure and progressive disclosure.

### roadmap

Product roadmap management and planning patterns.

## Workflow Example

```bash
# 1. Load project context
/context-prime

# 2. Make your changes...

# 3. Check for issues
/check

# 4. Fix formatting
/clean

# 5. Commit with good message
/commit

# 6. Create PR when ready
/ready
```

## Works Well With

- **python-toolkit** - Python-specific development
- **typescript-toolkit** - TypeScript/React development
- **security-suite** - Security auditing
- **pr-workflow** - Enhanced PR reviews
