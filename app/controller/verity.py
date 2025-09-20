from werkzeug.security import generate_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

# Hàm tạo mã xác thực ngẫu nhiên
def generate_verification_code(length=6):
    return ''.join(random.choices('0123456789', k=length))


def send_verification_email(user_email, user_name, verification_code):
    # Cấu hình trực tiếp thông tin email và mật khẩu
    sender_email = 'lehongduc201204@gmail.com'  # Thay bằng email của bạn
    sender_password = 'owdr wdlt oxnq tjou'  # Thay bằng mật khẩu hoặc mật khẩu ứng dụng

    subject = "Xác Thực Tài Khoản"
    body = f"""
    Chào {user_name},

    Đây là mã xác thực tài khoản của bạn:
    ---------------------------
    Mã xác thực: {verification_code}
    ---------------------------

    Vui lòng nhập mã này vào trang web để hoàn tất đăng ký.

    Trân trọng,
    Đội Hỗ Trợ
    """

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, message.as_string())
        return True
    except Exception as e:
        print(f"Lỗi gửi email: {e}")
        return False