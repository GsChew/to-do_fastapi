from pwdlib import PasswordHash
from typing import Any
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher
import jwt
from datetime import datetime, timedelta, timezone
from app.config import SECRET_KEY, ALGORITHM


password_hash = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher(),
    )
)

def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {'exp': expire, 'sub': str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> tuple[bool, str | None]:
    return password_hash.verify_and_update(plain_password, hashed_password)
