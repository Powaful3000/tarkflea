import mss
import time
import asyncio
import concurrent.futures


class brrr:
    safePic = None
    newPic = None
    monitor = {"top": 10, "left": 10, "width": 1034, "height": 778}
    sct = None
    loop = None
    executor = None

    def __init__(self, loop):
        print("init")
        self.sct = mss.mss()
        self.loop = loop
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self.loop.create_task(self.startBRRR())

    def doGrab(self):
        self.newPic = self.sct.grab(self.monitor)
        print(self.newPic)
        self.safePic = self.newPic
        print(self.safePic)

    async def startBRRR(self):
        while (True):
            self.loop.run_in_executor(self.executor, self.doGrab)


async def main():
    loop = asyncio.get_event_loop()
    hehe = brrr(loop)
    time.sleep(1)
    print(hehe.newPic)
    exit()


if __name__ == "__main__":
    asyncio.run(main())
