#!/usr/bin/env -S python3 -I -B
"""Tests for check-pins.py. Run: python3 -I -B scripts/test_check_pins.py"""

from __future__ import annotations

import copy
import json
import pathlib
import subprocess
import sys
import tempfile
import types
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = HERE / "check-pins.py"


def load() -> types.ModuleType:
    module = types.ModuleType("check_pins")
    exec(compile(SCRIPT.read_text(encoding="utf-8"), str(SCRIPT), "exec"), module.__dict__)  # noqa: S102 - the script under test
    return module


pins = load()
SHA = "0123456789abcdef0123456789abcdef01234567"
PLAIN = len(pins.MODS)  # index of the cadence entry that is not a mod
ALONE = PLAIN + 1  # index of the standalone entry


def cadence(name: str, sha: str | None = None) -> dict[str, object]:
    source: dict[str, object] = {"source": "git-subdir", "url": pins.CADENCE_URL, "path": f"plugins/{name}"}
    if sha is not None:
        source["sha"] = sha
    return {"name": name, "description": f"{name} plugin", "source": source}


def good() -> dict[str, object]:
    alone = {"name": "homelab", "description": "standalone", "source": {"source": "url", "url": "https://github.com/cameronsjo/homelab.git"}}
    return {"name": "workbench", "description": "d", "owner": {"name": "o"}, "plugins": [*(cadence(mod, SHA) for mod in pins.MODS), cadence("cadence"), alone]}


def problems(change) -> list[str]:  # noqa: ANN001 - a callable that edits the catalog in place
    catalog = copy.deepcopy(good())
    change(catalog)
    return pins.catalog_problems(catalog)


class CatalogTest(unittest.TestCase):
    def assert_one(self, change, text: str) -> None:  # noqa: ANN001
        found = problems(change)
        self.assertTrue(any(text in line for line in found), found)

    def test_the_fixture_passes(self) -> None:
        self.assertEqual(pins.catalog_problems(good()), [])

    def test_the_allowlists_are_exactly_these(self) -> None:
        # Widening any of these is the change a reviewer must see; a list of refused keys would not notice one more allowed.
        self.assertEqual(pins.TOP_KEYS, {"name", "description", "owner", "plugins"})
        self.assertEqual(pins.ENTRY_KEYS, {"name", "description", "source"})
        self.assertEqual(pins.CADENCE_KEYS, {"source", "url", "path"})
        self.assertEqual(pins.STANDALONE_KEYS, {"source", "url"})
        self.assertEqual(pins.OPTIONAL_KEYS, {"ref", "sha"})
        self.assertEqual(pins.PINNED_KEYS, {"source", "url", "path", "sha"})
        self.assertEqual(sorted(pins.MODS), ["afk", "board", "guard-toast", "herdr-bridge", "sploot", "verbs"])
        self.assertEqual((pins.OWNER, pins.CADENCE_URL), ("cameronsjo", "https://github.com/cameronsjo/cadence.git"))

    def test_a_top_level_key_outside_the_list_fails(self) -> None:
        for key in ("renames", "allowCrossMarketplaceDependenciesOn", "metadata", "forceRemoveDeletedPlugins"):
            with self.subTest(key=key):
                self.assert_one(lambda c, key=key: c.__setitem__(key, {}), f"the catalog has top-level {key}")

    def test_an_entry_key_outside_the_list_fails_on_any_entry(self) -> None:
        for index in (0, PLAIN, ALONE):
            for key in ("hooks", "commands", "agents", "skills", "mcpServers", "strict", "dependencies", "version", "userConfig"):
                with self.subTest(index=index, key=key):
                    self.assert_one(lambda c, index=index, key=key: c["plugins"][index].__setitem__(key, {}), "an entry holds description, name, source only")

    def test_an_entry_without_a_description_fails(self) -> None:
        self.assert_one(lambda c: c["plugins"][PLAIN].pop("description"), "an entry holds description, name, source only")

    def test_a_catalog_without_a_plugins_list_fails(self) -> None:
        for bad in ({"plugins": {}}, [], {"name": "x"}, None):
            with self.subTest(bad=bad):
                self.assertEqual(pins.catalog_problems(bad), ["the catalog has no plugins list"])

    def test_an_entry_that_is_not_an_object_fails(self) -> None:
        self.assert_one(lambda c: c["plugins"].append("board"), "is not an object")

    def test_a_name_that_is_not_plain_lowercase_fails(self) -> None:
        for name in ("Notes", "notes.", "no tes", "ｎotes", "", "-notes", "notes/x", 7, None):
            with self.subTest(name=name):
                self.assert_one(lambda c, name=name: c["plugins"].append({"name": name, "description": "", "source": {"source": "url", "url": "https://github.com/cameronsjo/x.git"}}), "not lowercase letters, digits and hyphens")

    def test_a_second_entry_with_a_name_fails(self) -> None:
        self.assert_one(lambda c: c["plugins"].append(cadence("cadence")), "cadence: 2 or more entries have this name")

    def test_a_string_source_fails(self) -> None:
        self.assert_one(lambda c: c["plugins"][PLAIN].__setitem__("source", "./plugins/cadence"), "not an object")

    def test_a_source_of_another_kind_or_place_fails(self) -> None:
        sources = (
            {"source": "github", "repo": "cameronsjo/cadence"},
            {"source": "url", "url": pins.CADENCE_URL},  # the whole cadence repository
            {"source": "url", "url": "https://github.com/cameronsjo/Cadence.git"},
            {"source": "url", "url": "https://github.com/evil/homelab.git"},
            {"source": "url", "url": "https://github.com/cameronsjo/homelab"},
            {"source": "url", "url": "git@github.com:cameronsjo/homelab.git"},
            {"source": "url", "url": "https://github.com/cameronsjo/homelab.git/../../evil/x.git"},
            {"source": "git-subdir", "url": "https://github.com/evil/cadence.git", "path": "plugins/notes"},
            {"source": "git-subdir", "url": "https://github.com/cameronsjo/cadence", "path": "plugins/notes"},
            {"source": "git-subdir", "url": "https://github.com/cameronsjo/homelab.git", "path": "plugins/notes"},
            {"source": "npm", "package": "x"},
            {},
        )
        for source in sources:
            with self.subTest(source=source):
                self.assert_one(lambda c, source=source: c["plugins"].append({"name": "notes", "description": "", "source": source}), "notes: source (")

    def test_a_cadence_path_is_the_entrys_own_directory_spelled_one_way(self) -> None:
        # Each of these reaches plugins/board under another name, unpinned.
        for path in ("plugins/board", "plugins//board", "plugins/./board", "./plugins/board", "plugins/board/", "plugins/board/.", "plugins\\board", "plugins/afk/../board", "plugins/Board", "plugins/notes/../board", "notes", "x/notes", "plugins//notes", "plugins/board/../notes", "", None, 7):
            with self.subTest(path=path):
                self.assert_one(lambda c, path=path: c["plugins"].append({"name": "notes", "description": "", "source": {"source": "git-subdir", "url": pins.CADENCE_URL, "path": path}}), "notes: source.path is")

    def test_a_source_key_outside_its_shape_fails(self) -> None:
        self.assert_one(lambda c: c["plugins"][PLAIN]["source"].__setitem__("subdir", "x"), "cadence: a cadence source holds")
        self.assert_one(lambda c: c["plugins"][ALONE]["source"].__setitem__("path", "plugins/board"), "homelab: a standalone source holds")
        self.assert_one(lambda c: c["plugins"][PLAIN]["source"].pop("path"), "cadence: source.path is 'None'")

    def test_ref_and_sha_are_allowed_off_a_mod(self) -> None:
        for index in (PLAIN, ALONE):
            self.assertEqual(problems(lambda c, index=index: c["plugins"][index]["source"].update(ref="main", sha=SHA)), [])


