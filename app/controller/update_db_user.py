import os

def remove_sqlalchemy_uri(file_path):
    if not os.path.exists(file_path):
        print("Không tìm thấy file:", file_path)
        return

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Lọc bỏ các dòng có chứa SQLALCHEMY_DATABASE_URI
    new_lines = [line for line in lines if "app.config['SQLALCHEMY_DATABASE_URI']" not in line]

    with open(file_path, 'w') as f:
        f.writelines(new_lines)

    print("Đã xóa dòng chứa SQLALCHEMY_DATABASE_URI trong", file_path)
