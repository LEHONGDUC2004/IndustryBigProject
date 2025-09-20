from sqlalchemy.exc import IntegrityError
from app.models import User  # Import đúng model
from app import db
import hashlib

def create_account(name_account, password, email):
    if name_account and password:
        # Kiểm tra nếu tài khoản đã tồn tại
        existing = User.query.filter_by(name_account=name_account).first()
        if existing:
            return 'Tài khoản đã tồn tại'

        # Hash password
        hashed_password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()

        # Tạo mới account
        account = User(name_account=name_account, password=hashed_password, email=email)
        db.session.add(account)

        try:
            db.session.commit()
            return 'Tạo tài khoản thành công'
        except IntegrityError:
            db.session.rollback()
            return 'Tài khoản đã tồn tại (lỗi ghi DB)'
    return 'Tạo tài khoản không thành công'
