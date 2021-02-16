from time import time, sleep
import random
import win32gui, win32api, win32con, win32ui
from python_imagesearch.imagesearch import *


leftMonitorsOffset:int = 2560 #IMPORTANT (0 if only one monitor, I have a 21:9 2560x1080 monitor so I set to 2560.  Thank imagesearch for being trash.)
DownMonitorsOffset:int = 0 #IMPORTANT (same shit as before)
gameBorderH:int = 16
gameBorderV:int = 39
posOffer = (946, 100) #Client Coords
posOK = (512, 398) #Client Coords
tarkPos = (0,0) #doesnt really matter
ScriptEnabled = True
sleepDurRange = [0.0001, 0.0005]
sleepDur = 0.001
countSurch = 0
surchTime = 0
startTime = time.time()

def randDur():
    global sleepDur
    sleepDur = random.uniform(sleepDurRange[0], sleepDurRange[1])
def clickCTS(HANDLE, x:int, y:int):
    win32api.SetCursorPos(win32gui.ClientToScreen(HANDLE,(x,y)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(sleepDur)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
def clickSTC(HANDLE, x:int, y:int):
    win32api.SetCursorPos(win32gui.ScreenToClient(HANDLE,(x,y)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(sleepDur)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
def sendKey(VK_CODE, duration_press_sec):
    win32api.keybd_event(VK_CODE, 0, 0, 0)
    time.sleep(duration_press_sec)
    win32api.keybd_event(VK_CODE, 0, win32con.KEYEVENTF_KEYUP, 0)
def _imagesearch(file_loc, acc=0.85):
    rawPos = imagesearch(file_loc, acc)
    pos = []
    if rawPos[0] != -1:
        pos = [rawPos[0]-leftMonitorsOffset,rawPos[1]]
        print("position : ", rawPos[0], rawPos[1], pos)
        sendKey(win32con.VK_ESCAPE, 0.05)
    else:
        print("image not found")
def computeAvgScans():
    global surchTime,countSurch, startTime
    avg = surchTime/countSurch
    elapsed = time.time() - startTime
    return ("average: " + avg + "  Elapsed: " + elapsed)
def surch(file_loc, nickname, acc=0.85,callback=None):
    global surchTime,countSurch
    countSurch+=1
    before = time.time()
    rawPos = imagesearch(file_loc, acc)
    after = time.time()
    surchTime += (after-before)
    avg = computeAvgScans)
    if (rawPos[0]!=-1):
        print("I see",nickname, " ", avg)
        if callback != None:
            callback()
        return True
    return False
    
def spamClickY():
    print("I see clock")
    for i in range(5):
        for J in range(5):
            clickCTS(tarkHANDLE, posOffer[0], posOffer[1])
            sendKey(0x59,sleepDur)
        sendKey(win32con.VK_F5,sleepDur)
def clickFail():
    clickCTS(tarkHANDLE, posOK[0], posOK[1])
    sendKey(win32con.VK_F5,sleepDur)

    



def main():
    global tarkHANDLE
    tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")
    tarkSize = (1024+gameBorderH,768+gameBorderV) #includes size of borders and header
    win32gui.MoveWindow(tarkHANDLE, tarkPos[0], tarkPos[1], tarkSize[0], tarkSize[1], False)
    win32gui.SetForegroundWindow(tarkHANDLE)
    sendKey(win32con.VK_F5,sleepDur)
    while(True):
        ScriptEnabled = not win32api.GetKeyState(win32con.VK_CAPITAL)
        if ScriptEnabled:
            for h in range(10):
                randDur()
                sendKey(win32con.VK_F5,sleepDur)
                surch("./search/clockimage.png", "offer", 0.9, spamClickY)
                surch("./search/NotFound.png", "fail", 0.95, clickFail)
            surch("./search/BOT.png","BOT", 0.8, exit)
        else:
            print("Paused")
            time.sleep(0.25)
    
main()