import ctypes
import ctypes.wintypes as wintypes
import os
import subprocess
import psutil
import pywintypes
import win32api
import win32con
import win32process

from projectjyn.core.enums import PidStatus

class Process:

    def __init__(self):
        self.native_terminator = NativeTerminator()

    @staticmethod
    def get_current_pid():
        return os.getpid()

    @staticmethod
    def get_current_process_name():
        return psutil.Process(os.getpid()).name()

    @staticmethod
    def get_process_state(process_name='studentmain.exe'):
        if not process_name.lower().endswith(".exe"):
            process_name += ".exe"

        # for proc in psutil.process_iter(['name']):
        #     if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
        #         return True

        process_iter = psutil.process_iter()
        for proc in process_iter:
            try:
                if proc.name().lower() == process_name.lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        return False

    @staticmethod
    def taskkill(process_name):
        state = subprocess.run(['TASKKILL', '-F', '-IM', process_name, '-T']).returncode

        if state == 0:
            return True
            # self.logger.info(f'The process ({process_name}) has been terminated (Return code {state})')

        elif state == 128:
            return False

        elif state == 1:
            return False

        else:
            return False

    @staticmethod
    def get_pid_from_process_name(process_name):
        """
        Get the PID(s) of a process by name.
        :returns: a tuple of PIDs, or None if not found.
        """
        if not process_name.lower().endswith(".exe"):
            process_name += ".exe"

        target = process_name.lower()
        pid_list = []

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == target:
                    pid_list.append(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return tuple(pid_list) or None

    @staticmethod
    def get_pid_by_name(process_name):
        pids = win32process.EnumProcesses()
        for pid in pids:
            try:
                # noinspection PyUnresolvedReferences
                h_process = win32api.OpenProcess(0x0400 | 0x0010, False, pid)  # QUERY_INFORMATION | VM_READ
                exe_name = win32process.GetModuleFileNameEx(h_process, 0)
                if exe_name.lower().endswith(process_name.lower()):
                    return pid
            except pywintypes.error as err:  # type: ignore
                # Insufficient permissions, permission denied or the process has exited
                print(f"pywintypes.error for PID {pid}: {err}")
                continue
            except OSError as err:
                print(f"OSError for PID {pid}: {err}")
                continue
            except Exception as err:
                print(f"Unexpected error for PID {pid}: {err}")
                continue
            return None

    @staticmethod
    def get_pids_by_path(target_path):
        """
        Return all PIDs whose executable path matches target_path.
        Returns a tuple of PIDs, or None if no match.
        """
        target_path = os.path.abspath(target_path).lower()
        pid_list = []

        for proc in psutil.process_iter(['pid', 'exe']):
            try:
                exe_path = proc.info['exe']
                if exe_path and exe_path.lower() == target_path:
                    pid_list.append(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return tuple(pid_list) or None

    @staticmethod
    def pid_exists(pid: int) -> PidStatus:
        try:
            p = psutil.Process(pid)
            p.status()
            return PidStatus.EXISTS
        except psutil.NoSuchProcess:
            return PidStatus.NOT_EXISTS
        except psutil.AccessDenied:
            return PidStatus.ACCESS_DENIED
        except OverflowError:
            return PidStatus.ERROR

    @staticmethod
    def terminate_process(pid: int, exit_code=1):
        print('TERMINATE PROCESS')
        h_process = None
        try:
            # noinspection PyUnresolvedReferences
            h_process = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, pid)
        except pywintypes.error as err:  # type: ignore
            print(err)
        except Exception as err:
            print(err)

        print(f'Value of h_process: {h_process}')
        if not h_process:
            # noinspection PyUnresolvedReferences
            print(f"OpenProcess failed, error={win32api.GetLastError()}")

            # noinspection PyUnresolvedReferences
            raise RuntimeError(f"OpenProcess failed, error={win32api.GetLastError()}")
        else:
            # noinspection PyUnresolvedReferences
            win32api.TerminateProcess(h_process, exit_code)

        # h_process = win32api.OpenProcess(win32con.PROCESS_TERMINATE | win32con.SYNCHRONIZE, False, pid)
        # if not h_process:
        #     raise Exception(f"OpenProcess failed, error={win32api.GetLastError()}")
        #
        # success = win32api.TerminateProcess(h_process, 1)
        # if not success:
        #     raise Exception(f"TerminateProcess failed, error={win32api.GetLastError()}")
        #
        # result = win32event.WaitForSingleObject(h_process, 5000)
        # if result == win32event.WAIT_OBJECT_0:
        #     exit_code = win32process.GetExitCodeProcess(h_process)
        #     print(f"Process terminated with exit code {exit_code}")
        # else:
        #     print("Timeout waiting for process to terminate")

    # # load kernel32.dll
    # kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    #
    # # Define Function Prototype
    # TerminateThread = kernel32.TerminateThread
    # TerminateThread.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    # TerminateThread.restype = wintypes.BOOL
    #
    # TerminateProcess = kernel32.TerminateProcess
    # TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
    # TerminateProcess.restype = wintypes.BOOL
    #
    # PROCESS_TERMINATE = 0x0001
    # OpenProcess = kernel32.OpenProcess
    # OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    # OpenProcess.restype = wintypes.HANDLE
    #
    # pid = 1234
    # hProcess = OpenProcess(PROCESS_TERMINATE, False, pid)
    #
    # if hProcess:
    #     result = TerminateProcess(hProcess, 1)  # return code 1
    #     print("TerminateProcess result:", result)
    # else:
    #     print("Failed to open process")

    def nt_terminate_process(self, pid: int):
        print('NT TERMINATE PROCESS')
        try:
            self.native_terminator.terminate(pid)
        except RuntimeError as err:
            print(err)
            return False
        else:
            return True

    @staticmethod
    def is_suspended(pid: int):
        """
        whether the certain programme is suspended
        :param pid: pid of programme
        :return: whether the certain programme is suspended
        """
        try:
            p = psutil.Process(pid)
            return p.status() == psutil.STATUS_STOPPED
        except psutil.NoSuchProcess:
            return False

    @staticmethod
    def suspend_process(pid: int):
        try:
            p = psutil.Process(pid)
            p.suspend()
            return True
        except psutil.NoSuchProcess:
            print("Process not found")
            return False
        except PermissionError:
            print('Permission Error in suspending')
            return False

    @staticmethod
    def resume_process(pid: int):
        try:
            p = psutil.Process(pid)
            p.resume()
            return True
        except psutil.NoSuchProcess:
            print("Process not found")
            return False
        except PermissionError:
            print('Permission Error in resuming')
            return False


class NativeTerminator:
    PROCESS_TERMINATE = 0x0001
    NTSTATUS = wintypes.LONG

    def __init__(self):
        self.ntdll = ctypes.WinDLL("ntdll")
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

        self.NtTerminateProcess = self.ntdll.NtTerminateProcess
        self.NtTerminateProcess.argtypes = [wintypes.HANDLE, self.NTSTATUS]
        self.NtTerminateProcess.restype = self.NTSTATUS

        self.RtlNtStatusToDosError = self.ntdll.RtlNtStatusToDosError
        self.RtlNtStatusToDosError.argtypes = [self.NTSTATUS]
        self.RtlNtStatusToDosError.restype = wintypes.DWORD

        self.OpenProcess = self.kernel32.OpenProcess
        self.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        self.OpenProcess.restype = wintypes.HANDLE

        self.CloseHandle = self.kernel32.CloseHandle
        self.CloseHandle.argtypes = [wintypes.HANDLE]
        self.CloseHandle.restype = wintypes.BOOL

    @staticmethod
    def win_error():
        err = ctypes.get_last_error()
        msg = ctypes.FormatError(err)
        return err, msg

    def terminate(self, pid, exit_code=1):
        h_process = self.OpenProcess(self.PROCESS_TERMINATE, False, pid)
        if not h_process:
            err, msg = self.win_error()
            raise RuntimeError(f"OpenProcess failed: {err} ({msg})")

        status = self.NtTerminateProcess(h_process, exit_code)

        self.CloseHandle(h_process)

        if status != 0:
            win32_err = self.RtlNtStatusToDosError(status)
            raise RuntimeError(
                f"NtTerminateProcess failed: NTSTATUS=0x{status:08X}, "
                f"Win32Error={win32_err}"
            )
        else:
            print(f"NTSTATUS = 0x{status:08X}")

        return True


# self.floatwin.setText(
#     f"窗口标题：{GetWindowText(hwnd)}\n窗口类名：{GetClassName(hwnd)}\n窗口位置：{str(GetWindowRect(hwnd))}\n窗口句柄：{int(hwnd)}\n窗口进程：{procname}")
