<<<<<<< HEAD
import pytesseract
import os
import re
=======
import os
>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
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
from difflib import get_close_matches
def computeAvgOF() -> str:
    return str(offerTotal) + "/" + str(failTotal)
def click(x: int, y: int):
    win32api.SetCursorPos(win32gui.ClientToScreen(tarkHANDLE, (x, y)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
<<<<<<< HEAD
    sleep(sleepDur)
=======
    randSleep()
>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
def press_key(VK_CODE, duration_press_sec):
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
def click_f5():
    click(posF5[0], posF5[1])
def spamClickY(rawPos=None):
    global offerTotal,clickLoop,LOOPSLEEPDUR
    offerTotal += 1
    x = posOffer[0]
    y = posOffer[1]
    if rawPos is not None:
        x, y = rawPos
<<<<<<< HEAD
    before = time()
    for _ in range(clickLoop):
=======
    # print(spamCount, "click", x, y, rawPos)
    if spamCount >= 5:
        spamCount = 0
        clickF5()
        return
    for _ in range(30):
>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
        click(x, y)
        press_key(0x59, sleepDur)
    after = time()
    timePer = (after - before)/clickLoop
    clickLoop = math.ceil(LOOPSLEEPDUR/timePer)
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
def fast_screenshot(handle: int) -> np.ndarray:
    start = time()
    left, top, right, bot = win32gui.GetWindowRect(handle)
    w = right - left
    h = bot - top
    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)
    # convert the raw data into a format opencv can read
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype="uint8")
    img.shape = (h, w, 4)
    # print(type(im))
    # cv2.imshow("asd", im)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)
    # drop the alpha channel to work with cv.matchTemplate()
    img = img[:, :, :3]
    # make image C_CONTIGUOUS to avoid errors with cv.rectangle()
    # img = np.ascontiguousarray(img)
    # make grey for my template match
    # img = cv2.cvtColor(img, cv2.COLOR_BGR)
    end = time()
    print("fast_screenshot took", end - start)
    return img
def found_bot(pos: tuple):
    #return
    print("Found bot X at pos", pos)
    text=matches=""
    (x2, y1) = pos
    x2 += imageDict["bot"][0].shape[1]
    # y1 += 70
    x1 = 1920 - x2
    y2 = y1 + 100
    # ocrRegion = (x1, y1, x2, y2)
    img = fast_screenshot(tarkHANDLE)[y1:y2, x1:x2]
    cv2.imwrite("asd.JPG", img)
    for i in range(14):
        if len(matches)>0:
            break
        config = "--psm " + str(i)
        print(config)
        text = pytesseract.image_to_string(img, lang='bender',config=config)
        print("read text:", text)
        matches = get_close_matches(text, botDict.keys(), 1, 0.2)
        print("matches", matchingKeys)
    if len(matches)==0:
        return
    match = botDict[matches[0]]
    print(match)
    print(type(match))
    # multi-template match
    result = cv2.matchTemplate(img, match[0], cv2.TM_CCOEFF_NORMED)
    (xCoords,yCoords) = np.where(result >= 0.99)
    for (x,y) in zip(xCoords, yCoords):
        print("finna click", x, y)
    # itemTemplate = cv2.imread(imgDir)
    # h, w = itemTemplate.shape[:2]
    # method = cv2.TM_CCOEFF_NORMED
    # threshold = 0.99
    # start = time()
    # res = cv2.matchTemplate(img, itemTemplate, method)
    # # TODO
    sys.exit()
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
def image_search_area_ndarray(
    template: np.ndarray, precision=0.8, screenshot: np.ndarray = None, region=None,
):
    # template
    img_rgb = np.array(screenshot)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED,)
    max_val: float
    max_loc: list
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if region is not None:
        max_loc[0] += region[0]
        max_loc[1] += region[1]
    if max_val < precision:
        return [-1, -1]
    return max_loc
def locateImage(
    file_loc, nickname, acc=0.8, callback=None, passRawPos=False, region=None
):
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
            if passRawPos is not None and passRawPos:
                callback((rawPosX, rawPosY))
            else:
                callback()
        return True
    return False
