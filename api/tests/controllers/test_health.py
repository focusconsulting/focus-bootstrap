import datetime
from typing import Self

import connexion  # type: ignore
from freezegun import freeze_time


class TestHealth:

    @freeze_time("2024-07-26")
    def test_get_health_endpoint(self: Self, test_client: connexion.FlaskApp) -> None:
        now = datetime.datetime.now(datetime.UTC)
        response = test_client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data == {
            "status": "up",
            "timestamp": now.isoformat(),
            "apiName": "opr-api",
            "apiVersion": "v1",
        }

    @freeze_time("2024-07-26")
    def test_get_health_deep_endpoint(self: Self, test_client: connexion.FlaskApp) -> None:
        now = datetime.datetime.now(datetime.UTC)
        response = test_client.get("/v1/health/deep")
        assert response.status_code == 200
        data = response.json()
        assert data == {
            "status": "up",
            "timestamp": now.isoformat(),
            "apiName": "opr-api",
            "apiVersion": "v1",
            "components": {"db": {"status": "up"}},
        }
