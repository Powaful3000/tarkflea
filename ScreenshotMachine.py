import multiprocessing as mp
from multiprocessing import connection
import win32ui
import win32gui
import win32con
from PIL import Image


class ScreenshotMachine:
    gameBorderH: int = 16
    gameBorderV: int = 39
    tarkSize = (1024+gameBorderH, 768+gameBorderV)
    parentConn: connection.Connection
    childConn: connection.Connection
    proc: mp.Process
    lastImg: Image = None

    def __init__(self):
        self.parentConn, self.childConn = mp.Pipe()
        self.proc = mp.Process(target=self.grabLoop, args=(self.childConn,))
        self.proc.start()
        self.childConn.close()

    def die(self):
        self.proc.terminate()

    def getLatest(self) -> connection.Connection:
        if (self.parentConn.poll()):
            self.lastImg = self.parentConn.recv()
        return self.lastImg

    def grabLoop(self, pipe: connection.Connection):
        tarkHANDLE = win32gui.FindWindow(None, "EscapeFromTarkov")
        while True:
            img = self.fastScreenshot(tarkHANDLE, )
            pipe.send(img)

    def fastScreenshot(_, hwnd, width=1024, height=768) -> Image:
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (width, height), dcObj, (0, 0), win32con.SRCCOPY)
        bmpinfo = dataBitMap.GetInfo()
        bmpstr = dataBitMap.GetBitmapBits(True)
        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        return im
