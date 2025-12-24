import subprocess
import time

# ========== Cấu hình ==========
PACKAGE_NAME = "com.roblox.client"
PLACE_ID = "2753915549"  # Thay ID game bạn muốn vào
CHECK_INTERVAL = 5  # giây

# ========== Tự động lấy thiết bị ADB đầu tiên ==========
def get_first_device():
    try:
        result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split("\n")[1:]  # bỏ dòng đầu
        for line in lines:
            if "device" in line and not "unauthorized" in line:
                return line.split()[0]
        return None
    except Exception as e:
        print("Lỗi khi tìm thiết bị ADB:", e)
        return None

# ========== Kiểm tra Roblox đang chạy ==========
def is_roblox_running(device_id):
    try:
        result = subprocess.run(["adb", "-s", device_id, "shell", "pidof", PACKAGE_NAME],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip() != ""
    except Exception as e:
        print("ADB Error:", e)
        return False

# ========== Mở lại Roblox ==========
def rejoin_game(device_id):
    print("→ Đang mở lại Roblox...")
    try:
        url = f"roblox://experiences/start?placeId={PLACE_ID}"
        cmd = ["adb", "-s", device_id, "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("✅ Lệnh gửi thành công!")
    except Exception as e:
        print("❌ Lỗi khi mở lại Roblox:", e)

# ========== Main loop ==========
def main():
    print("🌀 Đang tìm thiết bị ADB...")
    device_id = get_first_device()
    if not device_id:
        print("❌ Không tìm thấy thiết bị ADB nào đang kết nối.")
        return
    print(f"✅ Đã phát hiện thiết bị: {device_id}")

    while True:
        if not is_roblox_running(device_id):
            print("⚠ Roblox không chạy. Đang vào lại...")
            rejoin_game(device_id)
        else:
            print("✅ Roblox vẫn đang chạy.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
