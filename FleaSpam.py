import pytesseract
import os
import re
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
    sleep(sleepDur)
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
    global offerTotal, clickLoop, LOOPSLEEPDUR
    offerTotal += 1
    x = posOffer[0]
    y = posOffer[1]
    if rawPos is not None:
        x, y = rawPos
    before = time()
    for _ in range(clickLoop):
        click(x, y)
        # sleep(0.01)
        # click(1146, 488)  # all button
        # sleep(0.01)
        press_key(0x59, sleepDur)
    after = time()
    timePer = (after - before) / clickLoop
    clickLoop = math.floor(LOOPSLEEPDUR / timePer) + 1
    sleep(OFFERPAUSE)


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
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)
    # drop the alpha channel to work with cv.matchTemplate()
    img = img[:, :, :3]
    # make image C_CONTIGUOUS to avoid errors with cv.rectangle()
    # img = np.ascontiguousarray(img)
    # make grey for my template match
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    end = time()
    print("fast_screenshot took", end - start)
    return img


def found_bot(pos: tuple):
    # return
    print("Found bot X at pos", pos)
    checkPause()
    text = matches = ""
    (x2, y1) = pos
    x2 += imageDict["bot"][0].shape[1]
    x1 = 1920 - x2
    y2 = y1 + 95
    y1 += 70  ## +70 = trim top off
    x1 += 15
    x2 -= 15
    fullImg = fast_screenshot(tarkHANDLE)
    img = fullImg[y1:y2, x1:x2]
    #####Post processing for accuracy
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # img = cv2.bilateralFilter(img, 5, 50, 50)
    img = cv2.bilateralFilter(img, 9, 75, 75)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 17, 0)
    img = cv2.bilateralFilter(img, 9, 75, 75)
    #####

    b = time()
    text = pytesseract.image_to_string(img, lang="bender", config="--psm 11")
    a = time()
    print(a - b, "yikes")
    print("read text:", text)

    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    checkPause()
    found = "You must choose all:"
    if found in text:
        index = text.find(found)
        text = text[index + len(found) :].strip()
        print("trimmed:", text)

    matches = get_close_matches(text, botDict.keys(), 1, 0.8)  # tesseract be like: 20% error👿
    if len(matches) == 0:
        print("none sadge")
        return
    print("matches", matches)
    match = botDict[matches[0]]
    # match = cv2.cvtColor(match, cv2.COLOR_BGR2RGB)
    # print(match) # big output np array
    # print(type(fullImg), type(match))
    # print(fullImg.shape, match.shape)
    # print(fullImg.dtype, match.dtype)
    # cv2.imshow("fullImg", fullImg)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imshow("match", match)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    ## multi-template match
    checkPause()
    result = cv2.matchTemplate(fullImg, match, cv2.TM_CCOEFF_NORMED)  # img -> fullImg
    clicked = []  # list of coord tuples
    (yCoords, xCoords) = np.where(result >= 0.95)
    for (y, x) in zip(yCoords, xCoords):
        if (x, y) in clicked:
            continue
        print("finna click", x, y)
        clicked.append((x, y))  # coord tuple
        click(x, y)
        sleep(0.1)
    ##
    sleep(0.1)
    xConfirm, yConfirm = (960, 1080 - pos[1] - 30)
    print("CONFIRM", xConfirm, yConfirm)
    click(xConfirm, yConfirm)
    sleep(2)  # slow server😠
    return


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
    template: np.ndarray,
    precision=0.8,
    screenshot: np.ndarray = None,
    region=None,
):
    # template
    img_rgb = np.array(screenshot)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(
        img_gray,
        template,
        cv2.TM_CCOEFF_NORMED,
    )
    max_val: float
    max_loc: list
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if region is not None:
        max_loc[0] += region[0]
        max_loc[1] += region[1]
    if max_val < precision:
        return [-1, -1]
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
            if passRawPos is not None and passRawPos:
                callback((rawPosX, rawPosY))
            else:
                callback()
        return True
    return False


