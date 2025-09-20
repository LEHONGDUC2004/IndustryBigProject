
from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify,flash
from flask_login import login_user, logout_user, current_user
import app.controller.login as lg
import app.controller.create_account as cra
import app.controller.infor_user as inf
import app.models as mdl
import app.controller.verity as ver

auth_bp = Blueprint('auth', __name__)



# Route đăng nhập
@auth_bp.route('/login/data', methods=['GET', 'POST'])
def user_signin():
    # Xóa tất cả thông báo flash
    session.pop('_flashes', None)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = lg.check_login(username, password)
        if user:
            login_user(user)
            return redirect(url_for('main.index_login'))

        flash('Tài khoản hoặc mật khẩu không chính xác', 'error')

        return redirect(url_for('main.login'))
    return redirect(url_for('main.login'))

@auth_bp.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('main.login'))

@auth_bp.route('/register/data', methods=['GET', 'POST'])
def user_register():
    # Xóa tất cả thông báo flash
    session.pop('_flashes', None)
    if request.method.__eq__('POST'):
        user_name = request.form.get('name_user')
        password = request.form.get('password')
        re_en_password = request.form.get('re_en_password')
        email = request.form.get('email')

        result,mess=inf.is_format_password(password)

        if result:
            if password == re_en_password:
                  # Tạo mã xác thực ngẫu nhiên
                verification_code = ver.generate_verification_code()

                # Lưu thông tin đăng ký tạm thời vào session
                session['verification_code'] = verification_code
                session['user_registration'] = {
                    'name_user': user_name,
                    'password': password,
                    'email': email
                }

                # Gửi email xác thực
                if ver.send_verification_email(email, user_name, verification_code):
                    # Chuyển hướng tới file `verify.html` để nhập mã OTP
                    return redirect(url_for('main.verify'))
                else:
                    flash('Không thể gửi email xác thực. Vui lòng thử lại sau.', 'error')
                    # Nếu gửi email thất bại, thông báo lỗi
                    return redirect(url_for('main.register'))
            else:
                flash('Mật khẩu không khớp', 'error')
                return redirect(url_for('main.register'))
        else:
            flash(mess, 'error')
            return redirect(url_for('main.register'))

    flash('Đăng ký thất bại không tìm thấy dữ liêu', 'error')
    # Hiển thị trang đăng ký
    return redirect(url_for('main.register'))


@auth_bp.route('/verify', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp = request.form.get('otp')

        # Kiểm tra mã OTP
        if otp == session.get('verification_code'):
            # Lấy thông tin người dùng từ session
            user_registration = session.get('user_registration')
            account = cra.create_account(name_account=user_registration['name_user'], password=user_registration['password'], email=user_registration['email'])
            # Xóa thông tin tạm thời khỏi session
            session.pop('verification_code', None)
            session.pop('user_registration', None)

            # Chuyển hướng tới trang chủ hoặc trang đăng nhập
            return redirect(url_for('main.login'))  # Hoặc trang khác bạn muốn

        else:
            flash("Mã OTP không đúng. Vui lòng thử lại.",'error')
            return redirect(url_for('main.verify'))

    return redirect(url_for('main.verify'))


@auth_bp.route('/login-admin', methods=['GET', 'POST'], endpoint="admin_login")
def login_admin_process():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        # check user có quyền admin
        from app.models import User
        from werkzeug.security import check_password_hash

        user = User.query.filter_by(name_account=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("admin.index"))  # vào dashboard admin

        flash("Sai tài khoản hoặc mật khẩu", "error")
        return redirect(url_for("auth.admin_login"))

    # nếu GET thì hiển thị form
    return render_template("admin_login.html")
