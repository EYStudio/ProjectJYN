from enum import Enum, auto


class SuspendState(Enum):
    NOT_FOUND = 0
    SUSPENDED = 1
    RUNNING = 2


class UpdateState(Enum):
    IDLE = auto()
    CHECKING = auto()
    UPDATE_AVAILABLE = auto()
    UP_TO_DATE = auto()
    LOCAL_NEWER = auto()
    NOT_FOUND = auto()
    ERROR = auto()


class PidStatus(Enum):
    EXISTS = auto()
    NOT_EXISTS = auto()
    ACCESS_DENIED = auto()
    ERROR = auto()

    # Reserved extension status
    ZOMBIE = auto()
    STOPPED = auto()
    UNKNOWN = auto()

class PrivilegeLevel(Enum):
    USER = auto()
    ADMIN = auto()
    SYSTEM = auto()
