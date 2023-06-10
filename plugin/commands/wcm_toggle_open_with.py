from __future__ import annotations

from functools import wraps
from pathlib import Path
from typing import Any, Callable, TypeVar, cast

import sublime
import sublime_plugin

from ..core import AppContextMenuSet
from ..helpers import parse_app_and_target
from ..settings import get_plugin_setting

_T_AnyCallable = TypeVar("_T_AnyCallable", bound=Callable[..., Any])


def _provide_app_menu_set(error_prompt: bool = False) -> Callable[[_T_AnyCallable], _T_AnyCallable]:
    def decorator(func: _T_AnyCallable) -> _T_AnyCallable:
        @wraps(func)
        def wrapper(self: sublime_plugin.Command, app: str, target: str, **kwargs) -> Any:
            try:
                app_menu_set = parse_app_and_target(app, target)
            except Exception:
                if error_prompt:
                    sublime.error_message(f"Unsupported args: {app = }, {target = }")
                    return
                app_menu_set = None
            return func(self, app_menu_set=app_menu_set, **kwargs)

        return cast(_T_AnyCallable, wrapper)

    return decorator


class WcmToggleOpenWithCommand(sublime_plugin.ApplicationCommand):
    @_provide_app_menu_set(error_prompt=False)
    def is_checked(self, app_menu_set: AppContextMenuSet | None) -> bool:  # type: ignore
        return bool(app_menu_set and self._is_checked(app_menu_set))

    @_provide_app_menu_set(error_prompt=True)
    def run(self, app_menu_set: AppContextMenuSet) -> None:
        # currently enabled => we want to disable
        if self._is_checked(app_menu_set):
            app_menu_set.remove()
        # currently disable => we want to enabled
        else:
            app = app_menu_set.app
            menu_text: str = get_plugin_setting("menu_text")
            sublime.message_dialog(f"Please select {app.name} directory...")
            sublime.select_folder_dialog(
                lambda folder: self._add_select_app_dir_callback(
                    app_menu_set,
                    folder,  # type: ignore
                    menu_text,
                ),
                str(app.app_dir or ""),  # default folder for selecting is not working on Windows (ST bug?)
            )

    @staticmethod
    def _is_checked(app_menu_set: AppContextMenuSet) -> bool:
        return app_menu_set.exists()

    @staticmethod
    def _add_select_app_dir_callback(
        app_menu_set: AppContextMenuSet,
        app_dir: str | Path | None,
        menu_text: str,
    ) -> None:
        if not app_dir:
            return
        app_dir = Path(app_dir)

        # ensure necessary executables exist
        app = app_menu_set.app
        for file in {app.exe_name, app.cmd_exe_name}:
            if not (app_dir / file).is_file():
                sublime.error_message(f'Can not find "{file}" in "{app_dir}".')
                return

        app_menu_set.add(app_dir, menu_text)
