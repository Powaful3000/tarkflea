import random
from time import sleep, time
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image
from python_imagesearch.imagesearch import imagesearcharea
from windowcapture import WindowCapture
import mss

# IMPORTANT (0 if only one monitor, I have a 21:9 2560x1080 monitor so I set to 2560.  Thank imagesearch for being trash.)
leftMonitorsOffset: int = 2560
DownMonitorsOffset: int = 0  # IMPORTANT (same shit as before)
gameBorderH: int = 16
gameBorderV: int = 39
posOffer = (946, 100)  # Client Coords
posOK = (512, 398)  # Client Coords
posBOT = (420, 300)  # Client Coords
tarkPos = (10, 10)  # doesnt really matter
ScriptEnabled = True
sleepDurRange = [0.0001, 0.0005]
sleepDur = 0.001
countSurch = 0
surchTime = 0
failPause = 0  # SECONDS
offerPause = 0
startTime = time()
WinCap = WindowCapture("EscapeFromTarkov")
sct = mss.mss()

# includes size of borders and header
tarkSize = (1024+gameBorderH, 768+gameBorderV)
tarkHANDLE = None


def fastScreenshot(hwnd, width, height):
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


def generateRandomDuration():
    global sleepDur
    sleepDur = random.uniform(sleepDurRange[0], sleepDurRange[1])


def click(HANDLE, x: int, y: int):
    win32api.SetCursorPos(win32gui.ClientToScreen(HANDLE, (x, y)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    sleep(sleepDur)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def pressKey(VK_CODE, duration_press_sec):
    win32api.keybd_event(VK_CODE, 0, 0, 0)
    sleep(duration_press_sec)
    win32api.keybd_event(VK_CODE, 0, win32con.KEYEVENTF_KEYUP, 0)


def computeAvgScans():
    global surchTime, countSurch, startTime
    avg = surchTime/countSurch
    elapsed = time() - startTime
    return ("average: " + str(avg) + "  Elapsed: " + str(elapsed))


def locateImage(file_loc, nickname, acc=0.9, callback=None):
    global surchTime, countSurch
    countSurch += 1
    before = time()
    #img = fastScreenshot(tarkHANDLE, tarkSize[0], tarkSize[1])
    #img = WinCap.get_screenshot()
    img = sct.grab(sct.monitors[1])
    rawPos = imagesearcharea(file_loc, 0, 0, 1920, 1080, acc, img)
    after = time()
    surchTime += (after-before)
    avg = computeAvgScans()
    if (rawPos[0] != -1):
        print("I see", nickname, " ", avg)
        if callback != None:
            callback()
        return True
    return False


def spamClickY():
    for _ in range(10):
        for _ in range(10):
            click(tarkHANDLE, posOffer[0], posOffer[1])
            pressKey(0x59, sleepDur)
        pressKey(win32con.VK_F5, sleepDur)
    sleep(offerPause)


def clickFail():
    click(tarkHANDLE, posOK[0], posOK[1])
    pressKey(win32con.VK_F5, sleepDur)
    sleep(failPause)


def main():
    global tarkHANDLE
    tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")
    win32gui.MoveWindow(
        tarkHANDLE, tarkPos[0], tarkPos[1], tarkSize[0], tarkSize[1], False)
    win32gui.SetForegroundWindow(tarkHANDLE)
    pressKey(win32con.VK_F5, sleepDur)
    while(True):
        ScriptEnabled = not win32api.GetKeyState(win32con.VK_CAPITAL)
        if ScriptEnabled:
            for _ in range(10):
                generateRandomDuration()
                pressKey(win32con.VK_F5, sleepDur)
                locateImage("./search/clockimage.png",
                            "offer", 0.85, spamClickY)
                locateImage("./search/NotFound.png", "fail", 0.9, clickFail)
            locateImage("./search/BOT.png", "BOT", 0.8, exit)
        else:
            print("Paused", time())
            sleep(0.25)


main()