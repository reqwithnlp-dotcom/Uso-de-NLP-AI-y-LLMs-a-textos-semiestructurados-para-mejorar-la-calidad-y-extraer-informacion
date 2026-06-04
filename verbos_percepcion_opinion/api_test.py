import unittest
from fastapi.testclient import TestClient
from perception_opinion_api import app

client = TestClient(app)

class Test_percepcion_opinion(unittest.TestCase):
    def test_detect_perception_opinion_1(self):
        response = client.post("/perception-opinion", json={"text": "I think that this method is not the most suitable."})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "opinion_perception": ["think"],
                "others": ["I", "that", "this", "method", "is", "not", "the", "most", "suitable"],
            },
        )

    def test_detect_perception_opinion_2(self):
        response = client.post("/perception-opinion", json={"text": "María watched the movie and listened to the music."})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "opinion_perception": [],
                "others": ["María", "watched", "the", "movie", "and", "listened", "to", "the", "music"],
            },
        )
    
    def test_detect_perception_opinion_3(self):
        response = client.post("/perception-opinion", json={"text": "I feel pain in my back."})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "opinion_perception": ["feel"],
                "others": ["I", "pain", "in", "my", "back"],
            },
        )
    
    def test_detect_perception_opinion_empty(self):
        response = client.post("/perception-opinion", json={"text": ""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Text field is empty"},
        )

if __name__ == "__main__":
    unittest.main()