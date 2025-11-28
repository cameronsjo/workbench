# Plugin Compositions

Pre-configured plugin bundles for common workflows and project types. Install all plugins in a composition with a single settings update.

## Quick Reference

| Composition | Best For | Plugins |
|-------------|----------|---------|
| [essentials](#essentials) | Every project | core-productivity, pr-workflow |
| [fullstack-ts](#fullstack-ts) | TypeScript/React apps | essentials + typescript-toolkit, api-development |
| [python-backend](#python-backend) | Python services/APIs | essentials + python-toolkit, api-development |
| [code-quality](#code-quality) | Reviews & security | essentials + security-suite |
| [writing](#writing) | Documentation | core-productivity, obsidian-pkm, research-tools |
| [cloud-native](#cloud-native) | DevOps/Infrastructure | essentials + cloud-ops, security-suite |
| [data-platform](#data-platform) | Data engineering/ML | essentials + python-toolkit, data-science |
| [mcp-builder](#mcp-builder) | MCP server development | essentials + mcp-development, typescript-toolkit |

## Compositions

### essentials

**The foundation for every project.** Start here.

```json
{
  "enabledPlugins": [
    "core-productivity@cameronsjo",
    "pr-workflow@cameronsjo"
  ]
}
```

**Includes:**

- `/commit`, `/ready`, `/check`, `/clean`, `/turbo` - workflow commands
- `/pr-review` - multi-perspective PR reviews
- `/setup-labels` - repository label management
- `code-reviewer` agent
- `sass`, `hype`, `roast` communication modes

---

### fullstack-ts

**Full-stack TypeScript/React development.** Next.js, React, Node APIs.

```json
{
  "enabledPlugins": [
    "core-productivity@cameronsjo",
    "pr-workflow@cameronsjo",
    "typescript-toolkit@cameronsjo",
    "api-development@cameronsjo"
  ]
}
```

**Adds:**

- `frontend-developer`, `typescript-expert` agents
- `nextjs-app-router-developer` agent
- `/api-review` command
- API design skills with OpenAPI patterns

---

### python-backend

**Python backend services and APIs.** FastAPI, Django, data processing.

```json
{
  "enabledPlugins": [
    "core-productivity@cameronsjo",
    "pr-workflow@cameronsjo",
    "python-toolkit@cameronsjo",
    "api-development@cameronsjo"
  ]
}
```

**Adds:**

- `python-expert` agent (uv, async, type hints)
- `/test-gen` command
- API design skills with REST patterns
- Backend architecture guidance

---

### code-quality

**Maximum code quality focus.** Security audits, thorough reviews.

```json
{
  "enabledPlugins": [
    "core-productivity@cameronsjo",
    "pr-workflow@cameronsjo",
    "security-suite@cameronsjo"
  ]
}
```

**Adds:**

- `security-auditor` agent
- `/security-review` command
- OWASP Top 10 checklist
- Secret detection patterns

---

### writing

**Documentation and knowledge management.** Technical writing, PKM, research.

```json
{
  "enabledPlugins": [
    "core-productivity@cameronsjo",
    "obsidian-pkm@cameronsjo",
    "research-tools@cameronsjo"
  ]
}
```

**Adds:**

- `obsidian-markdown` skill
- `remembering-conversations` skill
- `comprehensive-researcher` agent
- `academic-researcher` agent
- MOC generation, tag management

---

### cloud-native

**DevOps and infrastructure.** Kubernetes, Terraform, cloud platforms.

```json
{
  "enabledPlugins": [
    "core-productivity@cameronsjo",
    "pr-workflow@cameronsjo",
    "cloud-ops@cameronsjo",
    "security-suite@cameronsjo"
  ]
}
```

**Adds:**

- `cloud-architect` agent
- `devops-troubleshooter` agent
- `terraform-specialist` agent
- Infrastructure security patterns

---

### data-platform

**Data engineering and ML.** Pipelines, analytics, machine learning.

```json
{
  "enabledPlugins": [
    "core-productivity@cameronsjo",
    "pr-workflow@cameronsjo",
    "python-toolkit@cameronsjo",
    "data-science@cameronsjo"
  ]
}
```

**Adds:**

- `data-scientist` agent
- `data-engineer` agent
- `database-optimizer` agent
- SQL optimization, ETL patterns

---

### mcp-builder

**Building MCP servers.** Protocol implementation, testing, security.

```json
{
  "enabledPlugins": [
    "core-productivity@cameronsjo",
    "pr-workflow@cameronsjo",
    "mcp-development@cameronsjo",
    "typescript-toolkit@cameronsjo"
  ]
}
```

**Adds:**

- `mcp-expert` agent
- `mcp-server-architect` agent
- `mcp-testing-engineer` agent
- `mcp-security-auditor` agent
- MCP development skill with templates

---

## Custom Compositions

Mix and match plugins based on your needs:

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
    "python-toolkit@cameronsjo",
    "security-suite@cameronsjo",
    "research-tools@cameronsjo"
  ]
}
```

## Composition Philosophy

1. **Start with essentials** - Every project benefits from good git workflows and PR reviews
2. **Add language toolkit** - Python or TypeScript based on your stack
3. **Add domain plugins** - Security, cloud, data, etc. based on project needs
4. **Keep it minimal** - Don't install everything; more plugins = more context
