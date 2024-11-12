import os

import connexion  # type: ignore
import pytest
from focus_api.app import create_app


@pytest.fixture(autouse=True)
def set_db_env() -> None:
    os.environ["POSTGRES_CONNECTION_STRING"] = (
        "postgresql+psycopg2://focus:secret123@localhost:5432/focus"
    )


@pytest.fixture
def test_client() -> connexion.FlaskApp:
    return create_app().test_client()
