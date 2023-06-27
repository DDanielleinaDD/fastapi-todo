from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    '''Класс пользователя.'''
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    register_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP,
                                                   default=datetime.utcnow)
    email: Mapped[str] = mapped_column(
            String(length=320), unique=True, index=True, nullable=False
        )
    hashed_password: Mapped[str] = mapped_column(
            String(length=1024), nullable=False
        )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True,
                                            nullable=True)
    is_superuser: Mapped[bool] = mapped_column(
            Boolean, default=False, nullable=True
        )
    is_verified: Mapped[bool] = mapped_column(
            Boolean, default=True, nullable=True
        )
    todo = relationship('Todo', back_populates='owner',
                        cascade='all, delete-orphan')
