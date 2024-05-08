import os

import connexion  # type: ignore
import pytest

from opr_api.app import create_app


@pytest.fixture(autouse=True)
def set_db_env() -> None:
    os.environ["POSTGRES_CONNECTION_STRING"] = (
        "postgresql+psycopg2://opr:secret123@localhost:5432/opr"
    )


@pytest.fixture
def test_client() -> connexion.FlaskApp:
    return create_app().test_client()
