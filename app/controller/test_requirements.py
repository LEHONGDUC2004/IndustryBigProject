import os
import shutil

def ensure_requirements_at_root(root_path="."):
    root_path = os.path.abspath(root_path)
    req_at_root = os.path.join(root_path, "requirements.txt")

    if os.path.exists(req_at_root):
        print("requirements.txt đã nằm ở thư mục gốc.")
        return

    # Duyệt đệ quy để tìm
    for dirpath, dirnames, filenames in os.walk(root_path):
        if "requirements.txt" in filenames:
            found_path = os.path.join(dirpath, "requirements.txt")
            print(f"Tìm thấy requirements.txt tại: {found_path}")

            # Di chuyển lên root
            shutil.move(found_path, req_at_root)
            print(f"Đã di chuyển requirements.txt về: {req_at_root}")
            return

    print("Không tìm thấy requirements.txt trong project.")
