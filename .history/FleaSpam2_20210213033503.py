import mss
import time
import asyncio


class brrr:
    safePic = None
    newPic = None
    monitor = {"top": 10, "left": 10, "width": 1034, "height": 778}
    sct = mss.mss()

    async def startBRRR(self):
        while (True):
            newPic = await self.sct.grab(monitor)
            safePic = newPic


async def main():
    hehe = brrr()
    hehe.safePic

if __name__ == "__main__":
    asyncio.run(main())
