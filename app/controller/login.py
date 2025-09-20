import hashlib

from app.models import User
from app import login_manager

def check_login(username, password):
    if username and password:
        hashed_password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
        return User.query.filter_by(name_account=username.strip(), password=hashed_password).first()

def is_active(account_id):
    account = User.query.get(account_id)
    return account.status if account else None

# Flask-Login sẽ gọi hàm này để load user từ ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))