#include <iostream>
#include <windows.h>

using namespace std;

int leftMonitorsOffset = 2560;
int DownMonitorsOffset = 0;
int gameBorderH = 16;
int gameBorderV = 39;

posOffer = 946, 100}
posOK = (512, 398) 
posBOT = (420,300) 
ScriptEnabled = True
sleepDurRange = [0.0001, 0.0005]
sleepDur = 0.001
countSurch = 0
surchTime = 0
startTime = time.time()
posOffer = {}
int tarkPos[] = {10,10};
tarkSize = {1024+gameBorderH,768+gameBorderV};

int main()
{
    HWND tarkHANDLE = FindWindowA(NULL, "EscapeFromTarkov");
    BOOL moved = MoveWindow(tarkHANDLE, tarkPos[0], tarkPos[1], tarkSize[0], tarkSize[1], FALSE);
}