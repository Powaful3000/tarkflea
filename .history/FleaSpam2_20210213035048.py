import mss
import time
import asyncio
import concurrent.futures


class brrr:
    safePic = None
    newPic = None
    monitor = {"top": 10, "left": 10, "width": 1034, "height": 778}
    sct = mss.mss()
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    def __init__(self):
        print("init")
        self.loop.create_task(self.startBRRR())

    async def startBRRR(self):
        while (True):
            print("a")
            self.loop.run_in_executor()
            self.newPic = self.sct.grab(self.monitor)
            print(self.newPic)
            self.safePic = self.newPic
            print(self.safePic)


def main():
    hehe = brrr()
    time.sleep(3)
    print(hehe.newPic)


if __name__ == "__main__":
    main()
