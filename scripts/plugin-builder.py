#!/usr/bin/env python3
"""
Plugin Builder CLI

Interactive tool for managing Claude Code marketplace plugins.
Manages a central registry of commands, agents, and skills,
and creates plugins by symlinking from the registry.

Usage:
    python scripts/plugin-builder.py [command]

Commands:
    list            List all assets in registry
    list-plugins    List all plugins and their assets
    add             Add a new asset to registry
    create          Create a new plugin
    edit            Edit a plugin (add/remove assets)
    build           Build/rebuild plugin symlinks
    validate        Validate all plugins and symlinks
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


class AssetType(Enum):
    """Types of assets in the registry."""
    COMMAND = "commands"
    AGENT = "agents"
    SKILL = "skills"


@dataclass
class Asset:
    """Represents an asset in the registry."""
    name: str
    asset_type: AssetType
    path: Path
    description: str = ""

    @property
    def registry_path(self) -> Path:
        """Path within registry."""
        return Path("registry") / self.asset_type.value / self.name


@dataclass
class Plugin:
    """Represents a plugin definition."""
    name: str
    description: str = ""
    version: str = "1.0.0"
    commands: list[str] = field(default_factory=list)
    agents: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    category: str = "productivity"


class PluginBuilder:
    """Main plugin builder class."""

    def __init__(self, marketplace_root: Optional[Path] = None):
        """Initialize the plugin builder."""
        if marketplace_root is None:
            # Auto-detect marketplace root
            script_dir = Path(__file__).parent
            marketplace_root = script_dir.parent

        self.root = marketplace_root
        self.registry_dir = self.root / "registry"
        self.plugins_dir = self.root / "plugins"

    def get_registry_assets(self, asset_type: Optional[AssetType] = None) -> list[Asset]:
        """Get all assets from the registry."""
        assets = []
        types_to_check = [asset_type] if asset_type else list(AssetType)

        for atype in types_to_check:
            type_dir = self.registry_dir / atype.value
            if not type_dir.exists():
                continue

            for item in type_dir.iterdir():
                if item.name.startswith("."):
                    continue

                # Handle both files (.md) and directories (skills)
                if item.is_file() and item.suffix == ".md":
                    name = item.stem
                elif item.is_dir():
                    name = item.name
                else:
                    continue

                assets.append(Asset(
                    name=name,
                    asset_type=atype,
                    path=item,
                    description=self._get_asset_description(item)
                ))

        return sorted(assets, key=lambda a: (a.asset_type.value, a.name))

    def _get_asset_description(self, path: Path) -> str:
        """Extract description from asset file."""
        try:
            if path.is_file():
                content = path.read_text(encoding="utf-8")
            elif path.is_dir():
                # Try SKILL.md or README.md
                for name in ["SKILL.md", "README.md"]:
                    desc_file = path / name
                    if desc_file.exists():
                        content = desc_file.read_text(encoding="utf-8")
                        break
                else:
                    return ""

            # Parse frontmatter description or first paragraph
            lines = content.strip().split("\n")
            if lines and lines[0] == "---":
                # YAML frontmatter
                for i, line in enumerate(lines[1:], 1):
                    if line == "---":
                        break
                    if line.startswith("description:"):
                        return line.split(":", 1)[1].strip().strip("\"'")

            # Fall back to first non-empty, non-heading line
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("---"):
                    return line[:100]

            return ""
        except Exception:
            return ""

    def get_plugins(self) -> list[Plugin]:
        """Get all plugin definitions."""
        plugins = []

        for plugin_dir in self.plugins_dir.iterdir():
            if not plugin_dir.is_dir() or plugin_dir.name.startswith("."):
                continue

            plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
            if plugin_json.exists():
                try:
                    data = json.loads(plugin_json.read_text(encoding="utf-8"))
                    plugin = Plugin(
                        name=data.get("name", plugin_dir.name),
                        description=data.get("description", ""),
                        version=data.get("version", "1.0.0"),
                        keywords=data.get("keywords", []),
                        category=data.get("category", "productivity")
                    )

                    # Discover assets in plugin
                    plugin.commands = self._list_plugin_assets(plugin_dir, "commands")
                    plugin.agents = self._list_plugin_assets(plugin_dir, "agents")
                    plugin.skills = self._list_plugin_assets(plugin_dir, "skills")

                    plugins.append(plugin)
                except Exception as e:
                    print(f"Warning: Could not load plugin {plugin_dir.name}: {e}")

        return sorted(plugins, key=lambda p: p.name)

    def _list_plugin_assets(self, plugin_dir: Path, asset_type: str) -> list[str]:
        """List asset names in a plugin directory."""
        assets_dir = plugin_dir / asset_type
        if not assets_dir.exists():
            return []

        names = []
        for item in assets_dir.iterdir():
            if item.name.startswith("."):
                continue
            if item.is_file() and item.suffix == ".md":
                names.append(item.stem)
            elif item.is_dir():
                names.append(item.name)

        return sorted(names)

    def create_plugin(self, name: str, description: str = "") -> Plugin:
        """Create a new empty plugin."""
        plugin_dir = self.plugins_dir / name

        if plugin_dir.exists():
            raise ValueError(f"Plugin '{name}' already exists")

        # Create directory structure
        plugin_dir.mkdir(parents=True)
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / "commands").mkdir()
        (plugin_dir / "agents").mkdir()
        (plugin_dir / "skills").mkdir()

        # Create plugin.json
        plugin = Plugin(name=name, description=description)
        plugin_json = {
            "name": name,
            "description": description,
            "version": "1.0.0",
            "author": {"name": "Cameron Sjo"},
            "keywords": [],
            "category": "productivity"
        }

        (plugin_dir / ".claude-plugin" / "plugin.json").write_text(
            json.dumps(plugin_json, indent=2),
            encoding="utf-8"
        )

        print(f"Created plugin: {name}")
        return plugin

    def add_asset_to_plugin(
        self,
        plugin_name: str,
        asset_name: str,
        asset_type: AssetType
    ) -> None:
        """Add an asset from registry to a plugin via symlink."""
        plugin_dir = self.plugins_dir / plugin_name
        if not plugin_dir.exists():
            raise ValueError(f"Plugin '{plugin_name}' does not exist")

        # Find asset in registry
        registry_path = self.registry_dir / asset_type.value / asset_name

        # Check for .md file or directory
        if not registry_path.exists():
            registry_path = self.registry_dir / asset_type.value / f"{asset_name}.md"

        if not registry_path.exists():
            raise ValueError(f"Asset '{asset_name}' not found in registry/{asset_type.value}")

        # Determine target path in plugin
        target_dir = plugin_dir / asset_type.value
        target_dir.mkdir(exist_ok=True)

        if registry_path.is_file():
            target_path = target_dir / registry_path.name
        else:
            target_path = target_dir / asset_name

        if target_path.exists():
            print(f"Asset already exists in plugin: {target_path}")
            return

        # Create relative symlink
        rel_path = os.path.relpath(registry_path, target_path.parent)
        os.symlink(rel_path, target_path)

        print(f"Added {asset_type.value[:-1]} '{asset_name}' to plugin '{plugin_name}'")

    def remove_asset_from_plugin(
        self,
        plugin_name: str,
        asset_name: str,
        asset_type: AssetType
    ) -> None:
        """Remove an asset from a plugin."""
        plugin_dir = self.plugins_dir / plugin_name
        if not plugin_dir.exists():
            raise ValueError(f"Plugin '{plugin_name}' does not exist")

        target_dir = plugin_dir / asset_type.value

        # Find the asset (could be .md file or directory)
        target_path = target_dir / asset_name
        if not target_path.exists():
            target_path = target_dir / f"{asset_name}.md"

        if not target_path.exists():
            raise ValueError(f"Asset '{asset_name}' not found in plugin")

        # Remove symlink or file
        if target_path.is_symlink():
            target_path.unlink()
        elif target_path.is_file():
            target_path.unlink()
        elif target_path.is_dir():
            shutil.rmtree(target_path)

        print(f"Removed {asset_type.value[:-1]} '{asset_name}' from plugin '{plugin_name}'")

    def add_to_registry(
        self,
        source_path: Path,
        asset_type: AssetType,
        name: Optional[str] = None
    ) -> Asset:
        """Add a new asset to the registry."""
        if not source_path.exists():
            raise ValueError(f"Source path does not exist: {source_path}")

        if name is None:
            name = source_path.stem if source_path.is_file() else source_path.name

        target_dir = self.registry_dir / asset_type.value
        target_dir.mkdir(parents=True, exist_ok=True)

        if source_path.is_file():
            target_path = target_dir / source_path.name
        else:
            target_path = target_dir / name

        if target_path.exists():
            raise ValueError(f"Asset already exists in registry: {target_path}")

        # Copy to registry
        if source_path.is_file():
            shutil.copy2(source_path, target_path)
        else:
            shutil.copytree(source_path, target_path)

        print(f"Added to registry: {asset_type.value}/{name}")

        return Asset(
            name=name,
            asset_type=asset_type,
            path=target_path,
            description=self._get_asset_description(target_path)
        )

    def validate(self) -> bool:
        """Validate all plugins and symlinks."""
        valid = True

        for plugin in self.get_plugins():
            plugin_dir = self.plugins_dir / plugin.name

            for asset_type in AssetType:
                assets_dir = plugin_dir / asset_type.value
                if not assets_dir.exists():
                    continue

                for item in assets_dir.iterdir():
                    if item.is_symlink():
                        target = item.resolve()
                        if not target.exists():
                            print(f"BROKEN SYMLINK: {item} -> {target}")
                            valid = False
                        else:
                            # Verify it points to registry
                            try:
                                target.relative_to(self.registry_dir)
                            except ValueError:
                                print(f"WARNING: Symlink not pointing to registry: {item}")

        if valid:
            print("All plugins validated successfully")

        return valid

    def rebuild_symlinks(self, plugin_name: Optional[str] = None) -> None:
        """Rebuild all symlinks for a plugin or all plugins."""
        plugins = self.get_plugins()
        if plugin_name:
            plugins = [p for p in plugins if p.name == plugin_name]
            if not plugins:
                raise ValueError(f"Plugin '{plugin_name}' not found")

        for plugin in plugins:
            plugin_dir = self.plugins_dir / plugin.name
            print(f"Rebuilding symlinks for: {plugin.name}")

            for asset_type in AssetType:
                assets_dir = plugin_dir / asset_type.value
                if not assets_dir.exists():
                    continue

                for item in assets_dir.iterdir():
                    if item.is_symlink():
                        target = item.resolve()
                        if target.exists():
                            # Re-create with relative path
                            item.unlink()
                            rel_path = os.path.relpath(target, item.parent)
                            os.symlink(rel_path, item)


def cmd_list(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """List assets in registry."""
    asset_type = None
    if args.type:
        asset_type = AssetType(args.type)

    assets = builder.get_registry_assets(asset_type)

    if not assets:
        print("No assets in registry")
        return

    current_type = None
    for asset in assets:
        if asset.asset_type != current_type:
            current_type = asset.asset_type
            print(f"\n{current_type.value.upper()}:")
            print("-" * 40)

        desc = f" - {asset.description[:60]}..." if asset.description else ""
        print(f"  {asset.name}{desc}")


def cmd_list_plugins(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """List all plugins."""
    plugins = builder.get_plugins()

    if not plugins:
        print("No plugins found")
        return

    for plugin in plugins:
        print(f"\n{plugin.name}")
        print("=" * len(plugin.name))
        if plugin.description:
            print(f"  {plugin.description}")
        print(f"  Version: {plugin.version}")

        if plugin.commands:
            print(f"  Commands: {', '.join(plugin.commands)}")
        if plugin.agents:
            print(f"  Agents: {', '.join(plugin.agents)}")
        if plugin.skills:
            print(f"  Skills: {', '.join(plugin.skills)}")


def cmd_add(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Add asset to registry."""
    source_path = Path(args.source)
    asset_type = AssetType(args.type)

    builder.add_to_registry(source_path, asset_type, args.name)


