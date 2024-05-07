from contextlib import contextmanager
from datetime import datetime
from typing import Any, Generator

import pydantic
from flask import g
from sqlalchemy import text
from sqlalchemy.orm import Session


class PydanticBaseModel(pydantic.BaseModel):
    model_config = {"from_attributes": True}


@contextmanager
def db_session() -> Generator[Session, None, None]:
    """Get a plain SQLAlchemy Session."""
    session = g.get("db")
    if session is None:
        raise Exception("No database session available in application context")

    yield session


def health_deep() -> tuple[dict[str, Any], int, dict[str, str]]:
    with db_session() as session:
        session.execute(text("SELECT 1;")).one()
        return (
            {
                "status": "up",
                "timestamp": datetime.now(),
                "apiName": "opr-api",
                "apiVersion": "v1",
                "components": {"db": {"status": "up"}},
            },
            200,
            {"Content-Type": "application/json"},
        )


def health() -> tuple[dict[str, Any], int, dict[str, str]]:
    return (
        {
            "status": "up",
            "timestamp": datetime.now(),
            "apiName": "opr-api",
            "apiVersion": "v1",
        },
        200,
        {"Content-Type": "application/json"},
    )
