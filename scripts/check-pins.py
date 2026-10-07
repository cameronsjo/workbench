#!/usr/bin/env -S python3 -I -B
"""Fail unless the catalog holds only known source shapes and every Claude Code mod is pinned to one commit.

Usage: check-pins.py [<marketplace.json>]   (default: .claude-plugin/marketplace.json beside scripts/)

A mod is a plugin that runs its own code inside every Claude Code session, so
the catalog never follows a branch for one: each mod's entry names one exact
commit. The six mods are listed in MODS below. The list is a copy of the roster
in the cadence repository; change both together.

The catalog cannot tell a mod from any other plugin (that is decided by files
inside the plugin), so the rule is an allowlist over the whole file. Anything
it does not list fails, and widening it is a change to this script:

- Top level: `name`, `description`, `owner`, `plugins`, and no other key. A
  key such as `renames` can move an installed plugin to another entry.
- Every entry: `name`, `description`, `source`, and no other key. An entry can
  also carry components (`hooks`, `commands`, `mcpServers`) or `dependencies`;
  those add code, or install another entry, from the catalog itself.
- Every name is unique once letter case, compatibility characters and trailing
  dots are folded.
- Every `source` is one of two shapes:
  - cadence: `source: git-subdir`, the cadence `url`, and `path: plugins/<name>`
    where <name> is the entry's own name, spelled exactly so. One spelling per
    directory means no second entry can reach a plugin under another name.
    Optional `ref` and `sha`.
  - standalone: `source: url` and `url: https://github.com/<owner>/<repo>.git`
    for the owner in OWNER, never the cadence repository itself. Optional
    `ref` and `sha`.
- Each of the six mods has an entry, and its source holds exactly `source`,
  `url`, `path` and a `sha` of 40 lowercase hex digits. No `ref`.

What this cannot see: whether a `sha` names a commit that was reviewed, and
whether a standalone repository ships a mod of its own.

Exit 0: the catalog passes. Exit 1: at least one problem, one per line.
Exit 2: the catalog could not be read.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import unicodedata

MODS = ("board", "verbs", "afk", "guard-toast", "herdr-bridge", "sploot")
OWNER = "cameronsjo"
CADENCE_URL = f"https://github.com/{OWNER}/cadence.git"
TOP_KEYS = frozenset({"name", "description", "owner", "plugins"})
ENTRY_KEYS = frozenset({"name", "description", "source"})
CADENCE_KEYS = frozenset({"source", "url", "path"})
STANDALONE_KEYS = frozenset({"source", "url"})
OPTIONAL_KEYS = frozenset({"ref", "sha"})
PINNED_KEYS = frozenset({"source", "url", "path", "sha"})
NAME = re.compile(r"[a-z0-9][a-z0-9-]*")
STANDALONE_URL = re.compile(rf"https://github\.com/{OWNER}/[A-Za-z0-9][A-Za-z0-9._-]*\.git")
SHA = re.compile(r"[0-9a-f]{40}")


def shown(text: object) -> str:
    """Text safe to print: control and non-ASCII characters escaped, so a name cannot hide in the log."""
    return str(text).encode("unicode_escape").decode("ascii")


def keys(found: object) -> str:
    return ", ".join(sorted(shown(k) for k in found))  # type: ignore[attr-defined]  # callers pass a collection of keys


def folded(text: str) -> str:
    """A name as a case-insensitive disk compares it, near enough. A trailing dot is dropped as Windows drops it."""
    once = unicodedata.normalize("NFKC", text.casefold())
    return unicodedata.normalize("NFKC", once.casefold()).rstrip(".")


def source_problems(name: str, source: object) -> list[str]:
    """Why one entry's source is neither allowed shape. Empty when it is one."""
    if not isinstance(source, dict):
        return [f"{name}: source is {shown(source)!r}, not an object; a path inside this registry is not a source it serves"]
    kind, url = source.get("source"), source.get("url")
    if kind == "git-subdir" and url == CADENCE_URL:
        required, what = CADENCE_KEYS, "a cadence source"
        want = f"plugins/{name}"
        problems = [] if source.get("path") == want else [f"{name}: source.path is {shown(source.get('path'))!r}, not {want!r}; a cadence entry is named for its directory and spells the path one way"]
    elif kind == "url" and isinstance(url, str) and STANDALONE_URL.fullmatch(url) and folded(url) != folded(CADENCE_URL):
        required, what, problems = STANDALONE_KEYS, "a standalone source", []
    else:
        return [f"{name}: source ({shown(kind)!r}, {shown(url)!r}) is neither git-subdir at {CADENCE_URL} nor url at https://github.com/{OWNER}/<repo>.git"]
    missing, extra = required - set(source), set(source) - required - OPTIONAL_KEYS
    if missing or extra:
        problems.append(f"{name}: {what} holds {keys(required)}, and optionally {keys(OPTIONAL_KEYS)}; this one has {keys(source)}")
    return problems


