from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_api_detect_shift():
    payload = {"texto": "John wondered where Mary was. Mary knew he was waiting."}

    response = client.post("/detect", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["from_character"]["canonical_name"] == "John"
    assert body[0]["to_character"]["canonical_name"] == "Mary"


def test_api_rejects_missing_texto():
    response = client.post("/detect", json={})

    assert response.status_code == 422
