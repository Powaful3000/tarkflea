import mss
import time


def main():
    monitor = {"top": 10, "left": 10, "width": 1034, "height": 778}

    sct = mss.mss()
    now = time.time()

    sct_img = sct.grab(monitor)

    print(time.time()-now)
