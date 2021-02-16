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

tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")
gameBorderH: int = 16
gameBorderV: int = 39
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


def ssLoop(ss: mp._Value):
    while True:
        ss.acquire()
        ss.value


if __name__ == "__main__":
    ss = mp.Value(Image, fastScreenshot())