class ModTest(unittest.TestCase):
    """Every case runs for each of the six: a check that judged one mod would pass a test that broke only that one."""

    def each(self, change, text: str) -> None:  # noqa: ANN001 - change(catalog, index)
        for index, mod in enumerate(pins.MODS):
            with self.subTest(mod=mod):
                found = problems(lambda c, index=index: change(c, index))
                self.assertTrue(any(line.startswith(f"{mod}: ") and text in line for line in found), found)

    def test_a_missing_mod_fails(self) -> None:
        self.each(lambda c, i: c["plugins"].pop(i), "no catalog entry has this name")

    def test_a_mod_without_a_sha_fails(self) -> None:
        self.each(lambda c, i: c["plugins"][i]["source"].pop("sha"), "a mod's source holds exactly path, sha, source, url")

    def test_a_sha_that_is_not_forty_lowercase_hex_fails(self) -> None:
        for bad in (SHA[:39], SHA.upper(), "main", SHA + "0", f" {SHA}", f"{SHA}\n", 7, None, ""):
            with self.subTest(sha=bad):
                self.each(lambda c, i, bad=bad: c["plugins"][i]["source"].__setitem__("sha", bad), "not 40 lowercase hex digits")

    def test_a_ref_beside_the_sha_fails(self) -> None:
        self.each(lambda c, i: c["plugins"][i]["source"].__setitem__("ref", "main"), "a mod's source holds exactly")

    def test_a_mod_at_another_path_fails(self) -> None:
        self.each(lambda c, i: c["plugins"][i]["source"].__setitem__("path", "plugins/cadence"), "source.path is 'plugins/cadence'")

    def test_a_mod_from_a_standalone_repository_fails(self) -> None:
        self.each(lambda c, i: c["plugins"][i].__setitem__("source", {"source": "url", "url": "https://github.com/cameronsjo/homelab.git", "sha": SHA}), "a mod is a git-subdir source in the cadence repository")

    def test_a_mod_named_in_another_case_fails_and_is_not_counted_missing_silently(self) -> None:
        for index, mod in enumerate(pins.MODS):
            with self.subTest(mod=mod):
                found = problems(lambda c, index=index, mod=mod: c["plugins"][index].__setitem__("name", mod.upper()))
                self.assertTrue(any(f"name it {mod!r} exactly" in line for line in found), found)

    def test_a_component_field_on_a_mod_fails(self) -> None:
        self.each(lambda c, i: c["plugins"][i].__setitem__("hooks", {}), "an entry holds description, name, source only")


