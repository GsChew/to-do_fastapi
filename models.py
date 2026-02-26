from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base
from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(datetime.UTC))
    tasks: Mapped[list['Task']] = relationship("Task", back_populates="user")


class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[str]
    deadline: Mapped[datetime | None]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship("User", back_populates="tasks")
