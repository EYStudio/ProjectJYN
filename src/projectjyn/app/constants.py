import os
import sys


def get_base_dir():
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        return os.path.dirname(sys.executable)

    # Running in normal Python environment
    if sys.argv and sys.argv[0]:
        return os.path.dirname(os.path.abspath(sys.argv[0]))

    return os.path.dirname(os.path.abspath(__file__))


E_CLASSROOM_NAME = 'studentmain'
E_CLASSROOM_PROGRAM_NAME = E_CLASSROOM_NAME + '.exe'

STUDENTMAIN_NAME = 'studentmain'
IS_E_CLASSROOM_STUDENTMAIN = STUDENTMAIN_NAME.lower() == E_CLASSROOM_NAME.lower()

BASE_DIR = get_base_dir()
CONFIG_PATH = os.path.join(BASE_DIR, "PJIPConfig.toml")

print(f"Config Path: {CONFIG_PATH}")