def locate_image_ndarray(
    image: np.ndarray,
    acc=0.8,
    callback=None,
    passRawPos=False,
    region=None,
):
    global surchTime, countSurch
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
    rawPosX, rawPosY = image_search_area_ndarray(image, acc, img)
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


def locateImages(file_loc: tuple, nickname: tuple, acc=(0.8), callback: tuple = None, passRawPos=None):
    global surchTime, countSurch
    countSurch += 1
    before = time()
    img = fastScreenshot()
    after = time()
    # print(after-before, "fastScreenshot")
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
                elif passRawPos[i]:
                    callback[i](rawPos)
                else:
                    callback[i]()
                    break


## TODO parallelize
def locate_images_keys(keys: tuple):
    global surchTime, countSurch
    countSurch += 1
    before = time()
    # img = machine.get()
    img = fastScreenshot()
    # print("Image Type1:", type(img))
    after = time()
    # print(after-before, "fastScreenshot")
    surchTime += after - before
    for key in keys:
        checkPause()
        # image, precision, callback, passArgs, region = dictImage
        # print(key, precision, callback, passArgs, region)
        dictImage = imageDict[key]
        rawPos = image_search_area_ndarray(dictImage[0], dictImage[1], img, dictImage[4])
        if rawPos[0] != -1 and dictImage[2] is not None:
            if dictImage[3]:
                dictImage[2](rawPos)
            else:
                dictImage[2]()
                break


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


def fastScreenshot() -> Image.Image:
    start = time()
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
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im = Image.frombuffer("RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)
    # if result == None:
    #     #PrintWindow Succeeded
    #     im.save("test.png",0)
    end = time()
    # print("fastScreenshot took", end - start)
    return im


def doJumping():
    if random.uniform(0, 1) < 0.5:
        press_key(0x20, sleepDur)  # Spacebar


def antiAFK():
    print("Begin antiAFK")
    loop = 0
    sleep(random.uniform(2, 3))
    click(76, 1064)  # Main Menu Button
    sleep(random.uniform(2, 3))
    click(954, 868)  # Hideout Button
    sleep(random.uniform(5, 6))
    while not locate_image_ndarray(*imageDict["hideoutEnter"]):
        print("Waiting for Enter button", progressSpinner[loop % 4], end="\r")
        loop += 1
        sleep(0.1)
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


def fleaCheck():
    # runs if not on flea page
    if not locateImage("./search/flea.png", "flea,", acc=0.9):
        print("not in flea :(")
        for _ in range(5):
            press_key(win32con.VK_ESCAPE, sleepDur)
            sleep(sleepDur)
        sleep(random.uniform(0.5, 0.7))
        click(1260, 1060)  # flea button
        sleep(random.uniform(1, 2))


def antiAFK2():
    sleep(sleepDur)
    press_key(win32con.VK_ESCAPE, sleepDur)


def ctrlClick(rawPos=None):
    print("ctrlClick")
    x, y = rawPos
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    sleep(0.01)
    click(x, y)
    sleep(0.01)
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    click(1, 1)
    sleep(0.01)


def collect_sells(dir: str):
    sellImages = []
    for filename in os.listdir(dir):
        filepath = os.path.join(dir, filename)
        if os.path.isdir(filepath):
            continue
        sellImages.append((filepath, filename, 0.95))
    return sellImages


def wait_until(key: str, whatdo=None):
    print(key)
    ### whatdo is tuple of tuples where 0th element is function name and second element is is arguments tuple
    ### ((function,(arg1,arg2)),(function2,(arg3,arg4)))
    while not locate_image_ndarray(*imageDict[key]):
        checkPause()
        if whatdo is not None:
            for doTup in whatdo:
                if len(doTup) > 1:
                    doTup[0](*doTup[1])
                else:
                    doTup[0]()


def saw_sleep_click(nickname, sleepRange, clickLoc, clickNum=1):
    print("".join(("saw", nickname)))
    sleep(random.uniform(*sleepRange))
    for _ in range(clickNum):
        click(*clickLoc)


def sell_items(searchArr) -> int:
    print("Selling Items")
    # wait_until("mainMenu", (press_key, (win32con.VK_ESCAPE, sleepDur)))
    wait_until(
        "mainMenu",
        (
            (
                press_key,
                (
                    win32con.VK_ESCAPE,
                    sleepDur,
                ),
            ),
            (
                sleep,
                (0.05,),
            ),
        ),
    )
    sleep(2)
    saw_sleep_click("menu", (1, 1.2), (1114, 1065))
    wait_until(
        "rapist",
        (
            (
                sleep,
                (0.5,),
            ),
        ),
    )
    sleep(2)
    saw_sleep_click("rapist", (1, 1.2), (871, 413))
    wait_until(
        "rapistLoaded",
        (
            (
                sleep,
                (0.5,),
            ),
        ),
    )
    sleep(0.2)
    saw_sleep_click("rapist menu", (1, 1.2), (240, 45), 10)
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
                print("noneStreak >= 5")
                break
            for search in searchArr:
                didFind = False
                if locateImage(search[0], search[1], search[2], ctrlClick, True, region):
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
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 1613, 542, -1, 0)  # Scroll down
            sleep(sleepDur)
    click(956, 182)  # Deal button
    # fleaCheck()
    return total


