from flask import Flask
from app.extensions import db, login_manager
from app.models import User
from app.admin import init_admin
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret123456'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@db/upload_app'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Vui lòng đăng nhập để tiếp tục.'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import register_routes
    register_routes(app)

    with app.app_context():
        db.create_all()

        # tạo user admin mặc định nếu chưa có
        if not User.query.filter_by(email="admin@example.com").first():
            u = User(
                email="admin@example.com",
                name_account="admin",
                password=generate_password_hash("Admin@123"),
                status=True
            )
            db.session.add(u)
            db.session.commit()
            print("Admin mặc định đã được tạo: admin / Admin@123")

    init_admin(app)

    return app
