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
from concurrent.futures import ThreadPoolExecutor, as_completed


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
    print("click_f5")
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
    totalTime = after - before
    timePer = totalTime / clickLoop
    clickLoop = math.floor(LOOPSLEEPDUR / timePer) + 1
    print(totalTime, timePer, clickLoop)
    # sleep(OFFERPAUSE)


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
    sleep(sleepDur)


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


def fast_screenshot(handle: int, gray=False) -> np.ndarray:
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
    imgView = img.view()
    # drop the alpha channel to work with cv.matchTemplate()
    imgView = imgView[:, :, :3]
    # make image C_CONTIGUOUS to avoid errors with cv.rectangle()
    imgView = np.ascontiguousarray(imgView)
    # make grey for my template match
    if gray:
        imgView = cv2.cvtColor(imgView, cv2.COLOR_RGB2GRAY)
    end = time()
    # print("fast_screenshot took", end - start)
    return imgView


def found_bot(pos: tuple):
    # return
    print("Found bot X at pos", pos)
    checkPause()
    text = matches = ""
    (x2, y1) = pos
    x2 += imageDict["bot"][0].shape[1]  # add width to x2
    x1 = 1920 - x2
    y2 = y1 + 95
    y1 += 70  ## +70 = trim top off
    x1 += 15
    x2 -= 15
    sleep(2)  # pain
    fullImg = fast_screenshot(tarkHANDLE)
    img = fullImg[y1:y2, x1:x2]
    #####Post processing for accuracy
    # img[np.where((img > [0, 0, 50]).all(axis=2))] = [0, 0, 0] #red
    # img[np.where((img > [40, 0, 0]).all(axis=2))] = [255, 255, 255] #blue
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # img = cv2.bilateralFilter(img, 5, 50, 50)
    img = cv2.bilateralFilter(img, 9, 75, 75)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 17, 0)
    img = cv2.bilateralFilter(img, 9, 75, 75)
    #####

    b = time()
    text = pytesseract.image_to_string(img, lang="bender", config="--psm 12")  # 11 or 12
    a = time()
    print(a - b, "yikes")
    print("read text:", text)
    # cv2.imshow(text, img)
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
    match = botDict[matches[0]].view()
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
    before = time()
    result = cv2.matchTemplate(fullImg, match, cv2.TM_CCOEFF_NORMED)  # img -> fullImg
    print(time() - before)
    (yCoords, xCoords) = np.where(result >= 0.97)
    for (y, x) in zip(yCoords, xCoords):
        print("finna click", x, y)
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
    before = time()
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    print("imagesearcharea", time() - before)
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


def image_search_area_ndarray(template: np.ndarray, precision=0.8, img: np.ndarray = None, region=None):
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # before = time()
    res = cv2.matchTemplate(
        img,
        template,
        cv2.TM_CCOEFF_NORMED,
    )
    max_val: float
    max_loc: list
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if region is not None:
        # max_loc[0] += region[0]
        # max_loc[1] += region[1]
        return (max_loc[0] + region[0], max_loc[1] + region[1])
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


def search_all(template: np.ndarray, acc=0.95, region=None):
    img = fast_screenshot(tarkHANDLE)
    if region is not None:
        x1, y1, x2, y2 = region
        img = img[y1:y2, x1:x2]
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)  # img -> fullImg
    (yCoords, xCoords) = np.where(result >= acc)
    return [(x + x1, y + y1) for (y, x) in zip(yCoords, xCoords)]


def locate_image_ndarray_all(template: np.ndarray, acc=0.97, callback=None, passRawPos=False, region=None):
    img = fast_screenshot(tarkHANDLE)
    if region is not None:
        x1, y1, x2, y2 = region
        img = img[y1:y2, x1:x2]
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)  # img -> fullImg
    (yCoords, xCoords) = np.where(result >= acc)
    ret = False
    for (y, x) in zip(yCoords, xCoords):
        if not ret:
            ret = True
        if region is not None:
            x += region[0]
            y += region[1]
        if callback is not None:
            callback((x, y))
        else:
            callback()
    return ret


def locate_image_ndarray(
    template: np.ndarray,
    acc=0.9,
    callback=None,
    passRawPos=False,
    region=None,
):
    global surchTime, countSurch
    countSurch += 1
    before = time()
    # img = machine.get()
    img = fast_screenshot(tarkHANDLE, gray=True)
    # print("Image Type:", type(img))
    if region is not None:
        x1, y1, x2, y2 = region
        img = img[y1:y2, x1:x2]
    after = time()
    surchTime += after - before
    # print("calling image_search_area", acc)
    rawPosX, rawPosY = image_search_area_ndarray(template, acc, img)
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


def plik_work(img, key) -> bool:
    # view the first ndarray (template) instead of copying :)
    template = imageDict[key][0].view()
    precision, callback, passArgs, region = imageDict[key][1:]
    rawPos = image_search_area_ndarray(template, precision, img, region)
    if rawPos[0] != -1 and callback is not None:
        print("saw", key)
        if passArgs:
            callback(rawPos)
        else:
            callback()
        return True
    return False


