#include <iostream>
#include <windows.h>

using namespace std;

int leftMonitorsOffset
int[] tarkPos = [10,10];
tarkSize = [1024+gameBorderH,768+gameBorderV];

int main()
{
    HWND tarkHANDLE = FindWindowA(NULL, "EscapeFromTarkov");
    BOOL moved = MoveWindow(tarkHANDLE, tarkPos[0], tarkPos[1], tarkSize[0], tarkSize[1], FALSE);
}