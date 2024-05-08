from typing import Self

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __tablename__(cls: Self) -> str:
        return cls.__name__.lower()