def parallel_locate_image_keys(keys: tuple):
    # print("parallel_locate_image_keys")
    checkPause()
    # np.ndarray
    img = fast_screenshot(tarkHANDLE, gray=True)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(plik_work, img, key): key for key in keys}
        # executor.map(plik_work, ((imgView, key) for key in keys))
        # for future in as_completed(futures, 1):
        checkPause()
        for future in as_completed(futures):
            if future.result():
                executor.shutdown(wait=False)
        executor.shutdown()


## TODO parallelize
def locate_images_keys(keys: tuple):
    global surchTime, countSurch
    countSurch += 1
    before = time()
    # img = machine.get()
    # ndarray
    img = fast_screenshot(tarkHANDLE, gray=True)  # was fastScreenshot (PIL.Image)
    # print("Image Type1:", type(img))
    after = time()
    # print(after-before, "fastScreenshot")
    surchTime += after - before
    for key in keys:
        checkPause()
        # image, precision, callback, passArgs, region = dictImage
        # print(key, precision, callback, passArgs, region)
        # print(key, " took:  ", end="")
        image = imageDict[key][0].view()
        precision, callback, passArgs, region = imageDict[key][1:]
        rawPos = image_search_area_ndarray(imageDict[key][0].view(), precision, img, region)
        if rawPos[0] != -1 and callback is not None:
            if passArgs:
                callback(rawPos)
            else:
                callback()
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


def fleaCheck():
    # runs if not on flea page
    print("fleaCheck")
    if not locate_image_ndarray(*imageDict["flea"]):
        print("not in flea :(")
        for _ in range(25):
            press_key(win32con.VK_ESCAPE, sleepDur)
            sleep(sleepDur)
        sleep(1)
        click(1260, 1060)  # flea button
        sleep(1)
        click_f5()


def antiAFK2():
    sleep(sleepDur)
    press_key(win32con.VK_ESCAPE, sleepDur)


def ctrlClick(rawPos=None):
    print("ctrlClick")
    x, y = rawPos
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    click(x, y)
    click(x, y)
    click(x, y)
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    click(1250, 1140)


def collect_sells(dir: str):
    sellImages = []
    for filename in os.listdir(dir):
        filepath = os.path.join(dir, filename)
        if os.path.isdir(filepath):
            continue
        # sellImages.append(cv2.imread(filepath, 0))
        sellImages.append(cv2.imread(filepath))
    return sellImages


def wait_until(key: str, whatdo=None):
    print(key)
    ### whatdo is tuple of tuples where 0th element is function name and second element is is arguments tuple
    ### ((function,(arg1,arg2)),(function2,(arg3,arg4)))
    while not locate_image_ndarray(imageDict[key][0].view(), *imageDict[key][1:]):
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
        sleep(sleepDur)


### TODO: batch search and click items, instead of search click loop
def sell_items(searchArr) -> int:
    print("Selling Items")
    fleaCheck()

    locate_images_keys(("bot",))  # check for bot popup because tarkov :)
    # wait_until("mainMenu", ((press_key, (win32con.VK_ESCAPE, sleepDur)), (sleep, (0.05,))))
    # sleep(1)

    click(1070, 1070)  # trader button
    sleep(1)

    # locate_images_keys(("bot",))  # check for bot popup because tarkov :)
    # saw_sleep_click("menu", (1, 1.2), (1114, 1065))
    wait_until("rapist", ((sleep, (0.5,)),))
    sleep(1)

    ## click traders button not menu lol
    click(1070, 1060)

    locate_images_keys(("bot",))  # check for bot popup because tarkov :)
    saw_sleep_click("rapist", (1, 1.2), (871, 413))
    wait_until("rapistLoaded", ((sleep, (0.2,)),))
    sleep(1)

    locate_images_keys(("bot",))  # check for bot popup because tarkov :)
    saw_sleep_click("rapist menu", (1, 1.2), (240, 45), 10)  # 240,45 is sell button
    total = 0
    region = (1265, 250, 1920, 1080)
    with ThreadPoolExecutor() as executor:
        for _ in range(10):
            click(240, 45)  # rapist sell button
            locate_images_keys(("bot",))  # check for bot popup because tarkov :)

            ##

            # list of coord tuples
            futures = {executor.submit(search_all, search, 0.97, region): search for search in searchArr}
            checkPause()
            # COLLECT CLICKS
            toClick = []
            for future in futures:
                res = future.result()
                if len(res) > 0:
                    toClick += res

            numSold = 0
            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            sleep(sleepDur)
            for (x, y) in toClick:
                numSold += 1
                click(x, y)
                click(x, y)
                click(x, y)
            sleep(sleepDur)
            win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

            # sleep(sleepDur)
            if numSold:
                print("click deal :)")
                click(956, 182)  # Deal button
                total += numSold
            print("fuelConSold", numSold)

            # sleep(sleepDur)
            click(1613, 542)  # click / move mouse to where it scrolls
            # sleep(sleepDur)
            for _ in range(8):
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 1613, 542, -1, 0)  # Scroll down
                sleep(sleepDur)
        click(956, 182)  # Deal button
        return total


