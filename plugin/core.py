from .types import AppInfo, MenuTarget
from pathlib import Path
from typing import Sequence, Union
import itertools
import winreg

KeyType = Union[winreg.HKEYType, int]


class AppContextMenuSet:
    def __init__(self, app: AppInfo, targets: Sequence[MenuTarget]) -> None:
        self.app = app
        self.targets = targets

    def exists(self) -> bool:
        return all(self._exists(self.app, target) for target in self.targets)

    def add(self, app_dir: Path) -> None:
        for target in self.targets:
            self._add(self.app, target, app_dir=app_dir)

    def remove(self) -> None:
        for target in self.targets:
            self._remove(self.app, target)

    @staticmethod
    def _exists(app: AppInfo, target: MenuTarget) -> bool:
        try:
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, Rf"{target.reg_key}\{app.name}")
            return True
        except OSError:
            return False

    @staticmethod
    def _add(app: AppInfo, target: MenuTarget, *, app_dir: Path) -> None:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, Rf"{target.reg_key}\{app.name}") as app_key:
            winreg.SetValueEx(app_key, None, 0, winreg.REG_SZ, f"Open with {app.name}")
            winreg.SetValueEx(app_key, "Icon", 0, winreg.REG_SZ, f"{app_dir / app.exe_name},0")
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, Rf"{target.reg_key}\{app.name}\command") as app_cmd_key:
            arg = '"%V"' if target.type == "directory_background" else '"%1"'
            winreg.SetValueEx(app_cmd_key, None, 0, winreg.REG_SZ, f"{app_dir / app.cmd_exe_name} {arg}")

    @staticmethod
    def _remove(app: AppInfo, target: MenuTarget) -> None:
        def delete_key(key: KeyType, subkey: str, recursive: bool = False) -> None:
            # delete children first
            if recursive:
                with winreg.OpenKey(key, subkey) as parent:
                    try:
                        for idx in itertools.count(0, step=1):
                            delete_key(parent, winreg.EnumKey(parent, idx), recursive=recursive)
                    except OSError:
                        pass  # end of enumeration
            winreg.DeleteKey(key, subkey)

        delete_key(winreg.HKEY_CURRENT_USER, Rf"{target.reg_key}\{app.name}", recursive=True)
