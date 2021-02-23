import configparser as CP
import random
import sys
from time import sleep, time
import win32api
import win32con
import win32gui
import numpy
import cv2
import pywintypes
import datetime
import ScreenshotMachine as sm


def imagesearcharea(template, precision=0.8, im=None):
    if im is None:
        print("fuck")
        return

    img_rgb = numpy.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


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
    return ("O:F " + computeAvgOF() + " Average time to search screen: " + f"{avg:.5f}" + "s  " + f"{(1/avg):.1f}" + " FPS  " + " Elapsed: " + str(datetime.timedelta(seconds=elapsed)) + "s")


def spamClickY():
    global offerTotal
    offerTotal += 1
    for _ in range(10):
        for _ in range(10):
            click(posOffer[0], posOffer[1])
            pressKey(0x59, sleepDur)
    sleep(OFFERPAUSE)
    clickF5()


def clickFail():
    global failTotal
    failTotal += 1
    click(posOK[0], posOK[1])
    sleep(0.1)
    sleep(FAILPAUSE)
    clickF5()


def clickF5():
    global lastF5
    now = time()
    if (now-lastF5 > 5):
        pressKey(win32con.VK_F5, sleepDur)
        lastF5 = now
    else:
        click(posF5[0], posF5[1])


def foundBot():
    global config
    if not TURBO_MODE:
        choice = random.choice(list(config['DEFAULT']))
        config.set("DEFAULT", choice, str(
            float(config["DEFAULT"][choice])+(float(config["DEFAULT"][choice]*1.1))))
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
    exit()


def locateImages() -> bool:
    global surchTime, countSurch, machine
    countSurch += 1
    before = time()
    img = machine.getLatest()
    after = time()
    surchTime += (after-before)
    end = ('\n', '\r')[lineReplace]
    for i in images:
        rawPos = imagesearcharea(
            i[0], i[2], img)

        if (rawPos is not None and rawPos[0] != -1):
            avg = printAvgScans()
            print("I saw", i[1], "\t", avg, end=end)
            eval(i[3])
            return True
        else:
            avg = printAvgScans()
            print("I saw", "None", " ", avg, end=end)
    return False


def gen(img_loc):
    gray = cv2.cvtColor(cv2.imread(img_loc), cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    return (gray, keypoints, descriptors)


images = [[gen("./search/NotFound.png"),     "fail",     0.8,    "clickFail()"],
          [gen("./search/clockImage.png"),   "offer",    0.85,   "spamClickY()"],
          [gen("./search/BOT.png"),          "BOT",      0.8,    "foundBot()"]]


def main():
    global TURBO_MODE, FAILPAUSE, OFFERPAUSE, LOOPSLEEPDUR, startTime, tarkHANDLE, bf, sift, images, config, numLoops, machine, MonitorsOffset, DownMonitorsOffset, posOffer, posBOT, posOK, posF5, leftMonitorsOffset, sleepDurRange, sleepDur, countSurch, surchTime, lastF5, offerTotal, failTotal, lineReplace

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
    tarkPos = (0, 0)  # doesnt really matter
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
    lineReplace = False
    numLoops = 2
    # includes size of borders and header
    tarkSize = (1024 + gameBorderH, 768 + gameBorderV)
    tarkHANDLE = tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    sift = cv2.SIFT_create()
    images = None

    machine = sm.ScreenshotMachine()
    if not TURBO_MODE:
        config = CP.ConfigParser({'DEFAULT': 'failpause'})
        config.read("settings.ini")
        try:
            a = config["DEFAULT"]
            FAILPAUSE = int(a["FAILPAUSE"])
            OFFERPAUSE = int(a["OFFERPAUSE"])
            LOOPSLEEPDUR = int(a["LOOPSLEEPDUR"])
        except:
            pass
    else:
        FAILPAUSE = 0
        OFFERPAUSE = 0
        LOOPSLEEPDUR = 1

    try:
        win32gui.MoveWindow(
            tarkHANDLE, tarkPos[0], tarkPos[1], tarkSize[0], tarkSize[1], False)
    except pywintypes.error as e:
        print("Can't find tarkov window.", e)
        exit()
    win32gui.SetForegroundWindow(tarkHANDLE)
    Now = None
    sys.stdout.flush()
    while True:
        ScriptEnabled = not win32api.GetKeyState(win32con.VK_CAPITAL)
        if ScriptEnabled:
            generateRandomDuration()
            clickF5()
            preLoopTime = time()
            for _ in range(round(numLoops)):
                if locateImages():
                    break
            numLoops += time() - preLoopTime - LOOPSLEEPDUR
        else:
            if Now is None:
                Now = time()
            print("Paused", str(time()-Now)[0:6], end='\r')


if __name__ == "__main__":
    main()
