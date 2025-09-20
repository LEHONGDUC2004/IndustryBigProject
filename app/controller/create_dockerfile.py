import os
from app.controller.find_entrypoint_and_pythonpath import find_entrypoint_and_pythonpath


def create_dockerfile(project_path, project_type):
    project_name = os.path.basename(os.path.abspath(project_path))
    dockerfile_path = os.path.join(project_path, 'Dockerfile')

    with open(dockerfile_path, 'w', encoding='utf-8') as f:
        if project_type == 'static':
            f.write("""\
FROM nginx:stable-alpine
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
""")
        elif project_type == 'nodejs':
            f.write("""\
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]
""")
        elif project_type == 'flask':
            entrypoint, python_path = find_entrypoint_and_pythonpath(project_path)
            if not entrypoint or not python_path:
                raise Exception("Không tìm thấy file chạy chính hợp lệ cho ứng dụng Flask.")

            # Normalize path
            entrypoint = entrypoint.replace("\\", "/")
            docker_workdir = f"/{project_name}"
            pythonpath = f"{docker_workdir}/{python_path}" if python_path != "." else docker_workdir

            # Chuyển file entrypoint sang dạng module
            module_entry = entrypoint[:-3].replace("/", ".")

            # Ghi Dockerfile
            f.write(f"""\
FROM python:3.11-slim
WORKDIR {docker_workdir}
COPY . .
ENV PYTHONPATH={pythonpath}
RUN apt-get update && apt-get install -y gcc libffi-dev libssl-dev
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv cryptography
EXPOSE 80
CMD ["sh", "-c", "sleep 15 && python -m {module_entry}"]
""")
        else:
            raise ValueError("Loại ứng dụng không hợp lệ: chỉ hỗ trợ 'static', 'nodejs', hoặc 'flask'.")
