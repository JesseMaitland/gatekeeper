import string
import secrets
import json
from pathlib import Path
from hashlib import md5
from cryptography.fernet import Fernet


def generate_password() -> str:
    punctuation = '!#$%&()*+,-/:;<=>?@[]^_{|}'
    choices = string.ascii_letters + string.digits + punctuation
    return ''.join(secrets.choice(choices) for i in range(30))


def create_md5_password_hash(user_name: str, password: str) -> str:
    pwd_str = user_name + password
    hashed_pwd = md5(pwd_str.encode()).hexdigest()
    return f"md5{hashed_pwd}"


def encrypt_password(password: str, fernet: Fernet) -> str:
    return fernet.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password: str, fernet: Fernet) -> str:
    return fernet.decrypt(encrypted_password.encode()).decode()


def get_fernet(secrets_path: Path) -> Fernet:
    return Fernet(json.load(secrets_path.open(mode='r'))['key'])
