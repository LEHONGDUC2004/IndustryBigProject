
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

KEY_SERVER = os.getenv("KEY_SERVER")
key = Fernet(KEY_SERVER)


def encrypt_data(plain_text):
    # Mã hóa chuỗi
    return key.encrypt(plain_text.encode()).decode()

def decrypt_data(encrypted_text):
    # Giải mã chuỗi
    return key.decrypt(encrypted_text.encode()).decode()
