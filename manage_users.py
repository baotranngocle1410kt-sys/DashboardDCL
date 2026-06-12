"""
Quản lý tài khoản Dashboard ĐCL
Chạy: python manage_users.py
"""
import json
import hashlib
import os
import subprocess

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LDN PA", "users.json")
USERS_FILE_VC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LDN PA", "Vitality Compass", "users.json")

def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(data):
    content = json.dumps(data, indent=2, ensure_ascii=False)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    with open(USERS_FILE_VC, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Đã lưu file users.json")

def hash_password(pw):
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def list_users(data):
    print("\n👥 Danh sách tài khoản:")
    print(f"{'STT':<5}{'Tên':<20}{'Email':<30}{'Vai trò':<10}{'Ngày tạo':<12}")
    print("-" * 77)
    for i, u in enumerate(data["users"], 1):
        role_icon = "👑" if u["role"] == "owner" else ("🚫" if u["role"] == "blocked" else "👤")
        print(f"{i:<5}{u['name']:<20}{u['email']:<30}{role_icon} {u['role']:<8}{u.get('createdAt','N/A'):<12}")
    print()

def add_user(data):
    print("\n➕ Thêm tài khoản mới:")
    name = input("   Tên hiển thị: ").strip()
    email = input("   Email: ").strip().lower()
    password = input("   Mật khẩu: ").strip()
    
    if not name or not email or not password:
        print("❌ Vui lòng nhập đủ thông tin.")
        return
    
    if any(u["email"].lower() == email for u in data["users"]):
        print(f"❌ Email {email} đã tồn tại.")
        return
    
    role = input("   Vai trò (user/owner) [mặc định: user]: ").strip() or "user"
    
    from datetime import date
    data["users"].append({
        "email": email,
        "passwordHash": hash_password(password),
        "role": role,
        "name": name,
        "createdAt": str(date.today())
    })
    save_users(data)
    print(f"✅ Đã thêm: {name} ({email}) - {role}")

def delete_user(data):
    list_users(data)
    try:
        idx = int(input("Nhập STT user muốn xóa: ")) - 1
        if data["users"][idx]["role"] == "owner":
            print("❌ Không thể xóa tài khoản Owner.")
            return
        user = data["users"].pop(idx)
        save_users(data)
        print(f"✅ Đã xóa: {user['name']} ({user['email']})")
    except (ValueError, IndexError):
        print("❌ STT không hợp lệ.")

def reset_password(data):
    list_users(data)
    try:
        idx = int(input("Nhập STT user muốn đổi mật khẩu: ")) - 1
        new_pw = input("Mật khẩu mới: ").strip()
        if not new_pw:
            print("❌ Mật khẩu không được trống.")
            return
        data["users"][idx]["passwordHash"] = hash_password(new_pw)
        save_users(data)
        print(f"✅ Đã đổi mật khẩu cho: {data['users'][idx]['name']}")
    except (ValueError, IndexError):
        print("❌ STT không hợp lệ.")

def git_push():
    print("\n📤 Đang push lên GitHub...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(["git", "add", "LDN PA/users.json", "LDN PA/Vitality Compass/users.json"], check=True)
    subprocess.run(["git", "commit", "-m", "Update users"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("✅ Đã push lên GitHub! Đợi 2-3 phút để website cập nhật.")

def main():
    print("=" * 50)
    print("  🧭 QUẢN LÝ TÀI KHOẢN DASHBOARD ĐCL")
    print("=" * 50)
    
    data = load_users()
    
    while True:
        print("\nChọn thao tác:")
        print("  1. 👥 Xem danh sách tài khoản")
        print("  2. ➕ Thêm tài khoản mới")
        print("  3. ❌ Xóa tài khoản")
        print("  4. 🔑 Đổi mật khẩu")
        print("  5. 📤 Push lên GitHub (áp dụng thay đổi)")
        print("  0. 🚪 Thoát")
        
        choice = input("\n👉 Chọn (0-5): ").strip()
        
        if choice == "1":
            list_users(data)
        elif choice == "2":
            add_user(data)
        elif choice == "3":
            delete_user(data)
        elif choice == "4":
            reset_password(data)
        elif choice == "5":
            git_push()
        elif choice == "0":
            print("👋 Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()