autoSellBool = True
posOffer = (1774, 174)  # Client Coords
posOK = (962, 567)  # Client Coords
posBOT = (420, 300)  # Client Coords
posF5 = (1411, 122)
tarkPos = (0, 0)  # doesnt really matter
ScriptEnabled = True
sleepDur = 0.00001
countSurch = 0.0
surchTime = 0.0
FAILPAUSE = 0  # SECONDS
OFFERPAUSE = 0.0
LOOPSLEEPDUR = 0.25
startTime = time()
lastF5 = startTime
offerTotal = 0
failTotal = 0
scanLoop = 3
spamCount = 0
allowedSecondsAFK = 600
progressSpinner = ["/", "-", "\\", "|"]
clickLoop = 3
# includes size of borders and header
tarkSize = (1920, 1080)
tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")
# , "./search/BOT.png"   , "BOT"    , 0.9
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
    "offer": (
        cv2.imread("./search/purchaseClear.png", 0),
        0.9,
        spamClickY,
        True,
        None,
    ),
    "afk": (cv2.imread("./search/afkWarning.png", 0), 0.9, antiAFK2, False, None),
    "fail": (
        cv2.imread("./search/NotFound1080.png", 0),
        0.9,
        clickFail,
        True,
        None,
    ),
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
    "hideoutEnter": (
        cv2.imread("./search/hideoutEnter.png", 0),
        0.9,
        None,
        False,
        (900, 20, 1000, 50),
    ),
}

