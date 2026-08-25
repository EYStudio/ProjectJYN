PROJECT_NAME = 'Project JYN'
PROJECT_NAME_ABBREVIATION = "PJYN"

STUDIO_NAME = 'EyStudio'
STUDIO_MOTTO = 'Exception Ignite Evolution'
DEVELOPERS = 'EyStudio developers'

MAJOR_VER = 0
MINOR_VER = 1
# PATCH_VER = 0

# PRE_STAGE = "a"  # alpha / beta / rc
# PRE_NUM = 2  # a2 / b1 / rc3
#
# PEP 440 version
# if PRE_STAGE:
#     VERSION = f"{MAJOR_VER}.{MINOR_VER}{PRE_STAGE}{PRE_NUM}"
# else:
#     VERSION = f"{MAJOR_VER}.{MINOR_VER}"
#     VERSION = f"{MAJOR_VER}.{MINOR_VER}.{PATCH_VER}"

VERSION = f"{MAJOR_VER}.{MINOR_VER}"

# Windows numeric version
# a=0, b=1, rc=2, final=3
# STAGE_MAP = {"a": 0, "b": 1, "rc": 2, None: 3}
# WIN_FILEVER = (
#     MAJOR_VER,
#     MINOR_VER,
#     STAGE_MAP[PRE_STAGE],
#     PRE_NUM if PRE_STAGE else PATCH_VER
# )

FULL_VERSION = f"{PROJECT_NAME} v{VERSION}"

UPDATE_URL = "https://api.github.com/repos/Eystudio/PJIP/releases/latest"
UPDATE_URLS = tuple(UPDATE_URL)

# CODE_NAME = ''
NICKNAME = PROJECT_NAME_ABBREVIATION
