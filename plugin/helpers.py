from __future__ import annotations

from itertools import product
from typing import Generator

from .core import AppContextMenuSet
from .types import AppInfo, MenuTarget

APP_INFOS = {
    "sublime_text": AppInfo(
        name="Sublime Text",
        nickname="st",
        exe_name="sublime_text.exe",
        cmd_exe_name="subl.exe",
    ),
    "sublime_merge": AppInfo(
        name="Sublime Merge",
        nickname="sm",
        exe_name="sublime_merge.exe",
        cmd_exe_name="smerge.exe",
    ),
}

MENU_TARGETS = {
    "file": MenuTarget(
        type="file",
        reg_key=R"SOFTWARE\Classes\*\shell",
    ),
    "directory": MenuTarget(
        type="directory",
        reg_key=R"SOFTWARE\Classes\Directory\shell",
    ),
    "directory_background": MenuTarget(
        type="directory_background",
        reg_key=R"SOFTWARE\Classes\Directory\Background\shell",
    ),
}


def enabled_app_context_menu_sets() -> Generator[AppContextMenuSet, None, None]:
    for app, target in product(APP_INFOS.keys(), MENU_TARGETS.keys()):
        if (app_menu_set := parse_app_and_target(app, target)).exists():
            yield app_menu_set


def parse_app_and_target(app_name: str, target_name: str) -> AppContextMenuSet:
    if not (app_info := APP_INFOS.get(app_name)):
        raise ValueError

    if target_name == "_all_":
        targets = [
            target
            for target in MENU_TARGETS.values()
            # cannot open a file with SM
            if not (app_info.nickname == "sm" and target.type == "file")
        ]
    else:
        targets = [MENU_TARGETS[target_name]]  # may KeyError

    return AppContextMenuSet(app_info, targets)
