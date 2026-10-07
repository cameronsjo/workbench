#!/usr/bin/env -S python3 -I -B
"""Fail unless every Claude Code mod in the catalog is pinned to one commit.

Usage: check-pins.py [<marketplace.json>]   (default: .claude-plugin/marketplace.json beside scripts/)

A mod is a plugin that runs its own code inside every Claude Code session, so
the catalog never follows a branch for one: each mod's entry names the exact
commit that was reviewed. The six mods are listed in MODS below. The list is a
copy of the roster in the cadence repository (`MODS` in `scripts/mods_lib.py`);
change both together.

For each of the six, the catalog must hold exactly one entry, and that entry
must be:

- keys `name`, `description` and `source`, and no others. A catalog entry can
  also carry a plugin's components (`hooks`, `commands`, `mcpServers` and so
  on); on a mod's entry those would add code the pin does not cover, so any
  other key fails.
- a `source` with exactly `source: git-subdir`, the cadence repository `url`,
  `path: plugins/<name>`, and a `sha` of 40 lowercase hex digits. A `ref` or
  any other key fails.

It also fails when any other entry reaches a mod: a name that matches one of
the six once letter case and compatibility characters are folded, or a source
whose path folds to `plugins/<mod>`.

Exit 0: all six are pinned. Exit 1: at least one problem, one per line.
Exit 2: the catalog could not be read.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import unicodedata

MODS = ("board", "verbs", "afk", "guard-toast", "herdr-bridge", "sploot")
CADENCE_URL = "https://github.com/cameronsjo/cadence.git"
ENTRY_KEYS = {"name", "description", "source"}
SOURCE_KEYS = {"source", "url", "path", "sha"}
SHA = re.compile(r"[0-9a-f]{40}")


def shown(text: object) -> str:
    """Text safe to print: control and non-ASCII characters escaped, so a name cannot hide in the log."""
    return str(text).encode("unicode_escape").decode("ascii")


def folded(text: str) -> str:
    """A name as a case-insensitive disk compares it, near enough."""
    return unicodedata.normalize("NFKC", text).casefold()


def reaches(entry: dict[str, object]) -> str | None:
    """The mod this entry reaches by name or by source path, or None."""
    name = entry.get("name")
    source = entry.get("source")
    path = source.get("path") if isinstance(source, dict) else None
    for mod in MODS:
        if isinstance(name, str) and folded(name) == mod:
            return mod
        if isinstance(path, str) and folded(path).strip("/").removeprefix("./") == f"plugins/{mod}":
            return mod
    return None


def entry_problems(mod: str, entry: dict[str, object]) -> list[str]:
    """Why one entry is not a valid pin of <mod>. Empty when it is."""
    problems: list[str] = []
    if entry.get("name") != mod:
        problems.append(f"{mod}: the entry is named {shown(entry.get('name'))!r}; name it {mod!r} exactly")
    extra = sorted(set(entry) - ENTRY_KEYS)
    if extra:
        problems.append(f"{mod}: the entry has {', '.join(shown(k) for k in extra)}; a mod's entry holds name, description and source only")
    source = entry.get("source")
    if not isinstance(source, dict):
        return [*problems, f"{mod}: the entry has no source object"]
    if set(source) != SOURCE_KEYS:
        problems.append(f"{mod}: source has keys {', '.join(sorted(shown(k) for k in source))}; it holds exactly source, url, path and sha")
    if source.get("source") != "git-subdir":
        problems.append(f"{mod}: source.source is {shown(source.get('source'))!r}, not 'git-subdir'")
    if source.get("url") != CADENCE_URL:
        problems.append(f"{mod}: source.url is {shown(source.get('url'))!r}, not {CADENCE_URL!r}")
    if source.get("path") != f"plugins/{mod}":
        problems.append(f"{mod}: source.path is {shown(source.get('path'))!r}, not 'plugins/{mod}'")
    sha = source.get("sha")
    if not isinstance(sha, str) or not SHA.fullmatch(sha):
        problems.append(f"{mod}: source.sha is {shown(sha)!r}, not 40 lowercase hex digits; a mod is pinned to one reviewed commit")
    return problems


def pin_problems(catalog: object) -> list[str]:
    """Every reason the catalog does not pin the six mods. Empty when it does."""
    plugins = catalog.get("plugins") if isinstance(catalog, dict) else None
    if not isinstance(plugins, list):
        return ["the catalog has no plugins list"]
    reached: dict[str, list[dict[str, object]]] = {mod: [] for mod in MODS}
    problems: list[str] = []
    for index, entry in enumerate(plugins):
        if not isinstance(entry, dict):
            problems.append(f"plugins[{index}] is not an object")
            continue
        mod = reaches(entry)
        if mod is not None:
            reached[mod].append(entry)
    for mod in MODS:
        entries = reached[mod]
        if len(entries) != 1:
            problems.append(f"{mod}: {len(entries)} catalog entries reach this mod by name or by path, expected 1")
        for entry in entries:
            problems += entry_problems(mod, entry)
    return problems


def main(argv: list[str]) -> int:
    if len(argv) > 1 or any(arg.startswith("-") for arg in argv):
        print(__doc__, file=sys.stderr)
        return 2
    path = pathlib.Path(argv[0]) if argv else pathlib.Path(__file__).resolve().parent.parent / ".claude-plugin" / "marketplace.json"
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        print(f"{shown(path)} could not be read as JSON: {shown(err)}", file=sys.stderr)
        return 2
    problems = pin_problems(catalog)
    for problem in problems:
        print(problem)
    if problems:
        print(f"FAIL  {len(problems)} problem(s): every mod is pinned to one reviewed commit, with nothing else on its entry")
        return 1
    print(f"PASS  {len(MODS)} of {len(MODS)} mods pinned by commit")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