def locate_image_ndarray(
    image: np.ndarray, acc=0.8, callback=None, passRawPos=False, region=None,
):
    global searchTime, countSurch
    countSurch += 1
    before = time()
    # img = machine.get()
    img = fast_screenshot(tarkHANDLE)
    # print("Image Type:", type(img))
    if region is not None:
        x1, y1, x2, y2 = region
        img = img[y1:y2, x1:x2]
    after = time()
    surchTime += after - before
    # print("calling image_search_area", acc)
    rawPosX, rawPosY = image_search_area(image, acc, img)
    if rawPosX != -1:
        if region is not None:
            rawPosX += region[0]
            rawPosY += region[1]
        if callback is not None:
            if passRawPos is not None and passRawPos:
                callback((rawPosX, rawPosY))
            else:
                callback()
        return True
    return False
def locateImages(
    file_loc: tuple, nickname: tuple, acc=(0.8), callback: tuple = None, passRawPos=None
):
    global surchTime, countSurch
    countSurch += 1
    before = time()
    img = fastScreenshot()
    after = time()
    #print(after-before, "fastScreenshot")
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
                if passRawPos is None:
                    callback[i]()
<<<<<<< HEAD
=======

>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
                elif passRawPos[i]:
                    callback[i](rawPos)
                else:
                    callback[i]()
                    break
<<<<<<< HEAD
def locate_images_keys(keys: tuple):
    global surchTime, countSurch
    countSurch += 1
    before = time()
    # img = machine.get()
    img = fastScreenshot()
    # print("Image Type1:", type(img))
    after = time()
    #print(after-before, "fastScreenshot")
    surchTime += after - before
    for key in keys:
        checkPause()
        #image, precision, callback, passArgs, region = imageDict[key]
        # print(key, precision, callback, passArgs, region)
        rawPos = image_search_area_ndarray(imageDict[key][0], imageDict[key][1], img, imageDict[key][4])
        if rawPos[0] != -1 and imageDict[key][2] is not None:
            if imageDict[key][3]:
                imageDict[key][2](rawPos)
            else:
                imageDict[key][2]()
                break
=======


>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
def checkPause():
    if not win32api.GetKeyState(win32con.VK_CAPITAL):
        print()
        loop = 0
        while not win32api.GetKeyState(win32con.VK_CAPITAL):
            loop += 1
            print("Paused", progressSpinner[loop % 4], end="\r")
            sleep(0.1)
        return True
    return False
<<<<<<< HEAD
def fastScreenshot() -> Image.Image:
    start = time()
=======


def fastScreenshot() -> Image.Image:

>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
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
<<<<<<< HEAD
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im = Image.frombuffer(
        "RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1
    )
=======

    saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        "RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1)

>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)
    # if result == None:
    #     #PrintWindow Succeeded
    #     im.save("test.png")
    end = time()
    #print("fastScreenshot took", end - start)
    return im
def doJumping():
    if random.uniform(0, 1) < 0.5:
<<<<<<< HEAD
        press_key(0x20, sleepDur)  # Spacebar
=======
        generateRandomDuration()
        pressKey(0x20, sleepDur)  # Spacebar


>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
def antiAFK():
    print("Begin antiAFK")
    loop = 0
    sleep(random.uniform(1, 2))
    click(76, 1064)  # Main Menu Button
    sleep(random.uniform(1, 2))
    click(954, 868)  # Hideout Button
<<<<<<< HEAD
    sleep(random.uniform(3, 5))
=======
    sleep(random.uniform(5, 7))
>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
    print()
    locate
    while not locate_image_ndarray(*imageDict["hideoutEnter"]):
        print("Waiting for Enter button", progressSpinner[loop % 4], end="\r")
        loop += 1
        sleep(0.1)
<<<<<<< HEAD
    sleep(1)
    press_key(win32con.VK_RETURN, sleepDur)
    sleep(random.uniform(3, 4))
    doJumping()
    press_key(0x57, random.uniform(2, 3))  # W
    doJumping()
    press_key(0x53, random.uniform(2, 3))  # S
    doJumping()
    press_key(win32con.VK_ESCAPE, sleepDur)
    sleep(random.uniform(1, 2))
    press_key(win32con.VK_ESCAPE, sleepDur)
    sleep(random.uniform(1, 2))
    click(1250, 1055)  # Flea Market Button
    sleep(random.uniform(1, 2))
