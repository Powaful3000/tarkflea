import multiprocessing as mp
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

TURBO_MODE = False

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
tarkHANDLE = tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")
tarkSize = (1024+gameBorderH, 768+gameBorderV)


def fastScreenshot():
    global tarkHANDLE
    global tarkSize
    wDC = win32gui.GetWindowDC(tarkHANDLE)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, tarkSize[0], tarkSize[1])
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (tarkSize[0], tarkSize[1]),
               dcObj, (0, 0), win32con.SRCCOPY)
    bmpinfo = dataBitMap.GetInfo()
    bmpstr = dataBitMap.GetBitmapBits(True)
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(tarkHANDLE, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    return im


def ssLoop(ss):
    while True:
        ss.acquire()
        ss.value = fastScreenshot()
        ss.release()


def computeAvgScans():
    global surchTime, countSurch, startTime
    avg = surchTime/countSurch
    elapsed = time() - startTime
    return ("Average O:F " + computeAvgOF() + " Average time to search screen: " + str(avg) + "  Elapsed: " + str(elapsed))


def locateImage(file_loc, nickname, acc=0.9, callback=None):
    global surchTime, countSurch
    countSurch += 1
    before = time()
    img = fastScreenshot(tarkHANDLE, tarkSize[0], tarkSize[1])
    rawPos = imagesearcharea(file_loc, 0, 0, 1920, 1080, acc, img)
    after = time()
    surchTime += (after-before)
    avg = computeAvgScans()
    if (rawPos[0] != -1):
        print("I saw", nickname, " ", avg, end='\r')
        if callback != None:
            callback()
        return True
    return False


if __name__ == "__main__":
    ss = mp.Value()
