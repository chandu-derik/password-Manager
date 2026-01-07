import base64
import hashlib
from cryptography.fernet import Fernet

def derive_key(master_password: str) -> Fernet:
    key = hashlib.sha256(master_password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))