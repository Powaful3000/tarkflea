import random
from time import sleep, time
#import threading
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image
from python_imagesearch.imagesearch import imagesearcharea
import configparser as CP


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
failPause = 60  # SECONDS
offerPause = 60
gayRetard = 25
startTime = time()

# includes size of borders and header
tarkSize = (1024+gameBorderH, 768+gameBorderV)
tarkHANDLE = tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")


config = CP.ConfigParser({'cum': 'failPause'})
config.read("settings.ini")
try:
    failPause = int(config["cum"]["failPause"])
    offerPause = int(config["cum"]["offerPause"])
    gayRetard = int(config["cum"]["gayRetard"])
except:
    pass

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


def click(x: int, y: int):
    win32api.SetCursorPos(win32gui.ClientToScreen(tarkHANDLE, (x, y)))
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
    img = fastScreenshot(tarkHANDLE, tarkSize[0], tarkSize[1])
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
            click(posOffer[0], posOffer[1])
            pressKey(0x59, sleepDur)
    clickF5()
    sleep(offerPause)


def clickFail():
    click(posOK[0], posOK[1])
    sleep(failPause)
    

def clickF5():
    click(posF5[0], posF5[1])

def foundBot():
    choice = random.choice(list(config['DEFAULT']))
    config.set("DEFAULT",choice,str(int(config["DEFAULT"][choice])+1))
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)
    exit()

def main():
    win32gui.MoveWindow(
        tarkHANDLE, tarkPos[0], tarkPos[1], tarkSize[0], tarkSize[1], False)
    win32gui.SetForegroundWindow(tarkHANDLE)
    clickF5()
    while(True):
        ScriptEnabled = not win32api.GetKeyState(win32con.VK_CAPITAL)
        if ScriptEnabled:
            generateRandomDuration()
            clickF5()
            locateImage("./search/clockimage.png","offer", 0.85, spamClickY)
            locateImage("./search/NotFound.png", "fail", 0.9, clickFail)
            sleep(0.5)
            locateImage("./search/BOT.png", "BOT", 0.8, foundBot)
        else:
            print("Paused", time())
            sleep(0.25)
            return

main()