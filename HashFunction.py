import bcrypt
import re
import json
import os
import hashlib

USERS_FILE = "users.json"
INTEGRITY_FILE = "users_hash.txt"


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


def password_strength(pw, username=""):
    score = 0
    if len(pw) >= 8:
        score += 1
    if re.search(r"[A-Z]", pw):
        score += 1
    if re.search(r"[a-z]", pw):
        score += 1
    if re.search(r"[0-9]", pw):
        score += 1
    if re.search(r"[^A-Za-z0-9]", pw):
        score += 1
    if username.lower() not in pw.lower():
        score += 1

    if score <= 2:
        return "Weak"
    if score <= 4:
        return "Medium"
    return "Strong"


def file_sha256(filename):
    if not os.path.exists(filename):
        return None

    with open(filename, "rb") as f:
        data = f.read()

    return hashlib.sha256(data).hexdigest()


def save_sha256_hash():
    hash_sha256 = file_sha256(USERS_FILE)

    if hash_sha256 is None:
        print("Không tìm thấy file người dùng.")
        return

    with open(INTEGRITY_FILE, "w") as f:
        f.write(hash_sha256)

    print("✅ Đã lưu SHA-256 của users.json vào", INTEGRITY_FILE)
    print("Hash_sha256:", hash_sha256)


def show_integrity_status():
    if not os.path.exists(INTEGRITY_FILE):
        print("⚠️ Chưa có file hash để kiểm tra. Hãy chọn 'Lưu hash'.")
        return

    if not os.path.exists(USERS_FILE):
        print("⚠️ File người dùng không tồn tại.")
        return

    with open(INTEGRITY_FILE) as f:
        saved = f.read().strip()

    current = file_sha256(USERS_FILE)

    print("\n--- KIỂM TRA TOÀN VẸN ---")
    print("Hash đã lưu:   ", saved)
    print("Hash hiện tại: ", current)

    if saved == current:
        print("✅ File toàn vẹn (không bị sửa).")
    else:
        print("❌ File đã bị chỉnh sửa!")

    print("--------------------------\n")


def register_user():
    username = input("Tạo tên tài khoản: ").strip()
    users = load_users()

    if username in users:
        print("Tên đăng nhập đã tồn tại.")
        return

    if not username:
        print("Tên không được để trống.")
        return

    while True:
        pw = input("Nhập mật khẩu: ")
        strength = password_strength(pw, username)
        print("Độ mạnh mật khẩu:", strength)

        if strength == "Strong":
            break
        else:
            print("Mật khẩu yếu, vui lòng nhập lại.")

    hashed_pw = bcrypt.hashpw(
        pw.encode('utf-8'),
        bcrypt.gensalt(12)
    )

    users[username] = {
        "password_hash": hashed_pw.decode('utf-8')
    }

    save_users(users)

    print("\n✅ Đăng ký thành công! Mật khẩu đã được băm bằng bcrypt.")
    print("Hash_bcrypt:", hashed_pw.decode('utf-8')[:60] + "...")

    save_sha256_hash()


def login_user():
    username = input("Nhập tên tài khoản: ").strip()
    users = load_users()

    if username not in users:
        print("Tên đăng nhập không tồn tại.")
        return

    pw = input("Nhập mật khẩu: ")
    stored_hashed_pw = users[username]["password_hash"].encode('utf-8')

    print("\n--- KIỂM TRA MẬT KHẨU ---")
    print("Hash_bcrypt được lấy ra từ file users.json:")
    print(stored_hashed_pw.decode('utf-8'))
    print("So sánh mật khẩu bạn nhập với hash_bcrypt này...")

    if bcrypt.checkpw(pw.encode('utf-8'), stored_hashed_pw):
        print("✅ Đăng nhập thành công!")
    else:
        print("❌ Sai mật khẩu.")


def tamper_users_file():
    if not os.path.exists(USERS_FILE):
        print("⚠️ File người dùng không tồn tại để giả mạo.")
        return

    users = load_users()
    users["_tampered_demo_"] = {
        "password_hash": "tampered_value"
    }

    save_users(users)

    print("⚠️ Đã giả lập tấn công: thêm dữ liệu giả vào users.json")


def main():
    while True:
        print("\n=== HỆ THỐNG DEMO: BCRYPT & KIỂM TRA TOÀN VẸN DỮ LIỆU ===")
        print("1) Đăng ký người dùng")
        print("2) Đăng nhập")
        print("3) Kiểm tra toàn vẹn (SHA-256)")
        print("4) Giả lập tấn công (sửa file users.json)")
        print("5) Thoát")

        choice = input("Chọn: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            show_integrity_status()
        elif choice == "4":
            tamper_users_file()
        elif choice == "5":
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()