import mss
import time

monitor = {"top": 10, "left": 10, "width": 1034, "height": 778}

sct = mss.mss()

now = time.time()

print(time.time()-now)
