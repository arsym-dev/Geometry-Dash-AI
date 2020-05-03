from ctypes import *
from ctypes.wintypes import *
import struct
import win32com.client

class MemoryHooker:
    def __init__(self, pid):
        self.OpenProcess = windll.kernel32.OpenProcess
        self.ReadProcessMemory = windll.kernel32.ReadProcessMemory
        self.CloseHandle = windll.kernel32.CloseHandle
        self.shell = win32com.client.Dispatch("WScript.Shell")

        self.buffer = c_char_p(b'.'*4)
        PROCESS_ALL_ACCESS = 0x1F0FFF
        self.processHandle = self.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

    def readInt32(self, address):
        bufferSize = 4
        bytesRead = c_ulong(0)

        if self.ReadProcessMemory(self.processHandle, address, self.buffer, bufferSize, byref(bytesRead)):
            v = self.buffer.value
            while len(v) < 4:
                v = v + b'\0'
            return struct.unpack('<I', v)[0]

        return None

    def close(self):
        self.CloseHandle(self.processHandle)




# C struct redefinitions
SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

class Keyboard:
    ## List of key hex codes:
    ## http://www.flint.jp/misc/?q=dik&lang=en
    def __init__(self):
        pass

    def pressKey(self, hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
        x = Input( ctypes.c_ulong(1), ii_ )
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def releaseKey(self, hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
        x = Input( ctypes.c_ulong(1), ii_ )
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))