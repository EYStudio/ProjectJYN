import threading
from dataclasses import dataclass
from typing import Callable

from projectjyn.studentmain_subsystem.monitor import Monitor


class MonitorManager:
    def __init__(self):
        self._tasks: dict[str, MonitorTask] = {}
        self._lock = threading.Lock()

    def register(
            self,
            name: str,
            monitor: Monitor,
            callback: Callable[[object], None],
            interval: float,
    ):
        if interval <= 0:
            raise ValueError("interval must be greater than 0")

        with self._lock:
            if name in self._tasks:
                raise ValueError(
                    f"Monitor already registered: {name}"
                )

            self._tasks[name] = MonitorTask(
                monitor=monitor,
                interval=interval,
                callback=callback
            )

    def start(self, name: str):
        with self._lock:
            task = self._tasks[name]

        task.start()

    def stop(self, name: str):
        with self._lock:
            task = self._tasks[name]

        task.stop()

    def start_all(self):
        with self._lock:
            tasks = list(self._tasks.values())

        for task in tasks:
            task.start()

    def stop_all(self):
        with self._lock:
            tasks = list(self._tasks.values())

        for task in tasks:
            task.stop()

    def is_running(self, name: str) -> bool:
        with self._lock:
            task = self._tasks[name]

        return task.is_running()


@dataclass
class MonitorTask:

    def __init__(self, monitor, interval, callback):
        self.monitor = monitor
        self.interval = interval
        self.callback = callback

        self._stop_event = threading.Event()
        self._thread = None

    def start(self):
        if self.is_running():
            return

        self._stop_event.clear()

        # noinspection PyAttributeOutsideInit
        self._thread = threading.Thread(
            target=self._run,
            daemon=True,
        )
        self._thread.start()

    def stop(self):
        self._stop_event.set()

    def is_running(self) -> bool:
        return (
                self._thread is not None
                and self._thread.is_alive()
        )

    def _run(self):
        while not self._stop_event.is_set():
            try:
                result = self.monitor.poll()
                self.callback(result)
            except Exception:
                # log
                pass

            self._stop_event.wait(self.interval)
