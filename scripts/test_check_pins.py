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


def entry(name: str, sha: str | None = SHA) -> dict[str, object]:
    source: dict[str, object] = {"source": "git-subdir", "url": pins.CADENCE_URL, "path": f"plugins/{name}"}
    if sha is not None:
        source["sha"] = sha
    return {"name": name, "description": f"{name} mod", "source": source}


def good() -> dict[str, object]:
    other = {"name": "cadence", "description": "not a mod", "source": {"source": "git-subdir", "url": pins.CADENCE_URL, "path": "plugins/cadence"}}
    return {"name": "workbench", "plugins": [other, *(entry(mod) for mod in pins.MODS)]}


class PinTest(unittest.TestCase):
    def problems(self, change) -> list[str]:  # noqa: ANN001 - a callable that edits the catalog in place
        catalog = copy.deepcopy(good())
        change(catalog["plugins"])
        return pins.pin_problems(catalog)

    def assert_one(self, change, text: str) -> None:  # noqa: ANN001
        found = self.problems(change)
        self.assertTrue(any(text in line for line in found), found)

    def test_six_pinned_entries_pass(self) -> None:
        self.assertEqual(pins.pin_problems(good()), [])

    def test_an_unpinned_plugin_that_is_not_a_mod_is_not_judged(self) -> None:
        self.assertEqual(self.problems(lambda p: p.append({"name": "x", "description": "", "source": "./x", "hooks": {}})), [])

    def test_a_missing_mod_fails(self) -> None:
        self.assert_one(lambda p: p.pop(1), "board: 0 catalog entries reach this mod")

    def test_a_mod_without_a_sha_fails(self) -> None:
        self.assert_one(lambda p: p[1]["source"].pop("sha"), "board: source has keys path, source, url")

    def test_a_sha_that_is_not_forty_lowercase_hex_fails(self) -> None:
        for bad in (SHA[:39], SHA.upper(), "main", SHA + "0", f" {SHA}", 7, None, ""):
            with self.subTest(sha=bad):
                self.assert_one(lambda p, bad=bad: p[1]["source"].__setitem__("sha", bad), "not 40 lowercase hex digits")

    def test_a_ref_beside_the_sha_fails(self) -> None:
        self.assert_one(lambda p: p[1]["source"].__setitem__("ref", "main"), "it holds exactly source, url, path and sha")

    def test_a_component_field_on_a_mods_entry_fails(self) -> None:
        for key in ("hooks", "commands", "agents", "skills", "mcpServers", "strict", "lspServers", "outputStyles"):
            with self.subTest(key=key):
                self.assert_one(lambda p, key=key: p[1].__setitem__(key, {}), f"board: the entry has {key}")

    def test_another_repository_fails(self) -> None:
        self.assert_one(lambda p: p[1]["source"].__setitem__("url", "https://github.com/evil/cadence.git"), "board: source.url is")

    def test_another_source_kind_fails(self) -> None:
        self.assert_one(lambda p: p[1]["source"].__setitem__("source", "github"), "board: source.source is 'github'")

    def test_a_source_that_is_a_string_fails(self) -> None:
        self.assert_one(lambda p: p[1].__setitem__("source", "./plugins/board"), "board: the entry has no source object")

    def test_a_second_entry_with_the_same_name_fails(self) -> None:
        self.assert_one(lambda p: p.append(entry("board", None)), "board: 2 catalog entries reach this mod")

    def test_a_second_entry_under_a_folded_name_fails(self) -> None:
        for name in ("Board", "BOARD", "ｂoard"):  # the last is a fullwidth b
            with self.subTest(name=name):
                found = self.problems(lambda p, name=name: p.append({"name": name, "description": "", "source": "./x"}))
                self.assertTrue(any("board: 2 catalog entries" in line for line in found), found)
                self.assertTrue(any("name it 'board' exactly" in line for line in found), found)

    def test_another_name_at_a_mods_path_fails(self) -> None:
        for path in ("plugins/board", "plugins/Board", "./plugins/board", "plugins/board/"):
            with self.subTest(path=path):
                twin = {"name": "notes", "description": "", "source": {"source": "git-subdir", "url": pins.CADENCE_URL, "path": path}}
                found = self.problems(lambda p, twin=twin: p.append(twin))
                self.assertTrue(any("board: 2 catalog entries" in line for line in found), found)

    def test_an_entry_that_is_not_an_object_fails(self) -> None:
        self.assert_one(lambda p: p.append("board"), "is not an object")

    def test_a_catalog_without_a_plugins_list_fails(self) -> None:
        self.assertEqual(pins.pin_problems({"plugins": {}}), ["the catalog has no plugins list"])
        self.assertEqual(pins.pin_problems([]), ["the catalog has no plugins list"])

    def test_the_roster_is_six(self) -> None:
        self.assertEqual(sorted(pins.MODS), ["afk", "board", "guard-toast", "herdr-bridge", "sploot", "verbs"])


class CommandTest(unittest.TestCase):
    def run_on(self, text: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "marketplace.json"
            path.write_text(text, encoding="utf-8")
            return subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), str(path)], capture_output=True, text=True, check=False)

    def test_pass_and_fail_exit_codes(self) -> None:
        ok = self.run_on(json.dumps(good()))
        self.assertEqual((ok.returncode, ok.stdout.strip()), (0, "PASS  6 of 6 mods pinned by commit"))
        catalog = good()
        catalog["plugins"][1]["source"].pop("sha")  # type: ignore[index]
        bad = self.run_on(json.dumps(catalog))
        self.assertEqual(bad.returncode, 1, bad.stdout)
        self.assertIn("FAIL  2 problem(s)", bad.stdout)

    def test_unreadable_json_is_exit_two(self) -> None:
        self.assertEqual(self.run_on("{").returncode, 2)

    def test_a_missing_file_and_a_flag_are_exit_two(self) -> None:
        for args in (["/nonexistent/marketplace.json"], ["--help"], ["a", "b"]):
            done = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), *args], capture_output=True, text=True, check=False)
            self.assertEqual(done.returncode, 2, args)

    def test_the_repository_catalog_passes(self) -> None:
        done = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT)], capture_output=True, text=True, check=False)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)


if __name__ == "__main__":
    unittest.main()
