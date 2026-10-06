import threading

from monitor import Monitor


class StudentmainDiscovery(Monitor):
    """
    Studentmain 的一次性发现服务。

    负责从系统注册表中读取 Studentmain 的安装目录。
    本身不负责轮询，也不负责保存发现结果。
    """

    KEY_PATH = r"SOFTWARE\TopDomain\e-Learning Class Standard\1.00"
    VALUE_NAME = "TargetDirectory"

    def __init__(self, logic):
        self.logic = logic

    def poll(self):
        """
        尝试查找 Studentmain。

        Returns:
            Studentmain 的路径；如果当前无法找到，则返回 None。
        """
        return self.logic.read_registry_value(
            self.KEY_PATH,
            self.VALUE_NAME,
        )


# deprecated
class StudentmainLookup:
    """
    持续查找 Studentmain 的轮询器。

    Discovery 只负责执行一次查找，而 Lookup 负责在
    Studentmain 尚未出现时周期性地重复查找。

    找到 Studentmain 后，通过 callback 将结果通知给上层，
    随后结束自身的查找任务。
    """

    def __init__(self, logic, callback):
        self.callback = callback
        self.discovery = StudentmainDiscovery(logic)

        self.path = None

        self.stop_event = threading.Event()

    def lookup(self):
        """
        持续查找 Studentmain，直到找到或收到停止请求。

        该方法是阻塞的，因此应由后台任务执行机制运行，
        不应直接在 Application 的主线程中调用。
        """
        while not self.stop_event.is_set():
            self.path = self.discovery.poll()

            if self.path:
                self.callback(self.path)
                break

            self.stop_event.wait(0.75)

    def stop(self):
        self.stop_event.set()


class StudentmainContext:
    """
    Studentmain 子系统的运行时上下文。

    保存当前发现到的 Studentmain 信息。
    """

    def __init__(self):
        # 当前 Studentmain 的路径。
        # None 表示当前尚未发现 Studentmain。
        self.path = None

    @property
    def available(self):
        """
        返回当前是否已经发现 Studentmain。
        """
        return self.path is not None
