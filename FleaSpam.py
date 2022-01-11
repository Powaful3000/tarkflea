from PIL import Image
import win32ui
import random
import sys
from time import sleep, time
import win32api
import win32con
import win32gui
import numpy as np
import cv2
import math


def randSleep():
    sleep(generateRandomDuration())


def computeAvgOF() -> str:
    return str(offerTotal) + "/" + str(failTotal)


def generateRandomDuration():
    global sleepDur
    sleepDur = random.uniform(sleepDurRange[0], sleepDurRange[1])
    return sleepDur


def click(x: int, y: int):
    win32api.SetCursorPos(win32gui.ClientToScreen(tarkHANDLE, (x, y)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    generateRandomDuration()
    sleep(sleepDur)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def pressKey(VK_CODE, duration_press_sec):
    win32api.keybd_event(VK_CODE, 0, 0, 0)
    sleep(duration_press_sec)
    win32api.keybd_event(VK_CODE, 0, win32con.KEYEVENTF_KEYUP, 0)


def printAvgScans() -> str:
    global surchTime, countSurch, startTime, scanLoop
    avg = surchTime / countSurch
    elapsed = time() - startTime
    return (
        "Average O:F "
        + computeAvgOF()
        + " Average time to search screen: "
        + str(round(avg, 6))
        + "  Elapsed: "
        + str(round(elapsed, 6))
        + " scanLoop: "
        + str(scanLoop)
    )


def clickF5():
    global lastF5
    now = time()
    if now - lastF5 > 5:
        pressKey(win32con.VK_F5, sleepDur)
        lastF5 = now
    else:
        click(posF5[0], posF5[1])


def spamClickY(rawPos=None):
    global offerTotal, spamCount
    offerTotal += 1
    spamCount += 1
    x = posOffer[0]
    y = posOffer[1]
    if rawPos is not None:
        x, y = rawPos
    # print(spamCount, "click", x, y, rawPos)
    if spamCount >= 5:
        spamCount = 0
        clickF5()
        return
    for _ in range(20):
        click(x, y)
        # click(1140, 490)  # all button
        pressKey(0x59, sleepDur)
    sleep(max(OFFERPAUSE, 0.1))


def clickFail(rawPos=None):
    global failTotal
    failTotal += 1
    if rawPos is None:
        x, y = posOK[0], posOK[1]
    else:
        x, y = rawPos
        x += 10
        y += 10
    click(x, y)
    sleep(max(FAILPAUSE, 0.2))
    clickF5()


def foundBot():
    exit()


# TODO change to region to fullscreen search
# subrect = big[y:y+h , x:x+h]
def imagesearcharea(smallLoc, precision=0.8, big=None, region=None):
    img_rgb = np.array(big)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(smallLoc, 0)
    if template is None:
        raise FileNotFoundError("Image file not found: {}".format(smallLoc))

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    max_val: float
    max_loc: list
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if region is not None:
        max_loc[0] += region[0]
        max_loc[1] += region[1]
    if max_val < precision:
        return [-1, -1]
    print("found", smallLoc, "at", max_loc)
    return max_loc


def locateImage(file_loc, nickname, acc=0.8, callback=None, passRawPos=False, region=None):
    global surchTime, countSurch
    countSurch += 1
    before = time()
    img = fastScreenshot()
    # print(img.size)
    if region is not None:
        # print("crop", region)
        img = img.crop(region)
    # print(img.size)
    after = time()
    surchTime += after - before
    rawPosX, rawPosY = imagesearcharea(file_loc, acc, img)
    avg = printAvgScans()
    if rawPosX != -1:
        if region is not None:
            rawPosX += region[0]
            rawPosY += region[1]
        print("I saw", nickname, (rawPosX, rawPosY), avg)  # end='\r'
        if callback is not None:
            if passRawPos is not None:
                if passRawPos:
                    callback((rawPosX, rawPosY))
                else:
                    callback()
            else:
                callback()
        return True
    return False


def locateImages(file_loc: tuple, nickname: tuple, acc=(0.8), callback: tuple = None, passRawPos=None):
    global surchTime, countSurch
    countSurch += 1
    before = time()
    img = fastScreenshot()
    after = time()
    surchTime += after - before
    # print("length", len(file_loc))
    for i in range(len(file_loc)):
        checkPause()
        # print("checking for ", file_loc[i])
        rawPos = imagesearcharea(file_loc[i], acc[i], img)
        # print(rawPos)
        avg = printAvgScans()
        if rawPos[0] != -1:
            print("I saw", nickname[i], rawPos, avg)  # end='\r'
            if callback is not None:
                if passRawPos is not None:
                    if passRawPos[i]:
                        callback[i](rawPos)
                    else:
                        callback[i]()
                        break
                else:
                    callback[i]()


def checkPause():
    if not win32api.GetKeyState(win32con.VK_CAPITAL):
        print()
        loop = 0
        while not win32api.GetKeyState(win32con.VK_CAPITAL):
            loop += 1
            print("Paused", progressSpinner[loop % 4], end="\r")
            sleep(0.1)
    return False


def fastScreenshot() -> Image:

    left, top, right, bot = win32gui.GetWindowRect(tarkHANDLE)
    w = right - left
    h = bot - top

    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer("RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)

    # if result == None:
    #     #PrintWindow Succeeded
    #     im.save("test.png")
    return im


def doJumping():
    if r(0, 1) < 0.5:
        generateRandomDuration()
        pressKey(0x20, sleepDur)  # Spacebar


def antiAFK():
    print("Begin antiAFK")
    loop = 0
    sleep(r(1, 2))
    click(76, 1064)  # Main Menu Button
    sleep(r(1, 2))
    click(954, 868)  # Hideout Button
    sleep(r(5, 7))
    print()
    while not locateImage("./search/hideoutEnter.png", "hideoutEnter"):
        print("Waiting for Enter button", progressSpinner[loop % 4], end="\r")
        loop += 1
        sleep(0.1)
    sleep(2)
    generateRandomDuration()
    pressKey(win32con.VK_RETURN, sleepDur)
    sleep(r(5, 7))
    doJumping()
    pressKey(0x57, r(7.5, 12.5))  # W
    doJumping()
    pressKey(0x53, r(7.5, 12.5))  # S
    doJumping()
    generateRandomDuration()
    pressKey(win32con.VK_ESCAPE, sleepDur)
    sleep(r(3, 5))
    generateRandomDuration()
    pressKey(win32con.VK_ESCAPE, sleepDur)
    sleep(r(3, 5))
    click(1250, 1055)  # Flea Market Button
    sleep(r(3, 5))
    return


def fleaCheck():
    # runs if not on flea page
    if not locateImage("./search/flea.png", "flea,", acc=0.9):
        print("not in flea :(")
        for _ in range(5):
            generateRandomDuration()
            pressKey(win32con.VK_ESCAPE, sleepDur)
            sleep(r(0.1, 0.3))
        sleep(r(1, 3))
        click(1260, 1060)  # flea button
        sleep(r(3, 5))


def antiAFK2():
    generateRandomDuration()
    pressKey(win32con.VK_ESCAPE, sleepDur)


def ctrlClick(rawPos=None):
    print("ctrlClick")
    x, y = rawPos
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    randSleep()
    click(x, y)
    randSleep()
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    click(1, 1)
    randSleep()


def sellFuelCon():
    searchArr = (("./search/fcon1.png", "fcon1", 0.93), ("./search/fcon2.png", "fcon2", 0.93))
    print("Selling Fuel Conn")
    for _ in range(25):  # spam so go home :)
        randSleep()
        pressKey(win32con.VK_ESCAPE, sleepDur)
    sleep(r(2, 3))
    click(1114, 1065)  # Traders button
    sleep(r(2, 3))
    click(871, 413)  # The Rapist
    sleep(r(2, 3))
    click(240, 45)  # Sell button
    sleep(r(1, 2))
    # At sell page, start sell loop
    region = (1265, 250, 1920, 1080)
    for _ in range(10):
        fuelConSold = 0
        noneStreak = 0
        if not checkPause():
            while True:
                if not checkPause():
                    if noneStreak >= 10:
                        print("noneStreak >= 10")
                        break
                    for search in searchArr:
                        didFind = False
                        if locateImage(search[0], search[1], search[2], ctrlClick, True, region):
                            fuelConSold += 1
                            didFind = True
                    if didFind:
                        noneStreak = 0
                    else:
                        noneStreak += 1
            randSleep()
            print("fuelConSold", fuelConSold)
            if fuelConSold > 0:
                print("click deal :)")
                for _ in range(5):
                    click(956, 182)  # Deal button
                    randSleep()
            randSleep()
            click(1613, 542)  # click / move mouse to where it scrolls
            randSleep()
            for _ in range(8):
                # print("scroll down")
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 1613, 542, -1, 0)  # Scroll down
                randSleep()
    fleaCheck()


posOffer = (1774, 178)  # Client Coords
posOK = (962, 567)  # Client Coords
posBOT = (420, 300)  # Client Coords
posF5 = (1411, 122)
tarkPos = (0, 0)  # doesnt really matter
ScriptEnabled = True
sleepDurRange = [0.0001, 0.0005]
sleepDur = 0.0001
countSurch = 0.0
surchTime = 0.0
FAILPAUSE = 0.1  # SECONDS
OFFERPAUSE = 0.0
LOOPSLEEPDUR = 1
startTime = time()
lastF5 = startTime
offerTotal = 0
failTotal = 0
scanLoop = 10
spamCount = 0
allowedSecondsAFK = 1200
progressSpinner = ["/", "-", "\\", "|"]
r = random.uniform
# includes size of borders and header
tarkSize = (1920, 1080)
tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")
# , "./search/BOT.png"   , "BOT"    , 0.9
images = [
    ("./search/purchaseClear.png", "./search/afkWarning.png", "./search/NotFound1080.png"),
    ("offer", "afk", "fail"),
    (0.9, 0.9, 0.9),
    (spamClickY, antiAFK2, clickFail),
    (True, False, True),
]

# TODO all button
def main():
    global scanLoop
    win32gui.MoveWindow(tarkHANDLE, tarkPos[0], tarkPos[1], tarkSize[0], tarkSize[1], False)
    win32gui.SetForegroundWindow(tarkHANDLE)
    sys.stdout.flush()
    # afkTime = time()
    loopNum = 0
    while True:
        if not checkPause():
            # if (time()-afkTime>allowedSecondsAFK):
            #     afkTime = time() # reset afkTime to now
            #     antiAFK()
            generateRandomDuration()
            clickF5()
            before = time()
            for _ in range(scanLoop):
                loopNum += 1
                checkPause()
                # print("localImages",i)
                if loopNum % 100 == 0:
                    # check for flea
                    fleaCheck()
                    if loopNum % 2500 == 0:
                        sellFuelCon()
                locateImages(
                    file_loc=images[0],
                    nickname=images[1],
                    acc=images[2],
                    callback=(spamClickY, antiAFK2, clickFail, foundBot),
                    passRawPos=(True, False, True, False),
                )
            dur = time() - before
            timePer = dur / scanLoop
            scanLoop = math.ceil(LOOPSLEEPDUR / timePer) + 1
            # sleep(max((LOOPSLEEPDUR - (dur)), 0))
            # print("scanLoop",scanLoop)


if __name__ == "__main__":
    main()
