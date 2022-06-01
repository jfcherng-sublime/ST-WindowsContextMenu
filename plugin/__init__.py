import sublime

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
    sublime.set_timeout_async(plugin_loaded_real)


def plugin_loaded_real() -> None:
    ...


def plugin_unloaded() -> None:
    ...
