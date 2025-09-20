import app.routes.upload_all

# === Kiểm tra định dạng file ===
ALLOWED_EXTENSIONS = {'zip'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

