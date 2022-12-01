# import all listeners and commands
from .commands.wcm_toggle_open_with import WcmToggleOpenWithCommand

__all__ = (
    # ST: core
    "plugin_loaded",
    "plugin_unloaded",
    # ST: commands
    "WcmToggleOpenWithCommand",
)


def plugin_loaded() -> None:
    """Called when the plugin is loaded."""


def plugin_unloaded() -> None:
    """Called when the plugin is unloaded."""
