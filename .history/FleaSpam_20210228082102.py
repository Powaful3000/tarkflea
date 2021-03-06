import configparser as CP
from multiprocessing import connection
import random
import sys
from time import sleep, time
import win32api
import win32con
import win32gui
import win32ui
import multiprocessing as mp
import numpy as np
import cv2
from PIL import Image


TURBO_MODE = True

gameBorderH: int = 16
gameBorderV: int = 39
posOffer = (946, 100)  # Client Coords
posOK = (512, 398)  # Client Coords
posBOT = (420, 300)  # Client Coords
posF5 = (747, 65)
tarkPos = (0, 0)  # doesnt really matter
ScriptEnabled = True
sleepDurRange = [0.0001, 0.0005]
sleepDur = 0.0001
countSurch = 0.0
surchTime = 0.0
FAILPAUSE = 0.1  # SECONDS
OFFERPAUSE = 0
LOOPSLEEPDUR = 1
startTime = time()
lastF5 = startTime
offerTotal = 0
failTotal = 0

# includes size of borders and header
tarkSize = (1024+gameBorderH, 768+gameBorderV)
tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")


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
            img = self.fastScreenshot(tarkHANDLE, tarkSize[0], tarkSize[1])
            pipe.send(img)

    def fastScreenshot(_, hwnd, width, height) -> Image:
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (width, height), dcObj, (0, 0), win32con.SRCCOPY)
        # dataBitMap.SaveBitmapFile(cDC, 'screenshot.bmp')
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


if not TURBO_MODE:
    config = CP.ConfigParser({'DEFAULT': 'failpause'})
    config.read("settings.ini")
    FAILPAUSE = int(config["DEFAULT"]["FAILPAUSE"])
    OFFERPAUSE = int(config["DEFAULT"]["OFFERPAUSE"])
    LOOPSLEEPDUR = int(config["DEFAULT"]["LOOPSLEEPDUR"])
else:
    FAILPAUSE = 0
    OFFERPAUSE = 0
    LOOPSLEEPDUR = 1


def computeAvgOF() -> str:
    return str(offerTotal)+"/"+str(failTotal)


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


def printAvgScans() -> str:
    global surchTime, countSurch, startTime
    avg = surchTime/countSurch
    elapsed = time() - startTime
    return ("Average O:F " + computeAvgOF() +
            " Average time to search screen: " +
            str(avg) + "  Elapsed: " + str(elapsed))


def spamClickY():
    global offerTotal
    offerTotal += 1
    for _ in range(10):
        for _ in range(10):
            click(posOffer[0], posOffer[1])
            pressKey(0x59, sleepDur)
    sleep(max(OFFERPAUSE, 0.1))
    clickF5()


def clickFail():
    global failTotal
    failTotal += 1
    click(posOK[0], posOK[1])
    sleep(FAILPAUSE)
    clickF5()


def clickF5():
    global lastF5
    now = time()
    if (now-lastF5 > 5):
        pressKey(win32con.VK_F5, sleepDur)
        lastF5 = now
    click(posF5[0], posF5[1])


def foundBot():
    if not TURBO_MODE:
        choice = random.choice(list(config['DEFAULT']))
        config.set("DEFAULT", choice, str(
            float(config["DEFAULT"][choice]) +
            (float(config["DEFAULT"][choice]*1.1))))
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
    exit()


def imagesearcharea(smallLoc, precision=0.8, big=None):
    img_rgb = np.array(big)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(smallLoc, 0)
    if template is None:
        raise FileNotFoundError('Image file not found: {}'.format(smallLoc))

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    max_val: float
    max_loc: list
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


def locateImages(machine: ScreenshotMachine, file_loc: tuple,
                 nickname: tuple, acc=(0.9), callback: tuple = None):
    global surchTime, countSurch
    countSurch += 1
    before = time()
    img = machine.getLatest()
    after = time()
    surchTime += (after-before)
    for i in range(len(file_loc)):
        rawPos = imagesearcharea(file_loc[i], acc[i], img)
        avg = printAvgScans()
        if (rawPos[0] != -1):
            print("I saw", nickname[i], " ", avg, end='\r')
            if callback is not None:
                callback[i]()


def main():
    machine = ScreenshotMachine()
    win32gui.MoveWindow(
        tarkHANDLE, tarkPos[0], tarkPos[1], tarkSize[0], tarkSize[1], False)
    win32gui.SetForegroundWindow(tarkHANDLE)
    Now = None
    sys.stdout.flush()
    while(True):
        ScriptEnabled = not win32api.GetKeyState(win32con.VK_CAPITAL)
        if ScriptEnabled:
            generateRandomDuration()
            clickF5()
            for _ in range(10):
                locateImages(machine, ("./search/clockImage.png",
                                       "./search/NotFound.png",
                                       "./search/BOT.png"),
                             ("offer", "fail", "BOT"),
                             (0.85, 0.8, 0.8),
                             (spamClickY, clickFail, foundBot))
            sleep(LOOPSLEEPDUR)
        else:
            if Now is None:
                Now = time()
            print("Paused", str(time()-Now)[0:6], end='\r')


if __name__ == "__main__":
    main()
