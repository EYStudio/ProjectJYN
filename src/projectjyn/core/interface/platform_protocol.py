from typing import Protocol


class ProcessProtocol(Protocol):
    pass


class RegistryProtocol(Protocol):
    pass


class ShellProtocol(Protocol):

    @staticmethod
    def start_file(file_path) -> bool:
        """start file form path"""
        ...


class SystemProtocol(Protocol):
    pass


class WindowProtocol(Protocol):
    pass


class PlatformProtocol(Protocol):

    @property
    def process(self) -> ProcessProtocol:
        ...

    @property
    def registry(self) -> RegistryProtocol:
        ...

    @property
    def shell(self) -> ShellProtocol:
        ...

    @property
    def system(self) -> SystemProtocol:
        ...

    @property
    def window(self) -> WindowProtocol:
        ...
