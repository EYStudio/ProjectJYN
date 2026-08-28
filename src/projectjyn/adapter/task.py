from typing import Iterable

from PySide6.QtCore import QObject, Signal

from projectjyn.adapter.runner import TerminatePIDTask
from projectjyn.config.runtime_config.config_structure import ConfigRoot


class TerminatePIDAdapter(QObject):
    change = Signal(str)

    def __init__(self, logic, current_pid, dispatcher, config_object: ConfigRoot):
        super().__init__()
        self.logic = logic
        self.current_pid = current_pid
        self.dispatcher = dispatcher
        self.config_object = config_object

    # Bugs here: self.logic.terminate_process cannot accept tuple, on int
    # def run_async(self, pids):
    #     other_pids = self.split_current_pid(pids)
    #     if not other_pids:
    #         return
    #
    #     task = FutureRunnable(
    #         self.logic.terminate_process,
    #         other_pids,
    #         callback=lambda _: self.change.emit("done"),
    #         error_callback=lambda e: self.change.emit(str(e))
    #     )
    #
    #     self.dispatcher.submit(task, priority=10)

    def run_async(self, pids):
        valid_pids = self.format_pids(pids)
        other_pids = self.split_current_pid(valid_pids)
        kill_method = self.config_object.process.kill_method
        if other_pids:
            task = TerminatePIDTask(self.logic, other_pids, kill_method)
            self.dispatcher.submit(task)


    def run_sync(self, pids):
        valid_pids = self.format_pids(pids)
        other_pids = self.split_current_pid(valid_pids)
        kill_method = self.config_object.process.kill_method
        if other_pids:
            task = TerminatePIDTask(self.logic, other_pids, kill_method)
            task.run()

    @staticmethod
    def format_pids(pids: int | Iterable[int]):
        if isinstance(pids, int):
            return (pids,)
        return tuple(pids)

    def split_current_pid(self, pids):
        """Check if pids contains current_pid and return the rest."""
        if self.current_pid in pids:
            self.change.emit('Cannot terminate the current process(form pid)')
            print('Cannot terminate the current process(form pid)')
        other_pids = [pid for pid in pids if pid != self.current_pid]
        return other_pids


class TerminateProcessAdapter(QObject):
    """Terminate process, rely on PID adapter"""
    change = Signal(str)

    def __init__(self, logic, current_process_name, pid_adapter: TerminatePIDAdapter, /):
        super().__init__()
        self.logic = logic
        self.pid_adapter = pid_adapter
        self.current_process_name = current_process_name

    def run_async(self, process_name):
        # if process_name == self.current_process_name:
        #     self.change.emit('Cannot terminate the current process')
        #     print('Cannot terminate the current process')
        #     return

        pids = self.logic.get_pid_from_process_name(process_name)
        if pids:
            self.pid_adapter.run_async(pids)
        else:
            print(f'Invalid pids: {pids}')

    def run_sync(self, process_name):
        # if process_name == self.current_process_name:
        #     self.change.emit('Cannot terminate the current process')
        #     return

        pids = self.logic.get_pid_from_process_name(process_name)
        self.pid_adapter.run_sync(pids)