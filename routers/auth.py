from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import (
    verify_password,
    create_access_token,
)
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import get_db
from app.models import User


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):

    stmt = select(User).where(
        User.email == form_data.username
    )

    result = await db.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    expires = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token = create_access_token(
        subject=user.id,
        expires_delta=expires,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }