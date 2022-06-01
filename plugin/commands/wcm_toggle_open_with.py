from ..core import AppContextMenuSet
from ..types import AppInfo, MenuTarget
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar, Union
import sublime
import sublime_plugin

AnyCallable = TypeVar("AnyCallable", bound=Callable[..., Any])
CanPath = Union[str, Path]


def provide_app_menu_set(error_prompt: bool = False) -> Callable[[AnyCallable], AnyCallable]:
    def decorator(func: AnyCallable) -> AnyCallable:
        def wrapper(self: sublime_plugin.Command, app: str, target: str, **kwargs) -> Any:
            try:
                app_menu_set = parse_app_and_target(app, target)
            except Exception:
                if error_prompt:
                    sublime.error_message(f"Unsupported args: {app = }, {target = }")
                    return
                app_menu_set = None
            return func(self, app_menu_set=app_menu_set, **kwargs)

        return wrapper  # type: ignore

    return decorator


def parse_app_and_target(app: str, target_str: str) -> AppContextMenuSet:
    if not (app_info := APPS.get(app, None)):
        raise ValueError

    if target_str == "_all_":
        targets = [
            target
            for target in MENU_TARGETS.values()
            # cannot open a file with SM
            if not (app_info.nickname == "sm" and target.type == "file")
        ]
    else:
        targets = [MENU_TARGETS[target_str]]  # may KeyError

    return AppContextMenuSet(app_info, targets)


APPS = {
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


class WcmToggleOpenWithCommand(sublime_plugin.ApplicationCommand):
    @provide_app_menu_set(error_prompt=False)
    def is_checked(self, app_menu_set: Optional[AppContextMenuSet]) -> bool:  # type: ignore
        return bool(app_menu_set and self._is_checked(app_menu_set))

    @provide_app_menu_set(error_prompt=True)
    def run(self, app_menu_set: AppContextMenuSet) -> None:
        # currently enabled => we want to disable
        if self._is_checked(app_menu_set):
            app_menu_set.remove()
        # currently disable => we want to enabled
        else:
            app = app_menu_set.app
            sublime.message_dialog(f"Please select {app.name} directory...")
            sublime.select_folder_dialog(
                lambda folder: self._add_select_app_dir_callback(app_menu_set, folder),  # type: ignore
                str(app.app_dir or ""),  # default folder for selecting is not working on Windows (ST bug?)
            )

    @staticmethod
    def _is_checked(app_menu_set: AppContextMenuSet) -> bool:
        return app_menu_set.exists()

    @staticmethod
    def _add_select_app_dir_callback(app_menu_set: AppContextMenuSet, app_dir: Optional[CanPath]) -> None:
        if not app_dir:
            return
        app_dir = Path(app_dir)

        # ensure necessary executables exist
        app = app_menu_set.app
        for file in (app.exe_name, app.cmd_exe_name):
            if not (app_dir / file).is_file():
                sublime.error_message(f'Can not find "{file}" in "{app_dir}".')
                return

        app_menu_set.add(app_dir)
