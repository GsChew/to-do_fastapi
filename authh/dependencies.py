from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError

from app.config import SECRET_KEY, ALGORITHM
from app.database import SessionDep
from app.models import User


# Схема получения токена из Authorization: Bearer ...
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Декодируем JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except PyJWTError:
        raise credentials_exception


    # Ищем пользователя в БД
    user = await session.get(User, int(user_id))

    if user is None:
        raise credentials_exception

    return user
