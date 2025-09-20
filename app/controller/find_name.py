import os


def find_executable_python_file(project_path):
    for root, dirs, files in os.walk(project_path):
        # Bỏ qua thư mục không cần thiết
        dirs[:] = [d for d in dirs if d not in ('venv', '.venv', '__pycache__', '.git')]

        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if '__main__' in content and 'app.run' in content:
                            return os.path.relpath(full_path, project_path)
                except Exception as e:
                    print(f"[] Không thể đọc file {full_path}: {e}")
    return None
