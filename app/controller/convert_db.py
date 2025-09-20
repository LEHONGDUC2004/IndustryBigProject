import subprocess

def import_sql_to_mysql(sql_path, db_info):
    command = [
        'mysql',
        f"-h{db_info['DB_HOST']}",
        f"-u{db_info['DB_USER']}",
        f"-p{db_info['DB_PASSWORD']}"
    ]

    docker_command = ['docker', 'exec', '-i', 'flask_mysql_host'] + command

    try:
        with open(sql_path, 'rb') as f:
            process = subprocess.Popen(docker_command, stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            if process.returncode == 0:
                print("Import .sql thành công")
            else:
                print("Import thất bại:")
                print(err.decode())
    except FileNotFoundError:
        print(" không tìm thấy lệnh docker")
