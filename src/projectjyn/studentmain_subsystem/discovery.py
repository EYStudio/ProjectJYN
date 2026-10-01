import threading


class StudentmainDiscovery:
    KEY_PATH = r"SOFTWARE\TopDomain\e-Learning Class Standard\1.00"
    VALUE_NAME = "TargetDirectory"

    def __init__(self, logic):
        self.logic = logic

    def find(self):
        return self.logic.read_registry_value(
            self.KEY_PATH,
            self.VALUE_NAME,
        )

class StudentmainLookup:
    def __init__(self, logic, callback):
        self.callback = callback
        self.discovery = StudentmainDiscovery(logic)
        self.path = None
        self.stop_event = threading.Event()

    def lookup(self):
        while not self.stop_event.is_set():
            self.path = self.discovery.find()
            if self.path:
                self.callback(self.path)
                break

            self.stop_event.wait(0.75)

    def stop(self):
        self.stop_event.set()


class StudentmainContext:
    def __init__(self):
        self.path = None

    @property
    def available(self):
        return self.path is not None
