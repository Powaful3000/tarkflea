import mss
import time
import asyncio
from PIL import ImageShow


class brrr:
    safePic = None
    newPic = None
    monitor = {"top": 10, "left": 10, "width": 1034, "height": 778}
    sct = mss.mss()

    async def startBRRR(self):
        while (True):
            newPic = await self.sct.grab(self.monitor)
            safePic = newPic


def main():
    hehe = brrr()
    ImageShow.show(hehe.safePic)


if __name__ == "__main__":
    main()
