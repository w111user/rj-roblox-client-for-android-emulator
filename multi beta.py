import subprocess
import time
import re

CHECK_INTERVAL = 3  # giây giữa mỗi lần kiểm tra
PLACE_ID = "2753915549"
PACKAGE_NAME = "com.roblox.client"
UI_FILE = "ui.xml"
KEYWORDS = ["Mất kết nối", "Disconnected", "hardware id mismatch", "267", "rời khỏi", "Leave"]

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
        return any(keyword in content for keyword in KEYWORDS)
    except Exception as e:
        print(f"⛔ Lỗi khi kiểm tra popup của thiết bị {device}: {e}")
        return False

def is_roblox_running(device):
    try:
        result = subprocess.check_output(
            ["adb", "-s", device, "shell", "pidof", PACKAGE_NAME],
            stderr=subprocess.DEVNULL
        )
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

def monitor_all_devices():
    print("🔁 Đang theo dõi tất cả thiết bị... (Rejoin nếu bị đá hoặc Roblox không hoạt động)")
    while True:
        devices = get_connected_devices()
        if not devices:
            print("⚠ Không phát hiện thiết bị ADB nào.")
        for device in devices:
            print(f"\n📱 Thiết bị: {device}")
            if is_roblox_running(device):
                print("✅ Roblox đang chạy.")
                if is_popup_error_present(device):
                    print("⚠ Phát hiện popup kick! Đang khởi động lại Roblox...")
                    close_roblox(device)
                    time.sleep(2)
                    open_roblox(device)
                    print("✅ Đã gửi lệnh rejoin sau khi bị đá.")
                    time.sleep(15)
                else:
                    print("✅ Roblox hoạt động bình thường.")
            else:
                print("❌ Roblox không chạy. Đang mở lại...")
                open_roblox(device)
                print("✅ Đã gửi lệnh mở Roblox.")
                time.sleep(10)
        time.sleep(CHECK_INTERVAL)

# Khởi chạy
monitor_all_devices()
