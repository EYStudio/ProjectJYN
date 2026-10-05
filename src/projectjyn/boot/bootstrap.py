import sys

from projectjyn.app.constants import IS_E_CLASSROOM_STUDENTMAIN


class BootStrap:

    def __init__(self, platform):
        self.platform = platform

    def run(self):

        self.check_platform()
        self.not_studentmain_warning()

        self.check_privilege()

    def check_privilege(self):

        if self.platform.privilege.is_admin():
            print("Run as admin")

        if self.platform.privilege.request_elevation():
            sys.exit('Privilege elevated')

        print("Run without admin")

    def check_platform(self):
        """Check whether OS is Windows nt"""
        if not self.platform.system.is_windows():
            sys.exit('UNSUPPORTED SYSTEMS')

    @staticmethod
    def not_studentmain_warning():
        if not IS_E_CLASSROOM_STUDENTMAIN:
            print('CURRENT E CLASSROOM IS NOT STUDENTMAIN')
            # print('MAY CAUSE UNEXPECTED EXCEPTIONS')
            sys.exit('CURRENT E CLASSROOM IS NOT STUDENTMAIN')
