import pytest
from app.config.version import VERSION
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_version_endpoint(client):
    response = client.get("/version")

    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert data["version"] == VERSION