=======
    sleep(2)
    generateRandomDuration()
    pressKey(win32con.VK_RETURN, sleepDur)
    sleep(random.uniform(5, 7))
    doJumping()
    pressKey(0x57, random.uniform(7.5, 12.5))  # W
    doJumping()
    pressKey(0x53, random.uniform(7.5, 12.5))  # S
    doJumping()
    generateRandomDuration()
    pressKey(win32con.VK_ESCAPE, sleepDur)
    sleep(random.uniform(3, 5))
    generateRandomDuration()
    pressKey(win32con.VK_ESCAPE, sleepDur)
    sleep(random.uniform(3, 5))
    click(1250, 1055)  # Flea Market Button
    sleep(random.uniform(3, 5))


>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
def fleaCheck():
    # runs if not on flea page
    if not locateImage("./search/flea.png", "flea,", acc=0.9):
        print("not in flea :(")
        for _ in range(5):
<<<<<<< HEAD
            press_key(win32con.VK_ESCAPE, sleepDur)
            sleep(sleepDur)
        sleep(random.uniform(0.5, 0.7))
        click(1260, 1060)  # flea button
        sleep(random.uniform(1, 2))
=======
            pressKey(win32con.VK_ESCAPE, sleepDur)
            randSleep()
        sleep(random.uniform(.5, .7))
        click(1260, 1060)  # flea button
        sleep(random.uniform(1, 2))


>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
def antiAFK2():
    sleep(sleepDur)
    press_key(win32con.VK_ESCAPE, sleepDur)
def ctrlClick(rawPos=None):
    print("ctrlClick")
    x, y = rawPos
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    sleep(sleepDur)
    click(x, y)
    sleep(sleepDur)
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    click(1, 1)
<<<<<<< HEAD
    sleep(sleepDur)
def collect_sells(dir: str):
    sellImages = []
    for filename in os.listdir(dir):
        filepath = os.path.join(dir, filename)
        if os.path.isdir(filepath):
            continue
        sellImages.append((filepath, filename, 0.95))
    return sellImages
def wait_until(key: str, whatdo=None):
    while not locate_image_ndarray(*imageDict[key]):
        check_pause()
        if whatdo is not None:
            for doTup in whatdo:
                if len(doTup[0]) > 1:
                    doTup[0](*doTup[1])
                else:
                    doTup[0]()
def saw_sleep_click(nickname, sleepRange, clickLoc):
    print("".join(("saw", nickname)))
    sleep(r(*sleepRange))
    click(*clickLoc)
def sell_items(searchArr) -> int:
    print("Selling Items")
    wait_until("mainMenu", (press_key, (win32con.VK_ESCAPE, sleepDur)))
    saw_sleep_click("menu", (0.5, 0.75), (1114, 1065))
    wait_until("rapist", (sleep, (0.5)))
    saw_sleep_click("rapist", (0.25, 0.5), (871, 413))
    wait_until("rapistLoaded", (sleep, (0.5)))
    saw_sleep_click("rapist menu", (0.25, 0.5), (240, 45))
    total = 0
    region = (1265, 250, 1920, 1080)
    click(1613, 542)  # click / move mouse to where it scrolls
    for _ in range(10):
        noneStreak = 0
        didFind = False
        itemsSold = 0
        while True:
            checkPause()
            if noneStreak >= 5:
                print("noneStreak >= 3")
                break
            if itemsSold % 20 == 0:
                print("full sell page")
                for _ in range(5):
                    click(956, 182)  # Deal button
                    sleep(sleepDur)
            for search in searchArr:
                didFind = False
                if locateImage(
                    search[0], search[1], search[2], ctrlClick, True, region
                ):
                    itemsSold += 1
                    total += 1
                    didFind = True
            if didFind:
                noneStreak = 0
            else:
                noneStreak += 1
        sleep(sleepDur)
        print("fuelConSold", itemsSold)
        if itemsSold > 10:
            print("click deal :)")
            click(956, 182)  # Deal button
        sleep(sleepDur)
        click(1613, 542)  # click / move mouse to where it scrolls
        sleep(sleepDur)
        for _ in range(8):
            win32api.mouse_event(
                win32con.MOUSEEVENTF_WHEEL, 1613, 542, -1, 0
            )  # Scroll down
            sleep(sleepDur)
    click(956, 182)  # Deal button
    # fleaCheck()
    return total
