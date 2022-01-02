import configparser as CP
from multiprocessing import connection
import random
import sys
from time import sleep, time
from typing import KeysView
import win32api
import win32con
import win32gui
import win32ui
import multiprocessing as mp
import numpy as np
import cv2
from PIL import Image
import math
import os
import signal

class KeyState:
    parentConn: connection.Connection
    childConn: connection.Connection
    proc: mp.Process

    def __init__(self):
        self.parentConn, self.childConn = mp.Pipe()
        self.proc = mp.Process(target=self.grabLoop, args=(self.childConn,))
        self.proc.start()
        
    def die(self):
        self.proc.terminate()
        
    def scriptEnabled(self) -> bool:
        return self.parentConn.recv()
    
    def grabLoop(self, pipe: connection.Connection):
        while True:
            if (win32api.GetKeyState(win32con.VK_INSERT)):
                os.kill(os.getppid(), signal.SIGTERM)
            ScriptEnabled = not win32api.GetKeyState(win32con.VK_CAPITAL)
            pipe.send(ScriptEnabled)
            sleep(0.1)
            
    
class ScreenshotMachine:
    gameBorderH: int = 16
    gameBorderV: int = 39
    tarkSize = (1024+gameBorderH, 768+gameBorderV)
    parentConn: connection.Connection
    childConn: connection.Connection
    proc: mp.Process

    def __init__(self):
        self.parentConn, self.childConn = mp.Pipe()
        self.proc = mp.Process(target=self.grabLoop, args=(self.childConn,))
        self.proc.start()

    def die(self):
        self.proc.terminate()

    def getLatest(self) -> connection.Connection:
        return self.parentConn.recv()

    def grabLoop(self, pipe: connection.Connection):
        tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")
        while True:
            img = self.fastScreenshot(tarkHANDLE)
            pipe.send(img)
            sleep(0.01)

    def fastScreenshot(_, hwnd) -> Image:

        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top


        hdesktop = win32gui.GetDesktopWindow()
        hwndDC = win32gui.GetWindowDC(hdesktop)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hdesktop, hwndDC)

        # if result == None:
        #     #PrintWindow Succeeded
        #     im.save("test.png")
        return im