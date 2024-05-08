import datetime
from typing import Any

from sqlalchemy import text

from opr_api.app import db_session


def health_deep() -> tuple[dict[str, Any], int, dict[str, str]]:
    with db_session() as session:
        session.execute(text("SELECT 1;")).one()
        return (
            {
                "status": "up",
                "timestamp": datetime.datetime.now(datetime.UTC),
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
            "timestamp": datetime.datetime.now(datetime.UTC),
            "apiName": "opr-api",
            "apiVersion": "v1",
        },
        200,
        {"Content-Type": "application/json"},
    )
