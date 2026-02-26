from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import User
from app.authh.security import verify_password, create_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):

    # 1. Ищем пользователя
    stmt = select(User).where(User.email == form_data.username)
    result = await db.execute(stmt)

    user = result.scalar_one_or_none()

    # 2. Проверяем: существует ли
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # 3. Проверяем пароль
    valid, _ = verify_password(
        form_data.password,
        user.password_hash,
    )

    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # 4. Время жизни токена
    access_token_expires = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # 5. Генерируем JWT
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )

    # 6. Отдаём клиенту
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }