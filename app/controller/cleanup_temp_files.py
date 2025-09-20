import os
import shutil


def cleanup_temp_files(project_name, zip_filename,
                       upload_dir, extract_dir, replaced_dir):

    def safe_rmtree(p, base):
        p = os.path.abspath(p)
        base = os.path.abspath(base)
        if p.startswith(base) and os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)

    # Xóa thư mục extract
    project_extract_dir = os.path.join(extract_dir, project_name)
    safe_rmtree(project_extract_dir, extract_dir)

    # Xóa file zip tạm
    for base_dir in [upload_dir, replaced_dir]:
        file_path = os.path.join(base_dir, zip_filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