def pin_problems(name: str, source: object) -> list[str]:
    """Why a mod's source is not pinned. Empty when it is. The shape is judged by source_problems."""
    if not isinstance(source, dict):
        return []
    problems: list[str] = []
    if source.get("source") != "git-subdir":
        problems.append(f"{name}: a mod is a git-subdir source in the cadence repository, not {shown(source.get('source'))!r}")
    if set(source) != PINNED_KEYS:
        problems.append(f"{name}: a mod's source holds exactly {keys(PINNED_KEYS)}; this one has {keys(source)}")
    sha = source.get("sha")
    if not isinstance(sha, str) or not SHA.fullmatch(sha):
        problems.append(f"{name}: source.sha is {shown(sha)!r}, not 40 lowercase hex digits; a mod is pinned to one commit")
    return problems


def catalog_problems(catalog: object) -> list[str]:
    """Every reason the catalog fails the rule in this file's docstring. Empty when it passes."""
    if not isinstance(catalog, dict) or not isinstance(catalog.get("plugins"), list):
        return ["the catalog has no plugins list"]
    problems: list[str] = []
    extra = set(catalog) - TOP_KEYS
    if extra:
        problems.append(f"the catalog has top-level {keys(extra)}; it holds {keys(TOP_KEYS)} only")
    seen: dict[str, str] = {}
    for index, entry in enumerate(catalog["plugins"]):
        if not isinstance(entry, dict):
            problems.append(f"plugins[{index}] is not an object")
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not NAME.fullmatch(name):
            problems.append(f"plugins[{index}]: name is {shown(name)!r}, not lowercase letters, digits and hyphens")
            if isinstance(name, str) and folded(name) in MODS:
                seen.setdefault(folded(name), name)
                problems.append(f"{folded(name)}: the entry is named {shown(name)!r}; name it {folded(name)!r} exactly")
            continue
        if name in seen:
            problems.append(f"{name}: 2 or more entries have this name")
        seen[name] = name
        if set(entry) != ENTRY_KEYS:
            problems.append(f"{name}: the entry has {keys(entry)}; an entry holds {keys(ENTRY_KEYS)} only")
        problems += source_problems(name, entry.get("source"))
        if name in MODS:
            problems += pin_problems(name, entry.get("source"))
    problems += [f"{mod}: no catalog entry has this name; every mod is listed and pinned" for mod in MODS if mod not in seen]
    return problems


def main(argv: list[str]) -> int:
    if len(argv) > 1 or any(arg.startswith("-") for arg in argv):
        print(__doc__, file=sys.stderr)
        return 2
    path = pathlib.Path(argv[0]) if argv else pathlib.Path(__file__).resolve().parent.parent / ".claude-plugin" / "marketplace.json"
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"), parse_constant=lambda word: (_ for _ in ()).throw(ValueError(f"{word} is not JSON")))
    except (OSError, ValueError) as err:
        print(f"{shown(path)} could not be read as JSON: {shown(err)}", file=sys.stderr)
        return 2
    problems = catalog_problems(catalog)
    for problem in problems:
        print(problem)
    if problems:
        print(f"FAIL  {len(problems)} problem(s): the catalog holds known source shapes only, and every mod is pinned to one commit")
        return 1
    count = len(catalog["plugins"])
    print(f"PASS  {count} entries in known shapes; {len(MODS)} of {len(MODS)} mods pinned by commit")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
