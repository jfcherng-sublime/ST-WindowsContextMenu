from __future__ import annotations

# import all listeners and commands
from .commands.wcm_toggle_open_with import WcmToggleOpenWithCommand
from .constants import PLUGIN_NAME
from .helpers import enabled_app_context_menu_sets
from .settings import get_plugin_setting, get_plugin_settings

__all__ = (
    # ST: core
    "plugin_loaded",
    "plugin_unloaded",
    # ST: commands
    "WcmToggleOpenWithCommand",
)


def plugin_loaded() -> None:
    """Called when the plugin is loaded."""
    settings = get_plugin_settings()
    settings.add_on_change(PLUGIN_NAME, _on_settings_changed)


def plugin_unloaded() -> None:
    """Called when the plugin is unloaded."""


def _on_settings_changed() -> None:
    for app_menu_set in enabled_app_context_menu_sets():
        app_menu_set.update_menu_text(get_plugin_setting("menu_text"))
