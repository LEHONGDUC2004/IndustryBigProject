from app.routes.main_route import main_bp
from app.routes.upload_all import uploadAll_bp
from app.routes.auth_route import auth_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(uploadAll_bp, url_prefix='/upload_all')

