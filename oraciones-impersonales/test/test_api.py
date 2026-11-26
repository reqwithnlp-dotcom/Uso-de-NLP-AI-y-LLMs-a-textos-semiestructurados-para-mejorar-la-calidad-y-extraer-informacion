

from unittest.mock import patch

from fastapi.testclient import TestClient

from service.api import app

client = TestClient(app)

FAKE_RESULTS = [
    {
        "sentence": "It rains.", "personal": False, "impersonal": True,
        "ambiguous": False, "type": "WEATHER_IT", "personal_type": None,
        "final_label": "IMPERSONAL", "decided_by": "layer1", "layer2_scores": None,
    },
    {
        "sentence": "I bought a car.", "personal": True, "impersonal": False,
        "ambiguous": False, "type": "PERSONAL", "personal_type": "PRONOUN_SUBJECT",
        "final_label": "PERSONAL", "decided_by": "layer1", "layer2_scores": None,
    },
    {
        "sentence": "It is fast.", "personal": False, "impersonal": False,
        "ambiguous": True, "type": "PERSONAL", "personal_type": None,
        "final_label": "PERSONAL", "decided_by": "layer2",
        "layer2_scores": {"PERSONAL": 0.91, "IMPERSONAL": 0.07},
    },
]


class TestHealth:
    def test_health_ok(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok"
        assert isinstance(body["layer2_loaded"], bool)


class TestAnalyzeContract:
    @patch("service.api.analyze_text", return_value=FAKE_RESULTS)
    def test_respuesta_correcta(self, mock_analyze):
        resp = client.post(
            "/analyze",
            json={"text": "It rains. I bought a car. It is fast."},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] == 3
        assert body["impersonal_count"] == 1
        assert body["personal_count"] == 1
        assert body["ambiguous_count"] == 1
        assert body["results"][0]["type"] == "WEATHER_IT"
        assert body["results"][1]["personal"] is True
        assert body["results"][1]["personal_type"] == "PRONOUN_SUBJECT"
        assert body["results"][2]["ambiguous"] is True
        assert body["results"][2]["decided_by"] == "layer2"
        assert body["results"][2]["layer2_scores"]["PERSONAL"] == 0.91
        assert body["results"][0]["layer2_scores"] is None
        assert body["layer2_resolved_count"] == 1
        assert body["undecided_count"] == 0
        mock_analyze.assert_called_once_with("It rains. I bought a car. It is fast.")

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
        assert resp.json() == {
            "results": [],
            "total": 0,
            "impersonal_count": 0,
            "personal_count": 0,
            "ambiguous_count": 0,
            "layer2_resolved_count": 0,
            "undecided_count": 0,
        }


class TestCapa2Contrato:
    @patch("service.api.analyze_text", return_value=[{
        **FAKE_RESULTS[2], "final_label": "UNDECIDED", "decided_by": "none",
        "layer2_scores": None,
    }])
    def test_sin_modelo_capa2_queda_undecided(self, _mock):
        body = client.post("/analyze", json={"text": "It is fast."}).json()
        assert body["results"][0]["final_label"] == "UNDECIDED"
        assert body["undecided_count"] == 1
        assert body["layer2_resolved_count"] == 0

    @patch("service.api.analyze_text", return_value=[{
        **FAKE_RESULTS[0], "final_label": "MAYBE",
    }])
    def test_final_label_invalido_falla(self, _mock):
        # El contrato solo admite PERSONAL / IMPERSONAL / UNDECIDED
        import pytest
        with pytest.raises(Exception):
            client.post("/analyze", json={"text": "It rains."})
