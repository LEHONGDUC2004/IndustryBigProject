from app import login_manager
from flask_login import current_user
from sqlalchemy import func
import hashlib
from app.models import User
from app import db
import re



def mapping_account(name_account,user_id):
    account=User.query.filter(User.name_account.__eq__(name_account.strip())).first()
    account.user_id=user_id
    db.session.commit()


def is_format_password(password):
    if len(password) < 8:
        return False, "Mật khẩu phải có ít nhất 8 ký tự."

    if not re.search(r'[A-Z]', password):
        return False, "Mật khẩu phải chứa ít nhất một chữ cái viết hoa."

    if not re.search(r'[a-z]', password):
        return False, "Mật khẩu phải chứa ít nhất một chữ cái viết thường."

    if not re.search(r'\d', password):
        return False, "Mật khẩu phải chứa ít nhất một chữ số."

    if not re.search(r'[!@#$%^&*()\-_=+]', password):
        return False, "Mật khẩu phải chứa ít nhất một ký tự đặc biệt (!@#$%^&*()-_+=)."

    return True, "Mật khẩu hợp lệ."

def change_password(id,password):
    pass