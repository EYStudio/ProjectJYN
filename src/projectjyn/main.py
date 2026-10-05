from projectjyn.boot import BootStrap
from projectjyn.platform import Platform


class ProjectJYNMain:
    def __init__(self):
        print('Nothing happened')
        self.platform = Platform()
        self.bootstrap = BootStrap(self.platform)


if __name__ == "__main__":
    ProjectJYNMain()
