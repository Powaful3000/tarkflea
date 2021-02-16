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


def grab(queue):
    # type: (Queue) -> None

    rect = {"top": 0, "left": 0, "width": 600, "height": 800}

    with mss.mss() as sct:
        for _ in range(1_000):
            queue.put(sct.grab(rect))

    # Tell the other worker to stop
    queue.put(None)


def save(queue):
    # type: (Queue) -> None

    number = 0
    output = "screenshots/file_{}.png"
    to_png = mss.tools.to_png

    while "there are screenshots":
        img = queue.get()
        if img is None:
            break

        to_png(img.rgb, img.size, output=output.format(number))
        number += 1


if __name__ == "__main__":
    # The screenshots queue
    queue = mp.Queue()  # type: Queue

    # 2 processes: one for grabing and one for saving PNG files
    mp.Process(target=grab, args=(queue,)).start()
    mp.Process(target=save, args=(queue,)).start()
