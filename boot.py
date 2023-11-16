def reload_plugin() -> None:
    import sys

    # remove all previously loaded plugin modules
    prefix = f"{__package__}."
    for module_name in tuple(filter(lambda m: m.startswith(prefix) and m != __name__, sys.modules)):
        del sys.modules[module_name]


reload_plugin()

try:
    import winreg  # noqa: F401
except ModuleNotFoundError:
    pass
else:
    from .plugin import *  # noqa: F401, F403
