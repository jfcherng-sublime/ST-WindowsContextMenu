from typing import Any, Optional

import sublime

from .constants import PLUGIN_NAME


def get_plugin_setting(key: str, default: Optional[Any] = None) -> Any:
    return get_plugin_settings().get(key, default)


def get_plugin_settings() -> sublime.Settings:
    return sublime.load_settings(f"{PLUGIN_NAME}.sublime-settings")


def get_st_setting(key: str, default: Optional[Any] = None) -> Any:
    return get_st_settings().get(key, default)


def get_st_settings() -> sublime.Settings:
    return sublime.load_settings("Preferences.sublime-settings")
