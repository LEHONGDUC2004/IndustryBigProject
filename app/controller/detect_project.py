import os

def detect_project_type(project_path):
    has_py = False
    has_html = False

    for root, dirs, files in os.walk(project_path):
        for filename in files:
            if filename.endswith('.py'):
                has_py = True
            elif filename.endswith('.html'):
                has_html = True

    if has_py:
        return 'flask'
    elif has_html:
        return 'static'
    else:
        return 'unknown'
