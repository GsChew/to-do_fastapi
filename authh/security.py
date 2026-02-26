from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

from app.config import SECRET_KEY, ALGORITHM


password_hasher = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher(),
    )
)


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    valid, _ = password_hasher.verify_and_update(
        plain_password,
        hashed_password,
    )
    return valid


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta,
) -> str:

    expire = datetime.now(timezone.utc) + expires_delta

    payload = {
        "sub": str(subject),
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return token