import win32ui
import win32gui
import win32con
import win32api
import sys
import random
import PIL
import multiprocessing as mp
import configparser as CP
from time import sleep, time
from python_imagesearch.imagesearch import imagesearcharea
from multiprocessing import connection
_G = 'settings.ini'
_F = 'EscapeFromTarkov'
_E = '\r'
_D = False
_C = True
_B = 'DEFAULT'
_A = None
TURBO_MODE = _C
leftMonitorsOffset = 2560
DownMonitorsOffset = 0
gameBorderH = 16
gameBorderV = 39
posOffer = 946, 100
posOK = 512, 398
posBOT = 420, 300
posF5 = 747, 65
tarkPos = 0, 0
ScriptEnabled = _C
sleepDurRange = [0.0001, 0.0005]
sleepDur = 0.0001
countSurch = 0
surchTime = 0
FAILPAUSE = 30
OFFERPAUSE = 30
LOOPSLEEPDUR = 1
startTime = time()
lastF5 = startTime
offerTotal = 0
failTotal = 0
lineReplace = _D
tarkSize = 1024+gameBorderH, 768+gameBorderV
tarkHANDLE = tarkHANDLE = win32gui.FindWindow(_A, _F)


class ScreenshotMachine:
    gameBorderH = 16
    gameBorderV = 39
    tarkSize = 1024+gameBorderH, 768+gameBorderV
    parentConn: 0
    childConn: 0
    proc: 0
    lastImg = _A
    lastImgTime = 0
    def __init__(A): A.parentConn, A.childConn = mp.Pipe(); A.proc = mp.Process(
        target=A.grabLoop, args=(A.childConn,)); A.proc.start()

    def die(A): A.proc.terminate()

    def getLatest(A):
        if A.parentConn.poll():
            A.lastImg = A.parentConn.recv()
            A.lastImgTime = time()
            return A.lastImg
        elif A.lastImg is not _A and time()-A.lastImgTime < 1:
            return A.lastImg
        else:
            return _A

    def grabLoop(A, pipe):
        B = win32gui.FindWindow(_A, _F)
        while _C:
            C = A.fastScreenshot(B)
            pipe.send(C)

    def fastScreenshot(J, hwnd, width=1024, height=768): E = height; D = width; F = win32gui.GetWindowDC(hwnd); B = win32ui.CreateDCFromHandle(F); C = B.CreateCompatibleDC(); A = win32ui.CreateBitmap(); A.CreateCompatibleBitmap(B, D, E); C.SelectObject(A); C.BitBlt(
        (0, 0), (D, E), B, (0, 0), win32con.SRCCOPY); G = A.GetInfo(); H = A.GetBitmapBits(_C); I = PIL.Image.frombuffer('RGB', (G['bmWidth'], G['bmHeight']), H, 'raw', 'BGRX', 0, 1); B.DeleteDC(); C.DeleteDC(); win32gui.ReleaseDC(hwnd, F); win32gui.DeleteObject(A.GetHandle()); return I


if not TURBO_MODE:
    config = CP.ConfigParser({_B: 'failpause'})
    config.read(_G)
    try:
        FAILPAUSE = int(config[_B]['FAILPAUSE'])
        OFFERPAUSE = int(config[_B]['OFFERPAUSE'])
        LOOPSLEEPDUR = int(config[_B]['LOOPSLEEPDUR'])
    except:
        pass
else:
    FAILPAUSE = 0
    OFFERPAUSE = 0
    LOOPSLEEPDUR = 1


def computeAvgOF(): return str(offerTotal)+'/'+str(failTotal)


def generateRandomDuration(): global sleepDur; sleepDur = random.uniform(
    sleepDurRange[0], sleepDurRange[1])


def click(x, y): win32api.SetCursorPos(win32gui.ClientToScreen(tarkHANDLE, (x, y))); win32api.mouse_event(
    win32con.MOUSEEVENTF_LEFTDOWN, 0, 0); sleep(sleepDur); win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def pressKey(VK_CODE, duration_press_sec): A = VK_CODE; win32api.keybd_event(A, 0, 0, 0); sleep(
    duration_press_sec); win32api.keybd_event(A, 0, win32con.KEYEVENTF_KEYUP, 0)


def printAvgScans(): global surchTime, countSurch, startTime; A = surchTime/countSurch; B = time() - \
    startTime; return'Average O:F '+computeAvgOF()+' Average time to search screen: '+str(A)+'  Elapsed: '+str(B)


def spamClickY():
    global offerTotal
    offerTotal += 1
    for _ in range(10):
        for _ in range(10):
            click(posOffer[0], posOffer[1])
            pressKey(89, sleepDur)
    sleep(OFFERPAUSE)
    clickF5()


def clickFail(): global failTotal; failTotal += 1; click(
    posOK[0], posOK[1]); sleep(0.1); sleep(FAILPAUSE); clickF5()


def clickF5():
    global lastF5
    A = time()
    if A-lastF5 > 5:
        pressKey(win32con.VK_F5, sleepDur)
        lastF5 = A
    else:
        click(posF5[0], posF5[1])


def foundBot():
    if not TURBO_MODE:
        A = random.choice(list(config[_B]))
        config.set(_B, A, str(float(config[_B][A])+float(config[_B][A]*1.1)))
        with open(_G, 'w')as B:
            config.write(B)
    exit()


def locateImages(machine, file_loc, nickname, acc, callback=_A):
    K = '\n'
    J = ' '
    I = 'I saw'
    D = callback
    C = file_loc
    global surchTime, countSurch
    countSurch += 1
    F = time()
    E = machine.getLatest()
    if E is not _A:
        G = time()
        surchTime += G-F
        for A in range(len(C)):
            H = imagesearcharea(C[A], 0, 0, 1920, 1080, acc[A], E)
            if H[0] != -1:
                B = printAvgScans()
                print(I, nickname[A], J, B, end=(K, _E)[lineReplace])
                if D != _A:
                    D[A]()
                    return _C
            else:
                B = printAvgScans()
                print(I, 'None', J, B, end=(K, _E)[lineReplace])
        return _D


def main():
    B = ScreenshotMachine()
    win32gui.MoveWindow(
        tarkHANDLE, tarkPos[0], tarkPos[1], tarkSize[0], tarkSize[1], _D)
    win32gui.SetForegroundWindow(tarkHANDLE)
    A = _A
    sys.stdout.flush()
    while _C:
        C = not win32api.GetKeyState(win32con.VK_CAPITAL)
        if C:
            generateRandomDuration()
            clickF5()
            D = time()
            for _ in range(10):
                if locateImages(B, ('./search/NotFound.png', './search/clockImage.png', './search/BOT.png'), ('fail', 'offer', 'BOT'), (0.8, 0.95, 0.8), (clickFail, spamClickY, foundBot)):
                    break
            sleep(max(LOOPSLEEPDUR-(time()-D), 0.01))
        else:
            if A is _A:
                A = time()
            print('Paused', str(time()-A)[0:6], end=_E)


if __name__ == '__main__':
    main()
