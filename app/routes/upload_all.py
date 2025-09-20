from flask import Blueprint, request, redirect, session, url_for
from werkzeug.utils import secure_filename
from app.controller.allowed_file import allowed_file
from app.controller.detect_project import detect_project_type
from app.controller.create_dockerfile import create_dockerfile
from app.controller.create_dockercompose import create_compose
from app.controller.convert_db import import_sql_to_mysql
from app.controller.replace_db_uri import replace_or_add_sqlalchemy_uri
from app.controller.replacename_db import replace_database_name
from app.controller.find_init_file import find_flask_app_file
from app.controller.test_requirements import ensure_requirements_at_root
from app.routes.jenkins_trigger import trigger_via_generic
from app.controller.test_host_port import find_port_host
from app.models import Project, Deployment
from flask_login import current_user, login_required
from app import db
from app.controller.cryto_utils import encrypt_data
from app.controller.upload_to_s3 import upload_to_s3
from app.controller.cleanup_temp_files import cleanup_temp_files
from app.controller.download_from_github import download_public_zip


import app.controller.counter as counter
import os
import shutil
import zipfile


uploadAll_bp = Blueprint('upload_all', __name__)

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/data/uploaded")
EXTRACT_DIR = os.environ.get("EXTRACT_DIR", "/data/extracted")
REPLACED_DIR = os.environ.get("REPLACED_DIR", "/data/replaced")

# Ensure directories exist
for p in [UPLOAD_DIR, EXTRACT_DIR, REPLACED_DIR]:
    os.makedirs(p, exist_ok=True)

@uploadAll_bp.route('/upload_all', methods=['POST'])
@login_required
def upload_all():
    # 1. Get DB info
    db_info = {
        'DB_NAME': request.form.get('name_database'),
        'DB_USER': request.form.get('name_user'),
        'DB_HOST': request.form.get('host_db'),
        'DB_PASSWORD': request.form.get('passwd')
    }
    # session['db_info'] = db_info
    github_url = request.form.get("github_url", "").strip()
    github_ref = request.form.get("github_ref", "").strip() or None
    # 2. Save .sql file if exists
    sql_file = request.files.get('file_sql')
    sql_filename = None
    if sql_file and sql_file.filename:
        sql_filename = secure_filename(sql_file.filename)
        sql_path = os.path.join(UPLOAD_DIR, sql_filename)
        sql_file.save(sql_path)

        replace_database_name(sql_path=sql_path,
                              new_db_name=db_info['DB_NAME'],
                              db_user=db_info['DB_USER'],
                              db_password=db_info['DB_PASSWORD'])

        import_sql_to_mysql(sql_path, db_info)

    if github_url:
        zip_path, zip_filename = download_public_zip(github_url, UPLOAD_DIR, ref=github_ref)
    else:
        # 3. Handle ZIP file
        zip_file = request.files.get('file_zip')
        if not zip_file or not allowed_file(zip_file.filename):
            return 'Invalid ZIP file.', 400

        zip_filename = secure_filename(zip_file.filename)
        zip_path = os.path.join(UPLOAD_DIR, zip_filename)
        zip_file.save(zip_path)


    # Extract project
    project_name = zip_filename.rsplit('.', 1)[0]
    # tạo file đếm
    counter.zip_count += 1

    extract_path = os.path.join(EXTRACT_DIR, project_name)
    os.makedirs(extract_path, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    subdirs = [d for d in os.listdir(extract_path) if os.path.isdir(os.path.join(extract_path, d))]
    project_real_path = os.path.join(extract_path, subdirs[0]) if len(subdirs) == 1 else extract_path

    ensure_requirements_at_root(project_real_path)

    # Copy .sql file into project if exists
    if sql_filename:
        shutil.copy(sql_path, os.path.join(project_real_path, sql_filename))

    find_port_host(project_real_path)

    init_file_path = find_flask_app_file(project_real_path)
    project_type = detect_project_type(project_real_path)

    create_dockerfile(project_real_path, project_type)

    create_compose(docker_path=project_real_path,
                   name_database=db_info['DB_NAME'],
                   name_user=db_info['DB_USER'],
                   host_db=db_info['DB_HOST'],
                   passwd=db_info['DB_PASSWORD'],
                   filename_sql=sql_filename,
                   index=counter.zip_count)

    project = Project(
        name=project_name,
        account_id=current_user.id,
        name_sql=sql_filename,
        name_database=db_info['DB_NAME'],
        name_host=db_info['DB_HOST'],
        name_user=db_info['DB_USER'],
        passwd=db_info['DB_PASSWORD']
    )

    replace_or_add_sqlalchemy_uri(init_file_path, project)

    # mã hóa và lưu vào DB
    project.name_database = encrypt_data(project.name_database)
    project.name_host = encrypt_data(project.name_host)
    project.name_user = encrypt_data(project.name_user)
    project.passwd = encrypt_data(project.passwd)

    db.session.add(project)
    db.session.commit()
    session['last_project_id'] = project.id
    # 7. Compress modified project
    replaced_path = os.path.join(REPLACED_DIR, zip_filename)
    shutil.make_archive(replaced_path.rsplit('.', 1)[0], 'zip',
                        root_dir=os.path.dirname(project_real_path),
                        base_dir=os.path.basename(project_real_path))
    final_zip_path = replaced_path
    # upload source code lên s3
    s3_key = upload_to_s3(final_zip_path, zip_filename, current_user.id, project.id)

    deployment = Deployment(
        project_id=project.id,
        zip_filename=zip_filename,
        status="pending"
    )
    db.session.add(deployment)
    db.session.commit()
    dep_id = deployment.id
    session['last_deploy_id'] = dep_id
    trigger_via_generic(zip_filename, s3_key, dep_id)

    cleanup_temp_files(
        project_name=project_name,
        zip_filename=zip_filename,
        upload_dir=UPLOAD_DIR,
        extract_dir=EXTRACT_DIR,
        replaced_dir=REPLACED_DIR
    )
    return redirect(url_for('main.success', name=project_name))



