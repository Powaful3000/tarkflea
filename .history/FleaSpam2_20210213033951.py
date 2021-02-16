import mss
import time
import asyncio
from PIL import ImageShow


class brrr:
    safePic = None
    newPic = None
    monitor = {"top": 10, "left": 10, "width": 1034, "height": 778}
    sct = mss.mss()
    loop = asyncio.get_event_loop()

    def __init__(self):
        self.loop.create_task(self.startBRRR())

    async def startBRRR(self):
        while (True):
            newPic = self.sct.grab(self.monitor)
            safePic = newPic


def main():
    hehe = brrr()
    time.sleep(1)
    print(hehe.newPic)


if __name__ == "__main__":
    main()
