import ctypes
import ctypes.wintypes as wintypes


class _ThreadEntry32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ThreadID", wintypes.DWORD),
        ("th32OwnerProcessID", wintypes.DWORD),
        ("tpBasePri", wintypes.LONG),
        ("tpDeltaPri", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
    ]

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



class ThreadTerminator:
    TH32CS_SNAPTHREAD = 0x00000004
    THREAD_TERMINATE = 0x0001
    ERROR_NO_MORE_FILES = 18
    INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value

    def __init__(self):
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.snapshot_threads = self.kernel32.CreateToolhelp32Snapshot
        self.snapshot_threads.argtypes = [wintypes.DWORD, wintypes.DWORD]
        self.snapshot_threads.restype = wintypes.HANDLE

        self.first_thread = self.kernel32.Thread32First
        self.next_thread = self.kernel32.Thread32Next
        for enumerate_thread in (self.first_thread, self.next_thread):
            enumerate_thread.argtypes = [wintypes.HANDLE, ctypes.POINTER(_ThreadEntry32)]
            enumerate_thread.restype = wintypes.BOOL

        self.open_thread = self.kernel32.OpenThread
        self.open_thread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        self.open_thread.restype = wintypes.HANDLE

        self.terminate_thread = self.kernel32.TerminateThread
        self.terminate_thread.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        self.terminate_thread.restype = wintypes.BOOL

        self.close_handle = self.kernel32.CloseHandle
        self.close_handle.argtypes = [wintypes.HANDLE]
        self.close_handle.restype = wintypes.BOOL

    def terminate(self, pid: int, exit_code: int = 1) -> bool:
        """Terminate matching snapshot threads and return False on any API failure.

        Arguments are validated by the caller. No matching threads returns False.
        """
        snapshot = self.snapshot_threads(self.TH32CS_SNAPTHREAD, 0)
        if snapshot == self.INVALID_HANDLE_VALUE or not snapshot:
            return False

        found = False
        success = True
        entry = _ThreadEntry32()
        entry.dwSize = ctypes.sizeof(entry)
        # owner_size = _ThreadEntry32.th32OwnerProcessID.offset + ctypes.sizeof(wintypes.DWORD)
        try:
            if not self.first_thread(snapshot, ctypes.byref(entry)):
                return False

            while True:
                # 默认 windows api 返回正确

                # if entry.dwSize < owner_size:
                #     success = False
                # elif entry.th32OwnerProcessID == pid:
                if entry.th32OwnerProcessID == pid:
                    found = True
                    thread = self.open_thread(self.THREAD_TERMINATE, False, entry.th32ThreadID)
                    if not thread:
                        success = False
                    else:
                        try:
                            if not self.terminate_thread(thread, exit_code):
                                success = False
                        finally:
                            if not self.close_handle(thread):
                                success = False

                entry.dwSize = ctypes.sizeof(entry)
                if not self.next_thread(snapshot, ctypes.byref(entry)):
                    if ctypes.get_last_error() != self.ERROR_NO_MORE_FILES:
                        success = False
                    break
        finally:
            if not self.close_handle(snapshot):
                success = False

        return found and success