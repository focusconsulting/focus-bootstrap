import os
import time
from typing import List, Union

import connexion  # type: ignore
import connexion.mock  # type: ignore
import flask
from flask import g
from opr_api.db import init
from opr_api.utils.logging import get_logger

logger = get_logger(__name__)


def openapi_filenames() -> List[str]:
    return ["../openapi.yaml"]


def get_project_root_dir() -> str:
    return os.path.join(
        os.path.dirname(__file__),
        "../",
    )


def create_app() -> connexion.FlaskApp:
    logger.info("Starting API")

    db_session_factory = init()

    # Enable mock responses for unimplemented paths.
    resolver = connexion.mock.MockResolver(mock_all=False)

    # TODO validation is not working for responses
    app = connexion.FlaskApp(
        __name__,
        strict_validation=True,
        validate_responses=True,
    )
    app.add_api(
        openapi_filenames()[0],
        resolver=resolver,
        strict_validation=True,
        validate_responses=True,
    )

    flask_app = app.app

    @flask_app.before_request
    def push_db() -> None:
        g.db = db_session_factory
        g.start_time = time.monotonic()
        g.connexion_flask_app = app

    @flask_app.teardown_request
    def close_db(
        exception: Union[Exception | None] = None,
    ) -> None:
        try:
            logger.debug("Closing DB session")
            db = g.pop(
                "db",
                None,
            )

            if db is not None:
                db.remove()
        except Exception:
            logger.exception("Exception while closing DB session")
            pass

    @flask_app.after_request
    def access_log_end(
        response: flask.Response,
    ) -> flask.Response:
        response_time_ms = 1000 * (time.monotonic() - g.get("start_time"))
        logger.info(
            "%s %s %s",
            response.status_code,
            flask.request.method,
            flask.request.full_path,
            extra={
                "remote_addr": flask.request.remote_addr,
                "response_length": response.content_length,
                "response_type": response.content_type,
                "status_code": response.status_code,
                "response_time_ms": response_time_ms,
            },
        )
        return response

    return app
