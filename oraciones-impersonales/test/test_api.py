

from unittest.mock import patch

from fastapi.testclient import TestClient

from service.api import app

client = TestClient(app)

FAKE_RESULTS = [
    {"sentence": "It rains.", "impersonal": True, "type": "WEATHER_IT"},
    {"sentence": "I bought a car.", "impersonal": False, "type": "PERSONAL"},
]


class TestHealth:
    def test_health_ok(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


class TestAnalyzeContract:
    @patch("service.api.analyze_text", return_value=FAKE_RESULTS)
    def test_respuesta_correcta(self, mock_analyze):
        resp = client.post("/analyze", json={"text": "It rains. I bought a car."})
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] == 2
        assert body["impersonal_count"] == 1
        assert body["results"][0]["type"] == "WEATHER_IT"
        assert body["results"][1]["impersonal"] is False
        mock_analyze.assert_called_once_with("It rains. I bought a car.")

    def test_body_sin_text_da_422(self):
        resp = client.post("/analyze", json={})
        assert resp.status_code == 422

    def test_text_vacio_da_422(self):
        # min_length=1 en el schema rechaza el string vacío
        resp = client.post("/analyze", json={"text": ""})
        assert resp.status_code == 422

    def test_tipo_invalido_da_422(self):
        resp = client.post("/analyze", json={"text": 123})
        assert resp.status_code == 422

    @patch("service.api.analyze_text", side_effect=RuntimeError("modelo no instalado"))
    def test_modelo_ausente_da_503(self, _mock):
        resp = client.post("/analyze", json={"text": "It rains."})
        assert resp.status_code == 503
        assert "modelo" in resp.json()["detail"].lower()

    @patch("service.api.analyze_text", return_value=[])
    def test_sin_oraciones_devuelve_lista_vacia(self, _mock):
        resp = client.post("/analyze", json={"text": "..."})
        assert resp.status_code == 200
        assert resp.json() == {"results": [], "total": 0, "impersonal_count": 0}
