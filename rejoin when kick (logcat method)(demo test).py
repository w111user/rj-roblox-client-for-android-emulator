import subprocess
import time
import re
import threading

CHECK_INTERVAL = 3  # giay giua moi lan kiem tra
PLACE_ID = "126884695634066"
PACKAGE_NAME = "com.roblox.client"
UI_FILE = "ui.xml"
KEYWORDS = ["Mất kết nối", "Disconnected", "hardware id mismatch", "267", "rời khỏi", "Leave"]
LOGCAT_TRIGGER = ["reason: 267", "reason: 277", "reason: 279", "reason: 260", "reason: 262", "reason: 304", "you have been kicked from the game"]

def get_connected_devices():
    try:
        result = subprocess.check_output(["adb", "devices"]).decode()
        devices = re.findall(r"^(emulator-\d+)\s+device", result, re.MULTILINE)
        return devices
    except subprocess.CalledProcessError:
        return []

def is_popup_error_present(device):
    try:
        subprocess.run(["adb", "-s", device, "shell", "uiautomator", "dump", "/sdcard/ui.xml"], stdout=subprocess.DEVNULL)
        subprocess.run(["adb", "-s", device, "pull", "/sdcard/ui.xml", UI_FILE], stdout=subprocess.DEVNULL)
        with open(UI_FILE, "r", encoding="utf-8") as f:
            content = f.read().lower()
        return any(keyword.lower() in content for keyword in KEYWORDS)
    except Exception as e:
        print(f"⛔ Loi khi kiem tra popup cua thiet bi {device}: {e}")
        return False

def is_roblox_running(device):
    try:
        result = subprocess.check_output(["adb", "-s", device, "shell", "pidof", PACKAGE_NAME], stderr=subprocess.DEVNULL)
        return bool(result.strip())
    except subprocess.CalledProcessError:
        return False

def close_roblox(device):
    subprocess.run(["adb", "-s", device, "shell", "am", "force-stop", PACKAGE_NAME])

def open_roblox(device):
    subprocess.run([
        "adb", "-s", device, "shell", "am", "start",
        "-a", "android.intent.action.VIEW",
        "-d", f"roblox://experiences/start?placeId={PLACE_ID}"
    ])

def rejoin(device, reason=""):
    print(f"⚠ Phat hien bi da ({reason}) → Dang restart Roblox...")
    close_roblox(device)
    time.sleep(2)
    open_roblox(device)
    print("✅ Da rejoin lai game.")

def monitor_logcat(device):
    print(f"📡 Theo doi logcat thiet bi {device} de bat ly do da...")
    process = subprocess.Popen(
        ["adb", "-s", device, "logcat"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )
    for line in process.stdout:
        if any(trigger in line.lower() for trigger in LOGCAT_TRIGGER):
            print(f"🚫 Phat hien log da: {line.strip()}")
            rejoin(device, reason="logcat")
            time.sleep(10)

def monitor_all_devices():
    print("🔁 Dang theo doi tat ca thiet bi... (Popup + Logcat)")
    devices = get_connected_devices()
    if not devices:
        print("⚠ Khong co thiet bi nao.")
        return

    # Start logcat threads cho tung device
    for device in devices:
        threading.Thread(target=monitor_logcat, args=(device,), daemon=True).start()

    while True:
        for device in devices:
            print(f"\n📱 Thiet bi: {device}")
            if is_roblox_running(device):
                print("✅ Roblox dang chay.")
                if is_popup_error_present(device):
                    rejoin(device, reason="popup")
                    time.sleep(15)
                else:
                    print("✅ Roblox hoat dong binh thuong.")
            else:
                print("❌ Roblox khong chay. Dang mo lai...")
                open_roblox(device)
                print("✅ Da mo Roblox.")
                time.sleep(10)
        time.sleep(CHECK_INTERVAL)

# 🚀 Bat dau theo doi
monitor_all_devices()
