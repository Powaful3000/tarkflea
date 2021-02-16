#include <iostream>
#include <windows.h>

using namespace std;

int main()
{
    HWND tarkHANDLE = FindWindowA(NULL, "EscapeFromTarkov");
    cout << tarkHANDLE << endl;
}