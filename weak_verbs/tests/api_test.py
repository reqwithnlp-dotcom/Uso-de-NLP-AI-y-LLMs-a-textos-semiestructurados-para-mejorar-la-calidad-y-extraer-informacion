import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestWeakVerbs(unittest.TestCase):
    def test_detect_weak_verbs_1(self):
        response = client.post(
            "/weak_verbs",
            json={"text": "She made a decision."},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            ["made"]
        )

    def test_detect_weak_verbs_2(self):
        response = client.post(
            "/weak_verbs", 
            json={"text": "He did an analysis of the data."}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            ["did"]
        )

    def test_detect_weak_verbs_3(self):
        response = client.post(
            "/weak_verbs", 
            json={"text": "They made an improvement."}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            ["made"]
        )
    
    def test_detect_weak_verbs_4(self):
        response = client.post(
            "/weak_verbs", 
            json={"text": "The company made a reduction in costs."}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            ["made"]
        )

    def test_detect_weak_verbs_empty(self):
        response = client.post(
            "/weak_verbs", 
            json={"text": ""}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Text field is empty"},
        )


if __name__ == "__main__":
    unittest.main()