# Claude Code Marketplace

Personal Claude Code plugin marketplace - a curated collection of agents, commands, and skills for software development.

## Quick Start

```bash
# Add marketplace
/plugin marketplace add cameron/claude-marketplace

# Browse available plugins
/plugin

# Install a plugin
/plugin install core-productivity@cameron-tools
```

## Available Plugins

| Plugin | Description | Components |
|--------|-------------|------------|
| **core-productivity** | Git workflows, code review, project checks | 8 commands, 1 agent |
| **python-toolkit** | Python development with uv, async, testing | 1 command, 1 agent, 1 skill |
| **typescript-toolkit** | TypeScript/React/Next.js patterns | 5 agents |
| **api-development** | REST API design, OpenAPI, architecture | 2 commands, 3 agents, 1 skill |
| **security-suite** | OWASP, vulnerability scanning, auth | 1 command, 2 agents, 2 skills |
| **pr-workflow** | Multi-perspective PR reviews, labels | 3 commands |
| **research-tools** | Comprehensive research, academic sources | 4 agents |
| **obsidian-pkm** | Obsidian markdown, MOCs, tags, linking | 3 agents, 1 skill |
| **mcp-development** | MCP server architecture, testing, security | 6 agents, 1 skill |
| **dx-tools** | Debugging, optimization, prompts | 2 commands, 4 agents, 2 skills |
| **cloud-ops** | AWS/Azure/GCP, Kubernetes, Terraform | 5 agents |
| **data-science** | SQL, ML pipelines, data engineering | 7 agents |

## Installation

### Add the Marketplace

```bash
/plugin marketplace add cameron/claude-marketplace
```

### Install Plugins

Install plugins based on your project needs:

```bash
# Essential for every project
/plugin install core-productivity@cameron-tools

# For Python projects
/plugin install python-toolkit@cameron-tools

# For TypeScript/React projects
/plugin install typescript-toolkit@cameron-tools

# For API development
/plugin install api-development@cameron-tools
```

### Project Configuration

Configure auto-installation in your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "cameron-tools": {
      "source": {
        "source": "github",
        "repo": "cameron/claude-marketplace"
      }
    }
  },
  "enabledPlugins": [
    "core-productivity@cameron-tools",
    "python-toolkit@cameron-tools"
  ]
}
```

## Plugin Details

### core-productivity

Essential productivity tools for every project.

**Commands:**
- `/commit` - Well-formatted git commits with conventional messages
- `/ready` - Commit, push, and create PR with automated review
- `/check` - Run project checks and fix errors
- `/clean` - Fix linting and formatting issues
- `/turbo` - Maximum speed execution mode
- `/catchup` - Read uncommitted changes after /clear
- `/context-prime` - Load project context from README
- `/explore` - Launch codebase investigation agent

**Agents:**
- `code-reviewer` - Expert code review for quality, security, maintainability

### python-toolkit

Python development expertise.

**Commands:**
- `/test-gen` - Generate comprehensive tests

**Agents:**
- `python-expert` - Advanced Python patterns, async, decorators, testing

**Skills:**
- `python-development` - Python best practices and patterns

### api-development

API design and architecture tools.

**Commands:**
- `/review.api` - Review API design for REST best practices
- `/review.architecture` - Review system architecture

**Agents:**
- `api-documenter` - OpenAPI specs, SDK generation, documentation
- `backend-architect` - RESTful APIs, microservices, database schemas
- `graphql-architect` - GraphQL schemas, resolvers, federation

**Skills:**
- `api-design` - REST API design guidelines and patterns

### security-suite

Security auditing and review tools.

**Commands:**
- `/review.security` - Comprehensive security audit

**Agents:**
- `security-auditor` - OWASP compliance, vulnerability detection
- `api-security-audit` - API-specific security review

**Skills:**
- `security-review` - Security review checklists and patterns
- `security-principles` - Core security principles

### pr-workflow

Pull request automation.

**Commands:**
- `/review.pr` - Multi-perspective PR review (PM, Dev, QA, Security)
- `/review.pr-fix` - Fix issues from PR review
- `/setup-labels` - Setup PR review labels

## Contributing

1. Fork this repository
2. Add or modify plugins in `plugins/`
3. Update `marketplace.json`
4. Submit a pull request

## License

MIT
