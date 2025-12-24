import subprocess
import time
import re
import threading
from colorama import init, Fore, Style
import os
import tkinter as tk
from tkinter import simpledialog, messagebox


init(autoreset=True)
os.system("color 1")

UI_FILE = "ui.xml"
PACKAGE_NAME = "com.roblox.client.vnggames"
CHECK_INTERVAL = 3
KEYWORDS = ["Mất kết nối", "Disconnected", "hardware id mismatch", "267", "rời khỏi", "Leave"]
LOGCAT_TRIGGER = [
    "reason: 267", "reason: 269", "reason: 277",
    "reason: 279", "reason: 260", "reason: 262",
    "reason: 304", "you have been kicked from the game"
]
SAVE_FILE = "place_id.txt"

def ask_with_timeout(question, title, timeout=3):
    root = tk.Tk()
    root.withdraw()  # ẩn cửa sổ chính

    answer = {"result": None}

    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("360x150")
    win.resizable(False, False)
    win.attributes("-topmost", True)

    label = tk.Label(win, text="", font=("Segoe UI", 10), justify="center", wraplength=340)
    label.pack(pady=10)

    def on_ok():
        answer["result"] = True
        win.destroy()

    def on_cancel():
        answer["result"] = False
        win.destroy()

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=5)
    ok_btn = tk.Button(btn_frame, text="OK", width=10, command=on_ok)
    cancel_btn = tk.Button(btn_frame, text="Cancel", width=10, command=on_cancel)
    ok_btn.pack(side="left", padx=10)
    cancel_btn.pack(side="right", padx=10)

    def countdown(i):
        if answer["result"] is not None:
            return
        label.config(text=f"{question}\n(Tự động dùng PLACE_ID sau {i}s...)")
        if i > 0:
            win.after(1000, countdown, i - 1)
        else:
            answer["result"] = True
            win.destroy()

    countdown(timeout)
    win.grab_set()
    root.wait_window(win)
    root.destroy()
    return answer["result"]


def get_place_id():
    while True:
        if os.path.exists(SAVE_FILE):
            print(Fore.CYAN + "📂 Đã phát hiện file PLACE_ID, vui lòng đợi...")
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                saved_id = f.read().strip()

            user_choice = ask_with_timeout(
                f"PLACE_ID hiện tại là: {saved_id}\nBạn có muốn sử dụng PLACE_ID này không?",
                "Xác nhận PLACE_ID",
                timeout=3
            )

            if user_choice:  # OK hoặc hết 3s không bấm
                print(Fore.GREEN + f"✅ Sử dụng PLACE_ID: {saved_id}")
                return saved_id
            else:  # Cancel → xóa file cũ
                os.remove(SAVE_FILE)
                print(Fore.YELLOW + "⚠️ Đã xóa PLACE_ID cũ. Vui lòng nhập PLACE_ID mới.")
                continue
        root = tk.Tk()
        root.withdraw()
        place_id = simpledialog.askstring("PLACE_ID", "🔹 Nhập PLACE_ID của bạn (chỉ gồm số):")
        root.destroy()

        if place_id is None:
            messagebox.showerror("❌ Lỗi", "Không có PLACE_ID nào được nhập. Dừng chương trình.")
            print(Fore.RED + "❌ Không có PLACE_ID được nhập. Dừng chương trình.")
            exit()

        place_id = place_id.strip()
        if place_id.isdigit():
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                f.write(place_id)
            messagebox.showinfo("✅ Thành công", "PLACE_ID đã được lưu!")
            print(Fore.GREEN + "✅ PLACE_ID đã được lưu. Đang khởi động...")
            return place_id
        else:
            messagebox.showwarning("⚠️ Sai định dạng", "PLACE_ID chỉ được chứa số (0–9). Vui lòng nhập lại!")
PLACE_ID = get_place_id()
print(Style.BRIGHT + Fore.YELLOW + f"🚀 PLACE_ID đang sử dụng: {PLACE_ID}")
def get_connected_devices():
    try:
        result = subprocess.check_output(["adb.exe", "devices"]).decode()
        devices = re.findall(r"^(emulator-\d+)\s+device", result, re.MULTILINE)
        return devices
    except subprocess.CalledProcessError:
        return []

def is_popup_error_present(device):
    try:
        subprocess.run(["adb.exe", "-s", device, "shell", "uiautomator", "dump", "/sdcard/ui.xml"], stdout=subprocess.DEVNULL)
        subprocess.run(["adb.exe", "-s", device, "pull", "/sdcard/ui.xml", UI_FILE], stdout=subprocess.DEVNULL)
        with open(UI_FILE, "r", encoding="utf-8") as f:
            content = f.read().lower()
        return any(keyword.lower() in content for keyword in KEYWORDS)
    except Exception as e:
        print(f"⛔ Lỗi khi kiểm tra popup của thiết bị {device}: {e}")
        return False

def is_roblox_running(device):
    try:
        result = subprocess.check_output(["adb.exe", "-s", device, "shell", "pidof", PACKAGE_NAME], stderr=subprocess.DEVNULL)
        return bool(result.strip())
    except subprocess.CalledProcessError:
        return False

def close_roblox(device):
    subprocess.run(["adb.exe", "-s", device, "shell", "am", "force-stop", PACKAGE_NAME])

def open_roblox(device):
    subprocess.run([
        "adb.exe", "-s", device, "shell", "am", "start",
        "-a", "android.intent.action.VIEW",
        "-d", f"roblox://experiences/start?placeId={PLACE_ID}"
    ])

def rejoin(device, reason=""):
    print(Fore.RED + f"⚠ Phát hiện bị đá ({reason}) → Đang restart Roblox...")
    close_roblox(device)
    time.sleep(2)
    open_roblox(device)
    print(Fore.GREEN + "✅ Đã rejoin lại game.")

def monitor_logcat(device):
    print(f"📡 Theo dõi logcat thiết bị {device} để phát hiện lý do đá...")
    process = subprocess.Popen(
        ["adb.exe", "-s", device, "logcat"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )
    for line in process.stdout:
        if any(trigger in line.lower() for trigger in LOGCAT_TRIGGER):
            print(Fore.RED + f"🚫 Phát hiện log bị đá: {line.strip()}")
            rejoin(device, reason="logcat")
            time.sleep(10)

def monitor_all_devices():
    print(Fore.YELLOW + "🔁 Đang theo dõi tất cả thiết bị... (Popup + Logcat)")
    devices = get_connected_devices()
    if not devices:
        print("⚠ Không có thiết bị nào được kết nối.")
        return
    for device in devices:
        threading.Thread(target=monitor_logcat, args=(device,), daemon=True).start()

    while True:
        for device in devices:
            print(Fore.BLUE + f"\n📱 Thiết bị: {device}")
            if is_roblox_running(device):
                print(Fore.YELLOW + "✅ Roblox đang chạy.")
                if is_popup_error_present(device):
                    rejoin(device, reason="popup")
                    time.sleep(15)
                else:
                    print(Fore.GREEN + "✅ Roblox hoạt động bình thường.")
            else:
                print(Fore.RED + "❌ Roblox không chạy. Đang mở lại...")
                open_roblox(device)
                print(Fore.GREEN + "✅ Đã mở Roblox.")
                time.sleep(10)
        time.sleep(CHECK_INTERVAL)

try:
    monitor_all_devices()
except KeyboardInterrupt:
    print(Fore.CYAN + "\n🛑 Đã dừng tool. Nếu có vấn đề vui lòng contact Discord: w11user")
    input("Nhấn Enter để thoát...")