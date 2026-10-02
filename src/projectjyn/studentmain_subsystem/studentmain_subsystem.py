from discovery import StudentmainContext, StudentmainLookup, StudentmainDiscovery
from projectjyn.studentmain_subsystem.manager import MonitorManager
from projectjyn.studentmain_subsystem.monitor import ProcessMonitor, SuspendMonitor, StudentmainPasswordMonitor


class StudentmainSubsystem:
    def __init__(self, logic, dispatcher):
        self.logic = logic

        self.context = StudentmainContext()

        self._dispatcher = dispatcher

        self._lookup = StudentmainLookup(
            logic=logic,
            callback=self._on_studentmain_found,
        )

        self._manager = MonitorManager()

        self._started = False

    # def start(self):
    #     if self._started:
    #         return
    #
    #     self._started = True
    #
    #     self._dispatcher.submit(
    #         self._lookup.lookup
    #     )

    # def stop(self):
    #     if not self._started:
    #         return
    #
    #     self._lookup.stop()
    #
    #     self._started = False

    def start(self):
        if self._started:
            return

        self._started = True

        self._manager.register(
            'discovery',
            StudentmainDiscovery(self.logic),
            self._on_studentmain_found,
            0.75
        )

        self._manager.start('discovery')


    def stop(self):
        if not self._started:
            return

        self._manager.stop_all()

        self._started = False

    def _on_studentmain_found(self, path):
        self.context.path = path

        self._manager.stop('discovery')

        # todo: save path

        self._start_components()

    def _start_components(self):
        self._manager.register('process', ProcessMonitor(self.logic), lambda x: print(x), 0.5)
        self._manager.register('process', SuspendMonitor(self.logic), lambda x: print(x), 0.5)
        self._manager.register('process', StudentmainPasswordMonitor(self.logic), lambda x: print(x), 0.5)
