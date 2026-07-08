import base64
from cryptography.fernet import Fernet
from config import Config

# Ensure key is correctly padded for Fernet
_key = base64.urlsafe_b64encode(Config.ENCRYPTION_KEY[:32].ljust(32, b'\0'))
cipher = Fernet(_key)

def encrypt_session(session_string: str) -> str:
    return cipher.encrypt(session_string.encode()).decode()

def decrypt_session(encrypted_string: str) -> str:
    return cipher.decrypt(encrypted_string.encode()).decode()
  
