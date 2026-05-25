import os
import subprocess
import datetime
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

print("==========================================================")
print("     HỆ THỐNG CẬP NHẬT TỰ ĐỘNG DASHBOARD LÊN GITHUB      ")
print("==========================================================\n")

# Đường dẫn dự án
script_update = r"LDN PA\Vitality Compass\update_dashboard_data.py"
git_exe = r"C:\Program Files\Git\cmd\git.exe"

# 1. Cập nhật dữ liệu từ Google Sheets
print(">>> BƯỚC 1: Đang tải và tổng hợp dữ liệu mới từ Google Sheets...")
try:
    result = subprocess.run(["python", "-u", script_update], check=True, capture_output=True, text=True, encoding='utf-8')
    print(result.stdout)
    print("✓ Tổng hợp dữ liệu thành công!")
except subprocess.CalledProcessError as e:
    print("\n[LỖI] Không thể tổng hợp dữ liệu từ Google Sheets:")
    print(e.stdout)
    print(e.stderr)
    sys.exit(1)

# 2. Đẩy lên GitHub
print("\n>>> BƯỚC 2: Đang tải dữ liệu mới lên trang web GitHub...")
files_to_push = [
    r"LDN PA/Vitality Compass/operations_data.json",
    r"LDN PA/Operations_Insights.md"
]

try:
    # Git add
    print("  * Đang chuẩn bị tệp tin...")
    for file in files_to_push:
        if os.path.exists(file):
            subprocess.run([git_exe, "add", file], check=True)

    # Git commit
    now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    commit_msg = f"Auto-update data: {now_str}"
    print(f"  * Đang tạo bản ghi commit: '{commit_msg}'...")
    subprocess.run([git_exe, "commit", "-m", commit_msg], check=True)

    # Git push
    print("  * Đang truyền dữ liệu lên GitHub...")
    subprocess.run([git_exe, "push", "origin", "main"], check=True)

    print("\n==========================================================")
    print("🎉 CẬP NHẬT TRANG WEB THÀNH CÔNG!")
    print("👉 Chị hãy mở link web bên dưới và bấm F5 (Làm mới) để xem:")
    print("   https://baotranngocle1410kt-sys.github.io/DashboardDCL/")
    print("==========================================================")
except Exception as e:
    print(f"\n[LỖI] Thất bại khi đẩy lên GitHub: {e}")
    sys.exit(1)
