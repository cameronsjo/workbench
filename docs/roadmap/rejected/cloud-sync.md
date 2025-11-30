# Cloud Sync

> Rejected - Git handles this.

## Request

Users asked for built-in syncing of plugins across machines. "Install once, available everywhere."

## Decision

**Won't implement.**

## Reasoning

Git already solves this problem:
1. The marketplace is a git repo
2. Clone it on any machine
3. Symlinks work cross-platform (with minor caveats on Windows)

Adding cloud sync would:
- Introduce account/auth complexity
- Require a backend service
- Duplicate functionality git provides for free
- Add security surface area

## Alternatives

For users who want sync:

1. **Git** - Clone the repo on each machine
2. **Dotfiles repo** - Include marketplace as a submodule
3. **chezmoi/stow** - Dotfile managers that handle symlinks

## Related Issues

Common variations of this request:
- "Sync plugins across devices"
- "Cloud backup for my customizations"
- "Share my setup with my team"

All solved by git.
