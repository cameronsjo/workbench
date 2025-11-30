---
description: Create detailed spec for roadmap item
category: roadmap
argument-hint: <item name>
---

# Create Roadmap Spec

Create a detailed specification for a roadmap item.

## Arguments

$ARGUMENTS - The item to spec out (e.g., "thumbnail generation" or "keyboard shortcuts")

## Instructions

1. Find the item in `docs/ROADMAP.md` (or create if it doesn't exist)

2. Create a new file `docs/roadmap/{kebab-case-name}.md` using this structure:

```markdown
# Feature: [Title]

> One-line summary of what this enables.

## Status

- **Status**: planned
- **Priority**: [from roadmap table]
- **Effort**: [from roadmap table]

## Problem

What problem does this solve? Why does it matter?

## Proposed Solution

High-level approach. Include diagrams if helpful.

## Implementation Details

### Backend Changes

- Database schema changes
- API endpoints
- Services/logic

### Frontend Changes

- Components
- State management
- UI/UX

## Alternatives Considered

What else did we think about? Why not those?

## Open Questions

- [ ] Question 1?
- [ ] Question 2?

## References

- Related docs
- External resources
```

3. Update the ROADMAP.md table to link to the new file:
   ```
   | Item | `planned` | High | Medium | [item.md](roadmap/item.md) |
   ```

4. Discuss the implementation with the user to fill in details