autoSellBool = True
=======
    randSleep()


# def sellFuelCon():
#     searchArr = (("./search/fcon1.png", "fcon1", 0.93),
#                  ("./search/fcon2.png", "fcon2", 0.93))
#     print("Selling Fuel Conn")
#     for _ in range(25):  # spam so go home :)
#         randSleep()
#         pressKey(win32con.VK_ESCAPE, sleepDur)
#     sleep(random.uniform(2, 3))
#     click(1114, 1065)  # Traders button
#     sleep(random.uniform(2, 3))
#     click(871, 413)  # The Rapist
#     sleep(random.uniform(2, 3))
#     click(240, 45)  # Sell button
#     sleep(random.uniform(1, 2))
#     # At sell page, start sell loop
#     region = (1265, 250, 1920, 1080)
#     for _ in range(10):
#         noneStreak = 0
#         didFind = False
#         if not checkPause():
#             fuelConSold = 0
#             while True:
#                 if not checkPause():
#                     if noneStreak >= 10:
#                         print("noneStreak >= 10")
#                         break
#                     for search in searchArr:
#                         didFind = False
#                         if locateImage(search[0], search[1], search[2], ctrlClick, True, region):
#                             fuelConSold += 1
#                             didFind = True
#                     if didFind:
#                         noneStreak = 0
#                     else:
#                         noneStreak += 1
#             randSleep()
#             print("fuelConSold", fuelConSold)
#             if fuelConSold > 0:
#                 print("click deal :)")
#                 for _ in range(5):
#                     click(956, 182)  # Deal button
#                     randSleep()
#             randSleep()
#             click(1613, 542)  # click / move mouse to where it scrolls
#             randSleep()
#             for _ in range(8):
#                 # print("scroll down")
#                 win32api.mouse_event(
#                     win32con.MOUSEEVENTF_WHEEL, 1613, 542, -1, 0)  # Scroll down
#                 randSleep()
#     fleaCheck()

def collect_sells(dir:str):
    sellImages = []
    for filename in os.listdir(dir):
        filepath = os.path.join(dir, filename)
        sellImages.append((filepath, filename, 0.95))
    return sellImages

def sell_items(searchArr):
    print("Selling Items")
    for _ in range(25):  # spam so go home :)
        randSleep()
        pressKey(win32con.VK_ESCAPE, sleepDur)
    sleep(random.uniform(2, 3))
    click(1114, 1065)  # Traders button
    sleep(random.uniform(2, 3))
    click(871, 413)  # The Rapist
    sleep(random.uniform(2, 3))
    click(240, 45)  # Sell button
    sleep(random.uniform(1, 2))
    # At sell page, start sell loop
    region = (1265, 250, 1920, 1080)
    click(1613, 542)  # click / move mouse to where it scrolls
    for _ in range(200):
                # print("scroll down")
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 1613, 542, -1, 0)  # Scroll down
        randSleep()
    for _ in range(10):
        noneStreak = 0
        didFind = False
        if not checkPause():
            fuelConSold = 0
            while True:
                if not checkPause():
                    if noneStreak >= 3:
                        print("noneStreak >= 3")
                        break
                    if (fuelConSold%20==0):
                        for _ in range(5):
                            click(956, 182)  # Deal button
                            randSleep()
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
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_WHEEL, 1613, 542, 1, 0)  # Scroll UP
                randSleep()
    fleaCheck()


