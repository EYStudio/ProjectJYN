import ctypes
import os
import sys
import time

from projectJYN import IS_E_CLASSROOM_STUDENTMAIN


class PJYNBootStrap:
    def __init__(self):
        self.check_operate_system()
        self.authority_admin = self.is_admin()
        if not self.authority_admin:
            if self.privilege_escalation():
                time.sleep(3)
                sys.exit()
            else:
                print("Run without admin")
        else:
            print('Run as admin')
        self.not_studentmain_warning()

    @staticmethod
    def check_operate_system():
        """Check whether OS is Windows nt"""
        if os.name != 'nt':
            sys.exit('UNSUPPORTED SYSTEMS')

    @staticmethod
    def is_admin():
        """Checking whether programme has administrator privilege"""

        authority = ctypes.windll.shell32.IsUserAnAdmin()
        return bool(authority)

    @staticmethod
    def privilege_escalation():
        """
        Try to rerun script as admin
        Uses ShellExecuteW with "runas"
        :return: True if elevation succeeded, False otherwise
        """
        result = ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', sys.executable, ' '.join(sys.argv), None, 1
        )
        return result > 32

    @staticmethod
    def not_studentmain_warning():
        if not IS_E_CLASSROOM_STUDENTMAIN:
            print('CURRENT E CLASSROOM IS NOT STUDENTMAIN')
            print('MAY CAUSE UNEXPECTED EXCEPTIONS')
