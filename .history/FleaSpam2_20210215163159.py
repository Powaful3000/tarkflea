import configparser as CP
import random
import sys
from time import sleep, time
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image
from python_imagesearch.imagesearch import imagesearcharea
import multiprocessing as mp
import mss
import mss.tools

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
tarkPos = (10, 10)  # doesnt really matter
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

# includes size of borders and header
tarkSize = (1024+gameBorderH, 768+gameBorderV)
tarkHANDLE = tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")


class ScreenshotMachine:
    def __init__(self):
        parentConn, childConn = mp.Pipe()
        proc = mp.Process(target=self.grabLoop, args=(childConn,))
        proc.start()
        while True:
            if (parentConn.poll()):
                latestImg = parentConn.recv()

    def grabLoop(self, pipe):
        tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")
        gameBorderH: int = 16
        gameBorderV: int = 39
        tarkSize = (1024+gameBorderH, 768+gameBorderV)
        while True:
            img = self.fastScreenshot(tarkHANDLE, tarkSize[0], tarkSize[1])
            pipe.send(img)

    def fastScreenshot():


if __name__ == "__main__":
    # The screenshots queue
    queue = mp.Queue()  # type: mp.Queue
