---
description: Suggest roadmap items (returns JSON, doesn't write)
category: roadmap
argument-hint: <item description>
---

# Suggest Roadmap Item

Analyze and return a structured roadmap suggestion WITHOUT writing to files. Use this when running as a subagent or when multiple agents might suggest items concurrently.

## Arguments

$ARGUMENTS - The item to suggest (e.g., "AVIF image support" or "better error messages")

## Instructions

1. Parse the item description from $ARGUMENTS
2. Determine the best category:
   - Performance (speed, rendering, caching)
   - Features (new functionality)
   - Technical Debt (cleanup, refactoring)
   - UX Improvements (user experience)
   - Infrastructure (devops, monitoring)
   - Security (vulnerabilities, hardening, access control)

3. Estimate Impact and Effort:
   - **Impact**: high / medium / low
   - **Effort**: small (< 1 day) / medium (1-3 days) / large (> 3 days)

4. Return a JSON object (do NOT write to any files):

```json
{
  "item": "Short item name",
  "category": "Features",
  "status": "idea",
  "impact": "High",
  "effort": "Medium",
  "details": "Brief description of what this enables"
}
```

## When to Use

- Running as a Task/subagent
- Multiple agents analyzing concurrently
- Parent will batch-write all suggestions

The parent agent should collect all suggestions and write them to `docs/ROADMAP.md` in a single operation.

## Example

Input: `/roadmap.suggest SSRF protection for the fetch tool`

Output:
```json
{
  "item": "SSRF protection for fetch tool",
  "category": "Security",
  "status": "idea",
  "impact": "High",
  "effort": "Medium",
  "details": "URL allowlist/blocklist, private IP blocking, domain restrictions"
}
```
