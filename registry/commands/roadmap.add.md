---
description: Add item to project roadmap
category: roadmap
argument-hint: <item description>
---

# Add Roadmap Item

Add a new item to the project roadmap.

## Arguments

$ARGUMENTS - The item to add (e.g., "AVIF image support" or "better error messages")

## Instructions

1. Parse the item description from $ARGUMENTS
2. Determine the best category:
   - Performance (speed, rendering, caching)
   - Features (new functionality)
   - Technical Debt (cleanup, refactoring)
   - UX Improvements (user experience)
   - Infrastructure (devops, monitoring)
   - Security (vulnerabilities, hardening, access control)

3. Determine Impact and Effort:
   - If explicitly provided in $ARGUMENTS, use those values
   - Otherwise, estimate based on your analysis:
     - **Impact**: high (core functionality, security, frequently used) / medium (nice to have, occasional use) / low (edge case, cosmetic)
     - **Effort**: small (< 1 day, simple change) / medium (1-3 days, design decisions needed) / large (> 3 days, significant work)
   - Only ask the user if you're running interactively AND genuinely uncertain

4. Add a row to the appropriate table in `docs/ROADMAP.md`:
   ```
   | [Item name] | `idea` | [Impact] | [Effort] | [Details or brief description] |
   ```

5. If effort is medium or large AND running interactively, offer to create a detail spec file

## Concurrency Warning

If multiple agents may write to the roadmap simultaneously, collect items and add them in a single batch at the end of analysis rather than one at a time. This prevents race conditions.

## Example

Input: `/roadmap.add AVIF image support for better compression`

Output: Added to Performance table:
```
| AVIF image support | `idea` | Medium | Small | 50% smaller than WebP |
```