def cmd_create(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Create a new plugin."""
    builder.create_plugin(args.name, args.description or "")


def cmd_edit(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Edit a plugin (add/remove assets)."""
    action = args.action
    plugin_name = args.plugin
    asset_name = args.asset
    asset_type = AssetType(args.type)

    if action == "add":
        builder.add_asset_to_plugin(plugin_name, asset_name, asset_type)
    elif action == "remove":
        builder.remove_asset_from_plugin(plugin_name, asset_name, asset_type)


def cmd_validate(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Validate plugins."""
    valid = builder.validate()
    sys.exit(0 if valid else 1)


def cmd_rebuild(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Rebuild symlinks."""
    builder.rebuild_symlinks(args.plugin)


def cmd_interactive(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Interactive mode."""
    print("Plugin Builder - Interactive Mode")
    print("=" * 40)

    while True:
        print("\nOptions:")
        print("  1. List registry assets")
        print("  2. List plugins")
        print("  3. Create new plugin")
        print("  4. Add asset to plugin")
        print("  5. Remove asset from plugin")
        print("  6. Add asset to registry")
        print("  7. Validate all plugins")
        print("  8. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            cmd_list(argparse.Namespace(type=None), builder)

        elif choice == "2":
            cmd_list_plugins(argparse.Namespace(), builder)

        elif choice == "3":
            name = input("Plugin name: ").strip()
            desc = input("Description: ").strip()
            try:
                builder.create_plugin(name, desc)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            plugins = builder.get_plugins()
            print("\nPlugins:", ", ".join(p.name for p in plugins))
            plugin = input("Plugin name: ").strip()

            print("\nAsset types: commands, agents, skills")
            atype = input("Asset type: ").strip()

            assets = builder.get_registry_assets(AssetType(atype))
            print(f"\nAvailable {atype}:", ", ".join(a.name for a in assets))
            asset = input("Asset name: ").strip()

            try:
                builder.add_asset_to_plugin(plugin, asset, AssetType(atype))
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            plugin = input("Plugin name: ").strip()
            atype = input("Asset type (commands/agents/skills): ").strip()
            asset = input("Asset name: ").strip()

            try:
                builder.remove_asset_from_plugin(plugin, asset, AssetType(atype))
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "6":
            source = input("Source path: ").strip()
            atype = input("Asset type (commands/agents/skills): ").strip()
            name = input("Name (or enter for auto): ").strip() or None

            try:
                builder.add_to_registry(Path(source), AssetType(atype), name)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "7":
            builder.validate()

        elif choice == "8":
            break

        else:
            print("Invalid choice")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Plugin Builder CLI for Claude Code marketplace"
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Marketplace root directory"
    )

    subparsers = parser.add_subparsers(dest="command")

    # list
    list_parser = subparsers.add_parser("list", help="List registry assets")
    list_parser.add_argument(
        "--type", "-t",
        choices=["commands", "agents", "skills"],
        help="Filter by asset type"
    )

    # list-plugins
    subparsers.add_parser("list-plugins", help="List all plugins")

    # add (to registry)
    add_parser = subparsers.add_parser("add", help="Add asset to registry")
    add_parser.add_argument("source", help="Source file or directory")
    add_parser.add_argument(
        "--type", "-t",
        required=True,
        choices=["commands", "agents", "skills"],
        help="Asset type"
    )
    add_parser.add_argument("--name", "-n", help="Asset name (default: from source)")

    # create (plugin)
    create_parser = subparsers.add_parser("create", help="Create new plugin")
    create_parser.add_argument("name", help="Plugin name")
    create_parser.add_argument("--description", "-d", help="Plugin description")

    # edit (plugin)
    edit_parser = subparsers.add_parser("edit", help="Edit plugin (add/remove assets)")
    edit_parser.add_argument("action", choices=["add", "remove"])
    edit_parser.add_argument("plugin", help="Plugin name")
    edit_parser.add_argument("asset", help="Asset name")
    edit_parser.add_argument(
        "--type", "-t",
        required=True,
        choices=["commands", "agents", "skills"]
    )

    # validate
    subparsers.add_parser("validate", help="Validate all plugins")

    # rebuild
    rebuild_parser = subparsers.add_parser("rebuild", help="Rebuild symlinks")
    rebuild_parser.add_argument("--plugin", "-p", help="Specific plugin (default: all)")

    # interactive
    subparsers.add_parser("interactive", aliases=["i"], help="Interactive mode")

    args = parser.parse_args()

    builder = PluginBuilder(args.root)

    if args.command == "list":
        cmd_list(args, builder)
    elif args.command == "list-plugins":
        cmd_list_plugins(args, builder)
    elif args.command == "add":
        cmd_add(args, builder)
    elif args.command == "create":
        cmd_create(args, builder)
    elif args.command == "edit":
        cmd_edit(args, builder)
    elif args.command == "validate":
        cmd_validate(args, builder)
    elif args.command == "rebuild":
        cmd_rebuild(args, builder)
    elif args.command in ("interactive", "i"):
        cmd_interactive(args, builder)
    else:
        # Default to interactive mode
        cmd_interactive(args, builder)


if __name__ == "__main__":
    main()
