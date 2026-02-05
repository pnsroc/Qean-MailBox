from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from .config import settings
from Crypto.Cipher import AES
import base64

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p: str) -> str:
    return pwd_context.hash(p)

def verify_password(p: str, h: str) -> bool:
    return pwd_context.verify(p, h)

def create_access_token(data: dict, expires_minutes: int = 60 * 24):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

# 简单 AES 封装（生产可再加强）
def _pad(s: bytes) -> bytes:
    pad_len = 16 - len(s) % 16
    return s + bytes([pad_len]) * pad_len

def _unpad(s: bytes) -> bytes:
    pad_len = s[-1]
    return s[:-pad_len]

def encrypt(text: str) -> str:
    key = settings.AES_KEY.encode()
    cipher = AES.new(key, AES.MODE_ECB)
    enc = cipher.encrypt(_pad(text.encode()))
    return base64.b64encode(enc).decode()

def decrypt(text: str) -> str:
    key = settings.AES_KEY.encode()
    cipher = AES.new(key, AES.MODE_ECB)
    raw = base64.b64decode(text)
    dec = _unpad(cipher.decrypt(raw))
    return dec.decode()