botDict = {
    "0.6 liter water bottle": cv2.imread("./search/sellItems/botItems/water.png"),
    "42nd Signature Blend English Tea": cv2.imread("./search/sellItems/botItems/tea.png"),
    "5L propane tank": cv2.imread("./search/sellItems/botItems/propane.png"),
    "AI-2 medkit": cv2.imread("./search/sellItems/botItems/cheese.png"),
    "Alyonka chocolate bar": cv2.imread("./search/sellItems/botItems/chocolate.png"),
    "Analgin painkillers": cv2.imread("./search/sellItems/botItems/pk.png"),
    "Antique teapot": cv2.imread("./search/sellItems/botItems/teapot.png"),
    "Bolts": cv2.imread("./search/sellItems/botItems/bolts.png"),
    "Broken GPhone X smartphone": cv2.imread("./search/sellItems/botItems/gpx.png"),
    "Bronze lion": cv2.imread("./search/sellItems/botItems/lion.png"),
    "Can of beef stew (Large)": cv2.imread("./search/sellItems/botItems/stewlarge.png"),
    "Can of condensed milk": cv2.imread("./search/sellItems/botItems/conmilk.png"),
    "Can of Hot Rod energy drink": cv2.imread("./search/sellItems/botItems/hotrod.png"),
    "Can of Majaica coffee beans": cv2.imread("./search/sellItems/botItems/coffee.png"),
    "Car Battery": cv2.imread("./search/sellItems/botItems/carbattery.png"),
    "Electric drill": cv2.imread("./search/sellItems/botItems/edrill.png"),
    "Expeditionary fuel tank": cv2.imread("./search/sellItems/botItems/bluefuel.png"),
    "Freeman crowbar": cv2.imread("./search/sellItems/botItems/crowbar.png"),
    "Gas analyzer": cv2.imread("./search/sellItems/botItems/gasan.png"),
    "Golden neck chain": cv2.imread("./search/sellItems/botItems/goldchain.png"),
    "Gloden rooster": cv2.imread("./search/sellItems/botItems/cock.png"),
    "Golden Star balm": cv2.imread("./search/sellItems/botItems/goldenstar.png"),
    "Graphics Card": cv2.imread("./search/sellItems/botItems/gpu.png"),
    "Grizzly medical kit": cv2.imread("./search/sellItems/botItems/grizzly.png"),
    "Horse figurine": cv2.imread("./search/sellItems/botItems/horse.png"),
    "Immobilizing splint": cv2.imread("./search/sellItems/botItems/imsplint.png"),
    "Insulating tape": cv2.imread("./search/sellItems/botItems/tape.png"),
    "Morphine injector": cv2.imread("./search/sellItems/botItems/morphine.png"),
    "Pack of sodium bicarbonate": cv2.imread("./search/sellItems/botItems/bic.png"),
    "Pack of sugar": cv2.imread("./search/sellItems/botItems/sugar.png"),
    "Pliers": cv2.imread("./search/sellItems/botItems/pliers.png"),
    "Printer paper": cv2.imread("./search/sellItems/botItems/paper.png"),
    "Red Rebel ice pick": cv2.imread("./search/sellItems/botItems/redrebel.png"),
    "Salewa first aid kit": cv2.imread("./search/sellItems/botItems/salewa.png"),
    "Screwdriver": cv2.imread("./search/sellItems/botItems/screwdriver.png"),
    "Spark plug": cv2.imread("./search/sellItems/botItems/splug.png"),
    "Strike Cigarettes": cv2.imread("./search/sellItems/botItems/strike.png"),
    "T-Shaped plug": cv2.imread("./search/sellItems/botItems/tplug.png"),
    "Toilet paper": cv2.imread("./search/sellItems/botItems/tp.png"),
    "Vaseline balm": cv2.imread("./search/sellItems/botItems/vaseline.png"),
    "WD-40 (100ml)": cv2.imread("./search/sellItems/botItems/wd40.png"),
    "Wrench": cv2.imread("./search/sellItems/botItems/wrench.png"),
    "Xenomorph sealing foam": cv2.imread("./search/sellItems/botItems/xeno.png"),
    "Zibbo lighter": cv2.imread("./search/sellItems/botItems/zibbo.png"),
    '"Fierce Hatchling" moonshine': cv2.imread("./search/sellItems/botItems/moonshine.png"),
    'Gunpowder "Eagle"': cv2.imread("./search/sellItems/botItems/greenpowder.png"),
}


def main():
    global scanLoop
    sellItems = collect_sells("./search/sellItems/")
    win32gui.MoveWindow(tarkHANDLE, tarkPos[0], tarkPos[1], tarkSize[0], tarkSize[1], False)
    for _ in range(5):
        try:
            win32gui.SetForegroundWindow(tarkHANDLE)
            break
        except Exception as e:
            print("Exception", e)
            print("Try Again :)")
            sleep(0.2)
    sys.stdout.flush()
    afkTime = time()
    c1 = c2 = r = 0
    start = time()
    locate_images_keys(("bot", "afk", "fail"))
    fleaCheck()
    while True:
        checkPause()
        # if time() - afkTime > allowedSecondsAFK:
        #     afkTime = time()  # reset afkTime to now
        #     antiAFK()
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
            ## TODO parallelize
            locate_images_keys(("bot", "afk", "fail", "offer"))
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
            c1,
            c2,
        )


if __name__ == "__main__":
    main()
# TODO LISTS
#
# time.sleep() for milliseconds takes way longer than presumed! fix/replace