autoSellBool = True
fleaCheckFrequency = 10
itemSellFrequency = 10
posOffer = (1774, 174)  # Client Coords
posOK = (962, 567)  # Client Coords
posBOT = (420, 300)  # Client Coords
posF5 = (1411, 122)
tarkPos = (0, 0)  # doesnt really matter
sleepDur = 0.00001
countSurch = 0.0
surchTime = 0.0
FAILPAUSE = 0  # SECONDS
OFFERPAUSE = 0.0
LOOPSLEEPDUR = 0.6
startTime = time()
lastF5 = startTime
offerTotal = 0
failTotal = 0
scanLoop = 5
spamCount = 0
progressSpinner = ["/", "-", "\\", "|"]
clickLoop = 3
# includes size of borders and header
tarkSize = (1920, 1080)
tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")
# np.ndarray
templateStore = {
    "offer": cv2.imread("./search/purchaseClear.png", 0),
    "afk": cv2.imread("./search/afkWarning.png", 0),
    "fail": cv2.imread("./search/NotFound1080.png", 0),
    "flea": cv2.imread("./search/flea.png", 0),
    "bot": cv2.imread("./search/bot.png", 0),
    "mainMenu": cv2.imread("./search/mainMenu.png", 0),
    "rapist": cv2.imread("./search/rapist.png", 0),
    "rapistLoaded": cv2.imread("./search/rapistLoaded.png", 0),
    "hideoutEnter": cv2.imread("./search/hideoutEnter.png", 0),
}
# np.ndarray, precision, callback, passArgs, region
imageDict = {
    "offer": (templateStore["offer"].view(), 0.95, spamClickY, True, None),  # (1700, 145, 1850, 1000)
    "afk": (templateStore["afk"].view(), 0.95, antiAFK2, False, None),  # (710, 450, 800, 480)
    "fail": (templateStore["fail"].view(), 0.95, clickFail, True, None),
    "flea": (templateStore["flea"].view(), 0.95, None, True, None),
    "bot": (templateStore["bot"].view(), 0.95, found_bot, True, None),
    "mainMenu": (templateStore["mainMenu"].view(), 0.95, None, False, (10, 1050, 45, 1075)),
    "rapist": (templateStore["rapist"].view(), 0.95, None, False, (830, 360, 910, 440)),
    "rapistLoaded": (templateStore["rapistLoaded"].view(), 0.95, None, False, (85, 35, 120, 50)),
    "hideoutEnter": (templateStore["hideoutEnter"].view(), 0.95, None, False, (900, 20, 1000, 50)),
}

botDict = {
    "0.6 liter water bottle": cv2.imread("./search/sellItems/botItems/water.png"),
    "42nd Signature Blend English Tea": cv2.imread("./search/sellItems/botItems/tea.png"),
    "5L propane tank": cv2.imread("./search/sellItems/botItems/propane.png"),
    "AI-2 medkit": cv2.imread("./search/sellItems/botItems/cheese.png"),
    "Alyonka chocolate bar": cv2.imread("./search/sellItems/botItems/chocolate.png"),
    "Analgin painkillers": cv2.imread("./search/sellItems/botItems/pk.png"),
    "Antique teapot": cv2.imread("./search/sellItems/botItems/teapot.png"),
    "Aseptic bandage": cv2.imread("./search/sellItems/botItems/bandage.png"),
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

### TODO: somehow batch search click purchase buttons + parallelize the four main template searches
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
            sleep(0.5)
    sys.stdout.flush()
    afkTime = time()
    c1 = c2 = r = 0
    autoSellFrequency = itemSellFrequency / fleaCheckFrequency
    start = time()
    parallel_locate_image_keys(("bot", "afk", "fail"))
    while True:
        checkPause()
        click_f5()
        before = time()
        c1 += 1
        if c1 == fleaCheckFrequency:
            # check for flea
            c1 = 0
            c2 += 1
            if c2 == autoSellFrequency:
                if autoSellBool:
                    r += sell_items(sellItems)
                c1 = c2 = 0
            fleaCheck()
        for _ in range(scanLoop):
            checkPause()
            # locate_images_keys(("bot", "afk", "fail", "offer"))
            checkPause()
            parallel_locate_image_keys(("bot", "afk", "fail", "offer"))
            checkPause()
        ## loops calc
        dur = time() - before
        timePer = dur / scanLoop
        scanLoop = math.ceil(LOOPSLEEPDUR / timePer)
        ##
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
