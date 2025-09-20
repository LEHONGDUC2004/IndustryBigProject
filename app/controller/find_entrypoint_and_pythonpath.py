import os
import ast

def find_entrypoint_and_pythonpath(project_root):
    for root, _, files in os.walk(project_root):
        for file in files:
            if not file.endswith('.py'):
                continue

            full_path = os.path.join(root, file)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tree = ast.parse(content)

                    # Check for if __name__ == "__main__"
                    has_main_check = any(
                        isinstance(node, ast.If)
                        and isinstance(node.test, ast.Compare)
                        and isinstance(node.test.left, ast.Name)
                        and node.test.left.id == "__name__"
                        for node in tree.body
                    )

                    if has_main_check and ("app.run" in content or "create_app()" in content):
                        rel_path = os.path.relpath(full_path, project_root)
                        python_path = os.path.dirname(rel_path)
                        print(f" Tìm thấy file entrypoint: {rel_path}")
                        print(f" PYTHONPATH: {python_path or '.'}")
                        return rel_path.replace("\\", "/"), python_path or "."
            except Exception as e:
                print(f" Lỗi đọc hoặc parse file {full_path}: {e}")

    print("️ Không tìm thấy entrypoint phù hợp trong dự án.")
    return None, None
