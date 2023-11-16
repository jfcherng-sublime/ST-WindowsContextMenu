from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import sublime

from .settings import get_st_setting


@dataclass
class AppInfo:
    name: str
    nickname: str
    exe_name: str
    cmd_exe_name: str

    @property
    def app_dir(self) -> Path | None:
        if self.nickname == "st":
            return Path(sublime.executable_path()).parent
        if self.nickname == "sm":
            if (sm_path := Path(get_st_setting("sublime_merge_path", ""))).is_file():
                return sm_path.parent
            # convention
            if (default := Path(R"C:\Program Files\Sublime Merge")).is_dir():
                return default
        return None


@dataclass
class MenuTarget:
    type: Literal["file", "directory", "directory_background"]
    reg_key: str
