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
    
    def test_detect_weak_verbs_with_phrasal_verb(self):
        response = client.post(
            "/weak_verbs", 
            json={"text": "We need to get up early tomorrow."}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            []
        )
    
    def test_detect_weak_verbs_with_complex_phrasal_verb(self):
        response = client.post(
            "/weak_verbs", 
            json={"text": "The teacher gave the difficult exam out to the students. Then, she made a cup of coffee."}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            ["made"]
        )


if __name__ == "__main__":
    unittest.main()