>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
posOffer = (1774, 178)  # Client Coords
posOK = (962, 567)  # Client Coords
posBOT = (420, 300)  # Client Coords
posF5 = (1411, 122)
tarkPos = (0, 0)  # doesnt really matter
ScriptEnabled = True
<<<<<<< HEAD
sleepDur = 0.00001
=======
sleepDurRange = [0.0001, 0.0003]
sleepDur = 0.00020
>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
countSurch = 0.0
surchTime = 0.0
FAILPAUSE = 0  # SECONDS
OFFERPAUSE = 0.0
<<<<<<< HEAD
LOOPSLEEPDUR = random.uniform(0, 0.1) + 0.7
=======
LOOPSLEEPDUR = random.uniform(0,0.1) + 0.5
>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
startTime = time()
lastF5 = startTime
offerTotal = 0
failTotal = 0
scanLoop = 3
spamCount = 0
allowedSecondsAFK = 1200
progressSpinner = ["/", "-", "\\", "|"]
<<<<<<< HEAD
clickLoop = 15
=======
random.uniform
>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
# includes size of borders and header
tarkSize = (1920, 1080)
tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")
# , "./search/BOT.png"   , "BOT"    , 0.9
<<<<<<< HEAD
# images = [
#     (
#         "./search/purchaseClear.png",
#         "./search/afkWarning.png",
#         "./search/NotFound1080.png",
#     ),
#     ("offer", "afk", "fail"),
#     (0.9, 0.9, 0.9),
#     (spamClickY, antiAFK2, clickFail),
#     (True, False, True),
# ]
# TODO all button
imageDict = {
    "offer": (cv2.imread("./search/purchaseClear.png", 0), 0.9, spamClickY, True, None,),
    "afk": (cv2.imread("./search/afkWarning.png", 0), 0.9, antiAFK2, False, None),
    "fail": (cv2.imread("./search/NotFound1080.png", 0), 0.9, clickFail, True, None,),
    "flea": (cv2.imread("./search/flea.png", 0), 0.9, None, True, None),
    "bot": (cv2.imread("./search/bot.png", 0), 0.9, found_bot, True, None),
    "mainMenu": (
        cv2.imread("./search/mainMenu.png", 0),
        0.9,
        None,
        False,
        (10, 1050, 45, 1075),
    ),
    "rapist": (
        cv2.imread("./search/rapist.png", 0),
        0.9,
        None,
        False,
        (850, 380, 870, 402),
    ),
    "rapistLoaded": (
        cv2.imread("./search/rapistLoaded.png", 0),
        0.9,
        None,
        False,
        (85, 35, 120, 50),
    ),
    "hideoutEnter": (cv2.imread("./search/hideoutEnter.png",0),0.9,None,False,(900,20,1000,50))
}
botDict = {
    "42nd Signature Blend English Tea": cv2.imread(
        "./search/sellItems/botItems/tea.png", 0
    ),
    "Car Battery": cv2.imread("./search/sellItems/botItems/carbattery.png", 0),
    'Gunpowder "Eagle"': cv2.imread(
        "./search/sellItems/botItems/greenpowder.png", 0
    ),
    "Pliers": cv2.imread("./search/sellItems/botItems/pliers.png", 0),
    "Pack of sodium bicarbonate": cv2.imread(
        "./search/sellItems/botItems/bic.png", 0
    ),
    "Salewa first aid kit": cv2.imread(
        "./search/sellItems/botItems/salewa.png",0
    ),
    "Printer paper": cv2.imread("./search/sellItems/botItems/paper.png", 0),
    "Analgin painkillers": cv2.imread("./search/sellItems/botItems/pk.png", 0),
    "Expeditionary fuel tank": cv2.imread(
        "./search/sellItems/botItems/bluefuel.png", 0
    ),
    "Grizzly medical kit": cv2.imread(
        "./search/sellItems/botItems/grizzly.png", 0
    ),
    "Golden Start balm": cv2.imread(
        "./search/sellItems/botItems/goldenstar.png", 0
    ),
    "5L propane tank": cv2.imread(
        "./search/sellItems/botItems/propane.png", 0
    ),
    "Bolts": cv2.imread("./search/sellItems/botItems/bolts.png", 0),
    "0.6 liter water bottle": cv2.imread(
        "./search/sellItems/botItems/water.png",0
    ),
    "Broken GPhone X smartphone": cv2.imread(
        "./search/sellItems/botItems/gpx.png", 0
    ),
    "Can of Majaica coffee beans": cv2.imread(
        "./search/sellItems/botItems/coffee.png", 0
    ),
    "Gas analyzer": cv2.imread("./search/sellItems/botItems/gasan.png", 0),
    "Immobilizing splint": cv2.imread(
        "./search/sellItems/botItems/imsplint.png", 0
    ),
    "Alyonka chocolate bar": cv2.imread(
        "./search/sellItems/botItems/chocolate.png", 0
    ),
    "Can of beef stew (Large)": cv2.imread(
        "./search/sellItems/botItems/stewlarge.png", 0
    ),
    "Antique teapot": cv2.imread("./search/sellItems/botItems/teapot.png", 0),
    "Golden neck chain": cv2.imread(
        "./search/sellItems/botItems/goldchain.png", 0
    ),
    "Can of condensed milk": cv2.imread(
        "./search/sellItems/botItems/conmilk.png", 0
    ),
    "Screwdriver": cv2.imread("./search/sellItems/botItems/screwdriver.png",0),
    "Toilet paper": cv2.imread("./search/sellItems/botItems/tp.png", 0),
}
=======
images = [
    ("./search/purchaseClear.png",
     "./search/afkWarning.png", "./search/NotFound1080.png"),
    ("offer", "afk", "fail"),
    (0.9, 0.9, 0.9),
    (spamClickY, antiAFK2, clickFail),
    (True, False, True),
]

