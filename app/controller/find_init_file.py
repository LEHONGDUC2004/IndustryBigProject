import os

def find_flask_app_file(base_path):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Điều kiện tìm Flask app or SQLAlchemy URI
                        if "Flask(__name__)" in content or "SQLALCHEMY_DATABASE_URI" in content:
                            return file_path
                except Exception as e:
                    print(f"[!] Bỏ qua file {file_path} do lỗi: {e}")
                    continue
    return None
