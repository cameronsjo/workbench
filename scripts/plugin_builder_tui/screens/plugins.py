"""Plugins screen for browsing and editing plugins."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import (
    Button,
    Label,
    ListItem,
    ListView,
    SelectionList,
    Static,
    Tree,
)
from textual.widgets.selection_list import Selection

from ..builder import AssetType, Plugin, PluginBuilder

if TYPE_CHECKING:
    pass


class PluginListItem(ListItem):
    """A list item representing a plugin."""

    def __init__(self, plugin: Plugin, **kwargs) -> None:
        super().__init__(**kwargs)
        self.plugin = plugin

    def compose(self) -> ComposeResult:
        with Horizontal(classes="plugin-item"):
            yield Label(self.plugin.name, classes="plugin-name")
            yield Label(
                f"({self.plugin.total_assets})",
                classes="plugin-count",
            )


class AddAssetModal(ModalScreen[list[tuple[str, AssetType]] | None]):
    """Modal for adding assets to a plugin with multiselect."""

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("space", "toggle", "Toggle"),
        ("a", "select_all", "Select All"),
    ]

    CSS = """
    AddAssetModal {
        align: center middle;
    }

    AddAssetModal > #add-asset-dialog {
        width: 70;
        height: auto;
        max-height: 85%;
        border: round #5fafff;
        background: $background;
        padding: 1 2;
    }

    AddAssetModal #asset-type-tabs {
        height: 3;
        margin-bottom: 1;
    }

    AddAssetModal #available-assets {
        height: 22;
        border: round #808080 30%;
        margin-bottom: 1;
    }

    AddAssetModal .modal-title {
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    AddAssetModal .selection-hint {
        color: #808080;
        margin-bottom: 1;
    }

    AddAssetModal .modal-buttons {
        height: 3;
        align: right middle;
    }

    AddAssetModal Button {
        margin: 0 1;
    }
    """

    def __init__(
        self,
        plugin: Plugin,
        builder: PluginBuilder,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.plugin = plugin
        self.builder = builder
        self.current_type = AssetType.COMMAND
        self.selected_assets: list[tuple[str, AssetType]] = []

    def compose(self) -> ComposeResult:
        with Container(id="add-asset-dialog"):
            yield Label(f"Add Assets to [bold]{self.plugin.name}[/]", classes="modal-title")
            yield Label("[dim]Space to toggle, A to select all[/]", classes="selection-hint")

            # Type selector buttons
            with Horizontal(id="asset-type-tabs"):
                yield Button("Commands", id="btn-commands", variant="primary")
                yield Button("Agents", id="btn-agents")
                yield Button("Skills", id="btn-skills")

            # Available assets list with multiselect
            yield SelectionList[str](id="available-assets")

            # Action buttons
            with Horizontal(classes="modal-buttons"):
                yield Button("Cancel", id="btn-cancel")
                yield Button("Add Selected (0)", id="btn-add", variant="success", disabled=True)

    def on_mount(self) -> None:
        """Load initial assets."""
        self._load_assets(AssetType.COMMAND)
        self.set_timer(0.1, lambda: self.query_one("#available-assets", SelectionList).focus())

    def _load_assets(self, asset_type: AssetType) -> None:
        """Load available assets for the given type, grouped by prefix."""
        self.current_type = asset_type

        # Update button styles
        for btn_id, btn_type in [
            ("btn-commands", AssetType.COMMAND),
            ("btn-agents", AssetType.AGENT),
            ("btn-skills", AssetType.SKILL),
        ]:
            btn = self.query_one(f"#{btn_id}", Button)
            btn.variant = "primary" if btn_type == asset_type else "default"

        # Get assets not already in the plugin
        all_assets = self.builder.get_registry_assets(asset_type)
        existing = set(getattr(self.plugin, asset_type.value, []))
        available = [a for a in all_assets if a.name not in existing]

        # Update modal title with count
        title = self.query_one(".modal-title", Label)
        title.update(
            f"Add {asset_type.value.title()} to [bold]{self.plugin.name}[/] "
            f"[dim]({len(available)} available)[/]"
        )

        # Group assets by prefix (e.g., roadmap.*, pr.*, review.*)
        groups: dict[str, list] = {}
        ungrouped = []
        for asset in available:
            if "." in asset.name:
                prefix = asset.name.split(".")[0]
                if prefix not in groups:
                    groups[prefix] = []
                groups[prefix].append(asset)
            elif "-" in asset.name:
                prefix = asset.name.split("-")[0]
                # Only group if we have 2+ with same prefix
                if prefix not in groups:
                    groups[prefix] = []
                groups[prefix].append(asset)
            else:
                ungrouped.append(asset)

        # Move single-item groups to ungrouped
        for prefix in list(groups.keys()):
            if len(groups[prefix]) < 2:
                ungrouped.extend(groups[prefix])
                del groups[prefix]

        # Update selection list
        selection_list = self.query_one("#available-assets", SelectionList)
        selection_list.clear_options()

        if not available:
            pass
        else:
            # Add grouped items first
            for prefix in sorted(groups.keys()):
                items = sorted(groups[prefix], key=lambda a: a.name)
                for asset in items:
                    desc = f" - {asset.description[:30]}..." if asset.description else ""
                    selection_list.add_option((f"[cyan]{prefix}[/] {asset.name}{desc}", asset.name))

            # Add ungrouped items
            for asset in sorted(ungrouped, key=lambda a: a.name):
                desc = f" - {asset.description[:35]}..." if asset.description else ""
                selection_list.add_option((f"{asset.name}{desc}", asset.name))

        self._update_add_button()

    def _update_add_button(self) -> None:
        """Update the Add button with selection count."""
        selection_list = self.query_one("#available-assets", SelectionList)
        selected = list(selection_list.selected)
        count = len(selected)

        btn = self.query_one("#btn-add", Button)
        btn.label = f"Add Selected ({count})"
        btn.disabled = count == 0

    def on_selection_list_selection_toggled(
        self, event: SelectionList.SelectionToggled
    ) -> None:
        """Handle selection changes."""
        self._update_add_button()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-commands":
            self._load_assets(AssetType.COMMAND)
        elif event.button.id == "btn-agents":
            self._load_assets(AssetType.AGENT)
        elif event.button.id == "btn-skills":
            self._load_assets(AssetType.SKILL)
        elif event.button.id == "btn-cancel":
            self.dismiss(None)
        elif event.button.id == "btn-add":
            selection_list = self.query_one("#available-assets", SelectionList)
            selected = [(str(v), self.current_type) for v in selection_list.selected]
            if selected:
                self.dismiss(selected)

    def action_cancel(self) -> None:
        """Cancel the modal."""
        self.dismiss(None)

    def action_select_all(self) -> None:
        """Select all available assets."""
        selection_list = self.query_one("#available-assets", SelectionList)
        selection_list.select_all()
        self._update_add_button()


class RemoveAssetModal(ModalScreen[list[tuple[str, AssetType]] | None]):
    """Modal for removing assets from a plugin with multiselect."""

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("space", "toggle", "Toggle"),
        ("a", "select_all", "Select All"),
    ]

    CSS = """
    RemoveAssetModal {
        align: center middle;
    }

    RemoveAssetModal > #remove-asset-dialog {
        width: 70;
        height: auto;
        max-height: 85%;
        border: round #ff5f5f;
        background: $background;
        padding: 1 2;
    }

    RemoveAssetModal #plugin-assets {
        height: 22;
        border: round #808080 30%;
        margin-bottom: 1;
    }

    RemoveAssetModal .modal-title {
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    RemoveAssetModal .selection-hint {
        color: #808080;
        margin-bottom: 1;
    }

    RemoveAssetModal .modal-buttons {
        height: 3;
        align: right middle;
    }

    RemoveAssetModal Button {
        margin: 0 1;
    }
    """

    def __init__(self, plugin: Plugin, **kwargs) -> None:
        super().__init__(**kwargs)
        self.plugin = plugin

    def compose(self) -> ComposeResult:
        total = len(self.plugin.commands) + len(self.plugin.agents) + len(self.plugin.skills)
        with Container(id="remove-asset-dialog"):
            yield Label(
                f"Remove Assets from [bold]{self.plugin.name}[/] [dim]({total} total)[/]",
                classes="modal-title",
            )
            yield Label("[dim]Space to toggle, A to select all[/]", classes="selection-hint")

            # Plugin's current assets with multiselect
            yield SelectionList[str](id="plugin-assets")

            # Action buttons
            with Horizontal(classes="modal-buttons"):
                yield Button("Cancel", id="btn-cancel")
                yield Button("Remove Selected (0)", id="btn-remove", variant="error", disabled=True)

    def on_mount(self) -> None:
        """Load plugin's assets."""
        selection_list = self.query_one("#plugin-assets", SelectionList)

        # Add commands
        for cmd in self.plugin.commands:
            selection_list.add_option((f"[cyan]cmd[/] /{cmd}", f"commands:{cmd}"))

        # Add agents
        for agent in self.plugin.agents:
            selection_list.add_option((f"[green]agent[/] {agent}", f"agents:{agent}"))

        # Add skills
        for skill in self.plugin.skills:
            selection_list.add_option((f"[yellow]skill[/] {skill}", f"skills:{skill}"))

        self.set_timer(0.1, lambda: selection_list.focus())

    def _update_remove_button(self) -> None:
        """Update the Remove button with selection count."""
        selection_list = self.query_one("#plugin-assets", SelectionList)
        selected = list(selection_list.selected)
        count = len(selected)

        btn = self.query_one("#btn-remove", Button)
        btn.label = f"Remove Selected ({count})"
        btn.disabled = count == 0

    def on_selection_list_selection_toggled(
        self, event: SelectionList.SelectionToggled
    ) -> None:
        """Handle selection changes."""
        self._update_remove_button()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-cancel":
            self.dismiss(None)
        elif event.button.id == "btn-remove":
            selection_list = self.query_one("#plugin-assets", SelectionList)
            results = []
            for v in selection_list.selected:
                type_str, asset_name = str(v).split(":", 1)
                results.append((asset_name, AssetType(type_str)))
            if results:
                self.dismiss(results)

    def action_cancel(self) -> None:
        """Cancel the modal."""
        self.dismiss(None)

    def action_select_all(self) -> None:
        """Select all assets."""
        selection_list = self.query_one("#plugin-assets", SelectionList)
        selection_list.select_all()
        self._update_remove_button()


class PluginsScreen(Screen):
    """Screen for browsing and editing plugins."""

    BINDINGS = [
        ("n", "new_plugin", "New Plugin"),
        ("a", "add_asset", "Add Asset"),
        ("r", "remove_asset", "Remove Asset"),
        ("enter", "select", "Select"),
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected_plugin: Plugin | None = None

    def compose(self) -> ComposeResult:
        builder: PluginBuilder = self.app.builder  # type: ignore
        plugins = builder.get_plugins()

        with Container(id="content"):
            yield Label("[bold]Plugins[/]", id="screen-title")

            with Horizontal():
                # Left pane: plugin list
                with Vertical(id="left-pane"):
                    yield Label("[bold]Select Plugin[/]")
                    yield ListView(
                        *[PluginListItem(p, id=f"plugin-{i}-init") for i, p in enumerate(plugins)],
                        id="plugin-list",
                    )
                    yield Button("New Plugin", id="btn-new", variant="primary")

                # Right pane: plugin details
                with Vertical(id="right-pane"):
                    yield Label("[bold]Plugin Contents[/]", id="plugin-title")
                    yield Static(
                        "[dim]Select a plugin to view its contents[/]",
                        id="plugin-details",
                    )
                    tree: Tree[str] = Tree("Assets", id="asset-tree")
                    tree.show_root = False
                    yield tree
                    with Horizontal(id="plugin-actions"):
                        yield Button(
                            "Add Asset", id="btn-add", variant="success", disabled=True
                        )
                        yield Button(
                            "Remove Asset", id="btn-remove", variant="error", disabled=True
                        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle plugin selection."""
        if not isinstance(event.item, PluginListItem):
            return

        self.selected_plugin = event.item.plugin
        self._update_plugin_details()

    def _update_plugin_details(self) -> None:
        """Update the right pane with selected plugin details."""
        if not self.selected_plugin:
            return

        plugin = self.selected_plugin

        # Update title
        title = self.query_one("#plugin-title", Label)
        title.update(f"[bold]{plugin.name}[/]")

        # Update details
        details = self.query_one("#plugin-details", Static)
        details.update(
            f"{plugin.description}\n"
            f"[dim]Version: {plugin.version} | Category: {plugin.category}[/]"
        )

        # Update tree
        tree = self.query_one("#asset-tree", Tree)
        tree.clear()

        # Add commands
        if plugin.commands:
            commands_node = tree.root.add("Commands", expand=True)
            for cmd in plugin.commands:
                commands_node.add_leaf(f"/{cmd}")

        # Add agents
        if plugin.agents:
            agents_node = tree.root.add("Agents", expand=True)
            for agent in plugin.agents:
                agents_node.add_leaf(agent)

        # Add skills
        if plugin.skills:
            skills_node = tree.root.add("Skills", expand=True)
            for skill in plugin.skills:
                skills_node.add_leaf(skill)

        if not (plugin.commands or plugin.agents or plugin.skills):
            tree.root.add_leaf("[dim]No assets[/]")

        # Enable action buttons
        self.query_one("#btn-add", Button).disabled = False
        self.query_one("#btn-remove", Button).disabled = False

    def _refresh_plugin_list(self) -> None:
        """Refresh the plugin list after changes."""
        builder: PluginBuilder = self.app.builder  # type: ignore
        plugins = builder.get_plugins()

        plugin_list = self.query_one("#plugin-list", ListView)
        current_plugin_name = self.selected_plugin.name if self.selected_plugin else None

        # Remove all existing items properly
        plugin_list.clear()

        # Use unique IDs with timestamp to avoid conflicts during refresh
        import time
        ts = int(time.time() * 1000) % 100000

        for i, p in enumerate(plugins):
            plugin_list.append(PluginListItem(p, id=f"plugin-{i}-{ts}"))

        # Re-select the current plugin if it still exists
        if current_plugin_name:
            for idx, p in enumerate(plugins):
                if p.name == current_plugin_name:
                    self.selected_plugin = p
                    self._update_plugin_details()
                    # Set the index to highlight the plugin
                    plugin_list.index = idx
                    break
            else:
                # Plugin was deleted, clear selection
                self.selected_plugin = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-new":
            self.action_new_plugin()
        elif event.button.id == "btn-add":
            self.action_add_asset()
        elif event.button.id == "btn-remove":
            self.action_remove_asset()

    def action_new_plugin(self) -> None:
        """Create a new plugin."""
        self.app.notify(
            "Use CLI: python plugin-builder.py create <name>",
            severity="information",
        )

    def action_add_asset(self) -> None:
        """Add assets to the selected plugin (multiselect)."""
        if not self.selected_plugin:
            self.app.notify("Select a plugin first", severity="warning")
            return

        builder: PluginBuilder = self.app.builder  # type: ignore

        def handle_add(result: list[tuple[str, AssetType]] | None) -> None:
            if result is None or not result:
                return

            added = 0
            errors = 0
            for asset_name, asset_type in result:
                try:
                    success = builder.add_asset_to_plugin(
                        self.selected_plugin.name,  # type: ignore
                        asset_name,
                        asset_type,
                    )
                    if success:
                        added += 1
                    else:
                        errors += 1
                except Exception:
                    errors += 1

            if added > 0:
                self.app.notify(
                    f"Added {added} asset(s) to {self.selected_plugin.name}",  # type: ignore
                    severity="information",
                )
                self._refresh_plugin_list()
            if errors > 0:
                self.app.notify(
                    f"{errors} asset(s) failed to add",
                    severity="warning",
                )

        self.app.push_screen(
            AddAssetModal(self.selected_plugin, builder),
            handle_add,
        )

    def action_remove_asset(self) -> None:
        """Remove assets from the selected plugin (multiselect)."""
        if not self.selected_plugin:
            self.app.notify("Select a plugin first", severity="warning")
            return

        # Check if plugin has any assets
        if not (self.selected_plugin.commands or self.selected_plugin.agents or self.selected_plugin.skills):
            self.app.notify(
                f"{self.selected_plugin.name} has no assets to remove",
                severity="information",
            )
            return

        builder: PluginBuilder = self.app.builder  # type: ignore

        def handle_remove(result: list[tuple[str, AssetType]] | None) -> None:
            if result is None or not result:
                return

            removed = 0
            errors = 0
            for asset_name, asset_type in result:
                try:
                    success = builder.remove_asset_from_plugin(
                        self.selected_plugin.name,  # type: ignore
                        asset_name,
                        asset_type,
                    )
                    if success:
                        removed += 1
                    else:
                        errors += 1
                except Exception:
                    errors += 1

            if removed > 0:
                self.app.notify(
                    f"Removed {removed} asset(s) from {self.selected_plugin.name}",  # type: ignore
                    severity="information",
                )
                self._refresh_plugin_list()
            if errors > 0:
                self.app.notify(
                    f"{errors} asset(s) failed to remove",
                    severity="warning",
                )

        self.app.push_screen(
            RemoveAssetModal(self.selected_plugin),
            handle_remove,
        )
