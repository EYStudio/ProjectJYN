from .process import Process
from .registry import Registry
from .shell import Shell
from .system import System
from .window import Window


class Platform:
    def __init__(self):
        self.process = Process()
        self.registry = Registry()
        self.shell = Shell()
        self.system = System()
        self.window = Window()