# TODO all button


>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
def main():
    global scanLoop
    sellItems = collect_sells("./search/sellItems/")
    win32gui.MoveWindow(
<<<<<<< HEAD
        tarkHANDLE, tarkPos[0], tarkPos[1], tarkSize[0], tarkSize[1], False
    )
=======
        tarkHANDLE, tarkPos[0], tarkPos[1], tarkSize[0], tarkSize[1], False)
>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
    win32gui.SetForegroundWindow(tarkHANDLE)
    sys.stdout.flush()
    afkTime = time()
    c1 = c2 = r = 0
    start = time()
    while True:
<<<<<<< HEAD
        checkPause()
        if (time()-afkTime>allowedSecondsAFK):
            afkTime = time() # reset afkTime to now
            antiAFK()
        click_f5()
        before = time()
        for _ in range(scanLoop):
            c1 += 1
            checkPause()
            if c1 == 50:
                # check for flea
                c1 = 0
                c2 += 1
                if c2 == 10:
                    if autoSellBool:
                        r += sell_items(sellItems)
                    c1 = c2 = 0
                fleaCheck()
            # locateImages(
            #     file_loc=images[0],
            #     nickname=images[1],
            #     acc=images[2],
            #     callback=(spamClickY, antiAFK2, clickFail, found_bot),
            #     passRawPos=(True, False, True, True),
            # )
            locate_images_keys(("offer", "afk", "fail", "bot"))
        dur = time() - before
        timePer = dur / scanLoop
        scanLoop = math.ceil(LOOPSLEEPDUR / timePer) + 1
        # sleep(max((LOOPSLEEPDUR - (dur)), 0))
        print(
            "Rotated",
            r,
            time() - start,
            scanLoop,
            "timePer",
            timePer,
            "dur",
            dur,
            c1,c2
        )
=======
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
                if loopNum % 50 == 0:
                    # check for flea
                    fleaCheck()
                    if loopNum % 1500 == 0:
                        sell_items(sellItems)
                locateImages(
                    file_loc=images[0],
                    nickname=images[1],
                    acc=images[2],
                    callback=(spamClickY, antiAFK2, clickFail),
                    passRawPos=(True, False, True),
                )
            dur = time() - before
            timePer = dur / scanLoop
            scanLoop = math.ceil(LOOPSLEEPDUR / timePer) + 1
            # sleep(max((LOOPSLEEPDUR - (dur)), 0))
            # print("scanLoop",scanLoop)


>>>>>>> c9fc9c351436c0cb51e19656b25e703d0d304329
if __name__ == "__main__":
    main()
# TODO LISTS
#
# time.sleep() for milliseconds takes way longer than presumed! fix/replace