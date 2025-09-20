import os
import re
from app.controller.find_name import find_executable_python_file


def find_port_host(project_path):
    target_file_rel = find_executable_python_file(project_path)
    if not target_file_rel:
        return None

    target_file_path = os.path.join(project_path, target_file_rel)

    with open(target_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Tìm dòng app.run(...)
    pattern = r'app\.run\((.*?)\)'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return None

    args_str = match.group(1)

    # Loại bỏ port=... nếu có (để thêm lại đúng sau)
    args_str = re.sub(r'port\s*=\s*\d+\s*,?', '', args_str)

    # Thêm host='0.0.0.0' nếu chưa có
    if "host=" not in args_str:
        args_str = args_str.strip()
        if args_str:
            args_str += ", host='0.0.0.0'"
        else:
            args_str = "host='0.0.0.0'"

    # Thêm port=80 nếu chưa có
    if "port=" not in args_str:
        args_str += ", port=80"

    # Làm sạch dấu phẩy dư thừa
    args_str = re.sub(r',\s*,', ',', args_str).strip().strip(',')

    # Tạo dòng mới
    new_run_line = f"app.run({args_str})"

    # Thay thế dòng cũ
    new_content = re.sub(pattern, new_run_line, content, flags=re.DOTALL)

    # Ghi lại file
    with open(target_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return target_file_rel
