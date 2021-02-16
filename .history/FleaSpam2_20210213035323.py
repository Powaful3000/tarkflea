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

    def __init__(self):
        print("init")
        self.sct = mss.mss()
        self.loop = asyncio.get_event_loop()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self.loop.create_task(self.startBRRR())

    def doGrab(self):
        print("grab")
        self.newPic = self.sct.grab(self.monitor)
        print(self.newPic)
        self.safePic = self.newPic
        print(self.safePic)

    async def startBRRR(self):
        while (True):
            print("a")
            self.loop.run_in_executor(self.executor, self.doGrab)


def main():
    hehe = brrr()
    time.sleep(1)
    print(hehe.newPic)


if __name__ == "__main__":
    main()
