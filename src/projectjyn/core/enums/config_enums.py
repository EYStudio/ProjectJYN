from enum import Enum, auto

class KillMethod(Enum):
    TERMINATE_PROCESS = 'TerminateProcess'
    TERMINATE_THREAD = 'TerminateThread'
    NT_TERMINATE_PROCESS = 'NtTerminateProcess'
    DEFAULT = TERMINATE_PROCESS
