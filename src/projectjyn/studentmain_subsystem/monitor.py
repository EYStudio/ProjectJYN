from abc import ABC, abstractmethod
from typing import Any

from projectjyn.app import constants
from projectjyn.core.enums import SuspendState


class Monitor(ABC):

    @abstractmethod
    def poll(self) -> Any:
        """Perform one check and return the current state."""
        raise NotImplementedError


class ProcessMonitor(Monitor):

    def __init__(self, logic):
        self.logic = logic

    def poll(self) -> bool:
        return self.logic.get_process_state(
            constants.E_CLASSROOM_PROGRAM_NAME
        )


class SuspendMonitor(Monitor):

    def __init__(self, logic):
        self.logic = logic

    def poll(self) -> SuspendState:
        pids = self.logic.get_pid_from_process_name(
            constants.E_CLASSROOM_PROGRAM_NAME
        )

        if not pids:
            return SuspendState.NOT_FOUND

        pid = pids[0]

        if self.logic.is_suspended(pid):
            return SuspendState.SUSPENDED

        return SuspendState.RUNNING


class StudentmainPasswordMonitor(Monitor):

    def __init__(self, logic):
        self.logic = logic

    def poll(self):
        return self.logic.decode_studentmain_password()
