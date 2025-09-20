import re

def replace_database_name(sql_path, new_db_name, db_user, db_password):
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Tìm tên cũ trong câu lệnh CREATE DATABASE hoặc USE
    match = re.search(r'(CREATE DATABASE|USE)\s+`?([a-zA-Z0-9_]+)`?', sql_content, re.IGNORECASE)
    if match:
        old_name = match.group(2)
        print(f"Phát hiện database cũ: {old_name} → sẽ thay bằng: {new_db_name}")

        # Thay tất cả tên cũ bằng tên mới (kể cả trong INSERT, FK, ...)
        sql_content = re.sub(rf'\b{old_name}\b', new_db_name, sql_content)
    else:
        print("Không tìm thấy tên database cũ — sẽ thêm mới phần khởi tạo.")

    # Kiểm tra nếu file chưa có CREATE USER thì thêm đoạn user vào đầu
    user_block = f"""CREATE DATABASE IF NOT EXISTS `{new_db_name}`;
CREATE USER IF NOT EXISTS '{db_user}'@'%' IDENTIFIED BY '{db_password}';
GRANT ALL PRIVILEGES ON `{new_db_name}`.* TO '{db_user}'@'%';
FLUSH PRIVILEGES;
USE `{new_db_name}`;\n\n"""

    if not re.search(r'CREATE\s+USER', sql_content, re.IGNORECASE):
        print("Chưa có CREATE USER → thêm đoạn user vào đầu file.")
        sql_content = user_block + sql_content
    else:
        print("Đã có CREATE USER → giữ nguyên phần đầu.")

    # Ghi đè lại file
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write(sql_content)
