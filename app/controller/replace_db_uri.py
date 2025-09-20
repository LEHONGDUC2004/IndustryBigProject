from app.controller.cryto_utils import decrypt_data
import os

def replace_or_add_sqlalchemy_uri(file_path, project=None):
    if not os.path.exists(file_path):
        print(f"Không tìm thấy file tại: {file_path}")
        return

    if not project:
        print("Project không được truyền vào")
        return

    #  Giải mã thông tinn
    real_db_name = project.name_database
    real_user = project.name_user
    real_pass = project.passwd
    real_host = project.name_host or "db"
    new_uri_line = (
        "app.config['SQLALCHEMY_DATABASE_URI'] = "
        f"'mysql+pymysql://{real_user}:{real_pass}@{real_host}/{real_db_name}?charset=utf8mb4'"
    )
    #  Thay vào file
    with open(file_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0)

        if 'SQLALCHEMY_DATABASE_URI' in content:
            # Ghi đè
            lines = content.splitlines()
            lines = [
                new_uri_line if 'SQLALCHEMY_DATABASE_URI' in line else line
                for line in lines
            ]
            f.write('\n'.join(lines))
        else:
            # Ghi thêm nếu chưa có
            f.write('\n' + new_uri_line)
        f.truncate()
