import datetime
from typing import Any

from sqlalchemy import text

from opr_api.app import db_session
from opr_api.controllers.response import success_response


def health_deep() -> tuple[dict[str, Any], int, dict[str, str]]:
    with db_session() as session:
        session.execute(text("SELECT 1;")).one()
        return success_response(
            "Response",
            {
                "status": "up",
                "timestamp": datetime.datetime.now(datetime.UTC),
                "apiName": "opr-api",
                "apiVersion": "v1",
                "components": {"db": {"status": "up"}},
            },
        ).to_api_response()


def health() -> tuple[dict[str, Any], int, dict[str, str]]:
    return success_response(
        "Success",
        {
            "status": "up",
            "timestamp": datetime.datetime.now(datetime.UTC),
            "apiName": "opr-api",
            "apiVersion": "v1",
        },
    ).to_api_response()