class TwinTest(unittest.TestCase):
    CATALOG = ".claude-plugin/marketplace.json"

    def test_distinct_paths_pass(self) -> None:
        self.assertEqual(pins.twin_problems([self.CATALOG, "scripts/check-pins.py", "README.md", "docs/a.md", "docs/b.md"]), [])

    def test_a_folded_twin_of_the_catalog_or_the_rule_fails(self) -> None:
        for twin in (".claude-plugin/marketplace.j\u017fon", ".claude-plugin/mar\u212aetplace.json", ".claude-plugin/Marketplace.json", ".Claude-Plugin/x", "\u017fcripts/check-pins.py", "scripts/Check-Pins.py", ".claude-plugin/\u1fb3\u0323", "docs/\u03aa\u0301"):
            with self.subTest(twin=twin):
                base = [self.CATALOG, "scripts/check-pins.py", ".claude-plugin/\u03b1\u0323\u0345", "docs/\u0390"]
                self.assertEqual(len(pins.twin_problems([*base, twin])), 1, twin)

    def test_twin_directories_are_named_once(self) -> None:
        self.assertEqual(pins.twin_problems(["docs/a.md", "Docs/a.md"]), ["Docs and docs are one path on a disk that ignores letter case or folds characters; keep one"])

    def test_a_name_holding_a_folding_slash_does_not_hide_a_twin(self) -> None:
        found = pins.twin_problems([self.CATALOG, ".claude-plugin/Marketplace.json", ".claude-plugin\uff0fmarketplace.json"])
        self.assertEqual(len(found), 1, found)
        self.assertIn(".claude-plugin/Marketplace.json and .claude-plugin/marketplace.json", found[0])


class CommandTest(unittest.TestCase):
    def test_a_paths_file_is_judged_and_must_be_the_catalogs_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            catalog = pathlib.Path(tmp) / "m.json"
            catalog.write_text(json.dumps(good()), encoding="utf-8")
            listing = pathlib.Path(tmp) / "paths"
            cases = (
                ([".claude-plugin/marketplace.json", "README.md"], 0, "PASS"),
                ([".claude-plugin/marketplace.json", ".claude-plugin/marketplace.j\u017fon"], 1, "are one path on a disk"),
                (["README.md"], 1, "does not list .claude-plugin/marketplace.json"),
                ([], 1, "does not list .claude-plugin/marketplace.json"),
            )
            for paths, code, text in cases:
                with self.subTest(paths=paths):
                    listing.write_bytes(b"".join(p.encode("utf-8") + b"\0" for p in paths))
                    done = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), str(catalog), str(listing)], capture_output=True, text=True, check=False)
                    self.assertEqual(done.returncode, code, done.stdout + done.stderr)
                    self.assertIn(text, done.stdout)
            missing = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), str(catalog), str(listing) + ".none"], capture_output=True, text=True, check=False)
            self.assertEqual(missing.returncode, 2)

    def run_on(self, text: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "marketplace.json"
            path.write_text(text, encoding="utf-8")
            return subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), str(path)], capture_output=True, text=True, check=False)

    def test_pass_and_fail_exit_codes(self) -> None:
        ok = self.run_on(json.dumps(good()))
        self.assertEqual((ok.returncode, ok.stdout.strip()), (0, "PASS  8 entries in known shapes; 6 of 6 mods pinned by commit"))
        catalog = good()
        catalog["plugins"][0]["source"].pop("sha")  # type: ignore[index]
        bad = self.run_on(json.dumps(catalog))
        self.assertEqual(bad.returncode, 1, bad.stdout)
        self.assertIn("FAIL  2 problem(s)", bad.stdout)

    def test_unreadable_json_is_exit_two(self) -> None:
        for text in ("{", '{"plugins": [], "x": NaN}', ""):
            with self.subTest(text=text):
                self.assertEqual(self.run_on(text).returncode, 2)

    def test_a_missing_file_and_a_flag_are_exit_two(self) -> None:
        for args in (["/nonexistent/marketplace.json"], ["--help"], ["a", "b", "c"]):
            done = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), *args], capture_output=True, text=True, check=False)
            self.assertEqual(done.returncode, 2, args)

    def test_the_repository_catalog_passes_with_all_six(self) -> None:
        done = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT)], capture_output=True, text=True, check=False)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        catalog = json.loads((HERE.parent / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        pinned = {e["name"]: e["source"].get("sha") for e in catalog["plugins"] if e["name"] in pins.MODS}
        self.assertEqual(sorted(pinned), sorted(pins.MODS))
        self.assertTrue(all(isinstance(sha, str) and len(sha) == 40 for sha in pinned.values()), pinned)


if __name__ == "__main__":
    unittest.main()
