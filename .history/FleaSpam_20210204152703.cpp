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

int main()
{
    HWND tarkHANDLE = FindWindowA(NULL, "EscapeFromTarkov");
    // cout << tarkHANDLE << endl;
    // cout << GetParent(tarkHANDLE) << endl;
    // cout << MoveWindow(tarkHANDLE, tarkPos[0], tarkPos[1], tarkSize[0], tarkSize[1], FALSE) << endl;
    // cout << SetForegroundWindow(tarkHANDLE) << endl;
    // cout << SetActiveWindow(tarkHANDLE) << endl;
    // cout << BringWindowToTop(tarkHANDLE) << endl;
    // Sleep(1000);
    // sent = SendMessage(tarkHANDLE, );
    cout << SendMessage(tarkHANDLE, )
}