import configparser as CP
import random
import sys
from time import sleep, time
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image
from python_imagesearch.imagesearch import imagesearcharea
import multiprocessing as mp
import mss
import mss.tools

TURBO_MODE = True

# IMPORTANT (0 if only one monitor, I have a 21:9 2560x1080 monitor so I set to 2560.  Thank imagesearch for being trash.)
leftMonitorsOffset: int = 2560
DownMonitorsOffset: int = 0  # IMPORTANT (same shit as before)
gameBorderH: int = 16
gameBorderV: int = 39
posOffer = (946, 100)  # Client Coords
posOK = (512, 398)  # Client Coords
posBOT = (420, 300)  # Client Coords
posF5 = (747, 65)
tarkPos = (10, 10)  # doesnt really matter
ScriptEnabled = True
sleepDurRange = [0.0001, 0.0005]
sleepDur = 0.0001
countSurch = 0
surchTime = 0
FAILPAUSE = 30  # SECONDS
OFFERPAUSE = 30
LOOPSLEEPDUR = 1
startTime = time()
lastF5 = startTime
offerTotal = 0
failTotal = 0

# includes size of borders and header
tarkSize = (1024+gameBorderH, 768+gameBorderV)
tarkHANDLE = tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")


class ScreenshotMachine:
    gameBorderH: int = 16
    gameBorderV: int = 39
    tarkSize = (1024+gameBorderH, 768+gameBorderV)
    latestImg = None

    def __init__(self):
        parentConn, childConn = mp.Pipe()
        proc = mp.Process(target=self.grabLoop, args=(childConn,))
        proc.start()
        proc.join()
        while True:
            if (parentConn.poll()):
                self.latestImg5 = parentConn.recv()

    def grabLoop(self, pipe):
        tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")
        while True:
            img = self.fastScreenshot(tarkHANDLE, tarkSize[0], tarkSize[1])
            pipe.send(img)

    def fastScreenshot(_, hwnd, width, height):
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (width, height), dcObj, (0, 0), win32con.SRCCOPY)
        #dataBitMap.SaveBitmapFile(cDC, 'screenshot.bmp')
        bmpinfo = dataBitMap.GetInfo()
        bmpstr = dataBitMap.GetBitmapBits(True)
        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        return im


if __name__ == "__main__":
    machine = ScreenshotMachine()
    time.sleep(1)
    print(machine.latestImg)
