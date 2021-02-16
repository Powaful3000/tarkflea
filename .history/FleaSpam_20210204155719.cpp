#include <iostream>
#include <windows.h>
#include <chrono>

using namespace std;

int leftMonitorsOffset = 2560;
int DownMonitorsOffset = 0;
int gameBorderH = 16;
int gameBorderV = 39;
int posOffer[] = {946, 100};
int posOK[] = {512, 398};
int posBOT[] = {420,300}; 
BOOL ScriptEnabled = TRUE;
float sleepDurRange[] = {0.0001, 0.0005};
float sleepDur = 0.001;
int countSurch = 0;
int surchTime = 0;
auto startTime = chrono::high_resolution_clock::now();
int tarkPos[] = {0,0};
int tarkSize[] = {1024+gameBorderH,768+gameBorderV};

void pressKey(HWND hwnd, int VK_CODE, float duration_press_sec) {
    SendMessage(hwnd, VK_CODE, VK_F5, 0);
    Sleep(duration_press_sec);
    SendMessage(hwnd, VK_CODE, VK_F5, 0);
}

void click(HWND hwnd, int x, int y) {
    POINT pt;
    pt.x = x;
    pt.y = y;
    SetCursorPos(x, ClientToScreen(hwnd, (x,y)));
}

int main()
{
    HWND tarkHANDLE = FindWindowA(NULL, "EscapeFromTarkov");
    cout << tarkHANDLE << endl;
    cout << GetParent(tarkHANDLE) << endl;
    cout << MoveWindow(tarkHANDLE, tarkPos[0], tarkPos[1], tarkSize[0], tarkSize[1], FALSE) << endl;
    cout << SetForegroundWindow(tarkHANDLE) << endl;
    cout << SetActiveWindow(tarkHANDLE) << endl;
    cout << BringWindowToTop(tarkHANDLE) << endl;
    pressKey(tarkHANDLE, VK_F5, 0);
    //SendMessage(tarkHANDLE, WM_LBUTTONDOWN, MK_LBUTTON, MAKELPARAM(posOK[0], posOK[1]));
    //SendMessage(tarkHANDLE, WM_LBUTTONUP, 0, MAKELPARAM(posOK[0], posOK[1]));
}