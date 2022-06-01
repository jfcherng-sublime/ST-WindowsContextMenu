from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import sublime


@dataclass
class AppInfo:
    name: str
    nickname: str
    exe_name: str
    cmd_exe_name: str

    @property
    def app_dir(self) -> Optional[Path]:
        if self.nickname == "st":
            return Path(sublime.executable_path()).parent
        if self.nickname == "sm":
            pref = sublime.load_settings("Preferences.sublime-settings")
            if Path(bound_sm := pref.get("sublime_merge_path", "")).is_file():
                return bound_sm.parent
            # convention
            if (default := Path(R"C:\Program Files\Sublime Merge")).is_dir():
                return default
            return None
        return None


@dataclass
class MenuTarget:
    type: str
    reg_key: str
