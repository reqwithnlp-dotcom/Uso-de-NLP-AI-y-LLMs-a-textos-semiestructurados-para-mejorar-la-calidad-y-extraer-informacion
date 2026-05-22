import unittest
from fastapi.testclient import TestClient
from ejemplo_api import app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app) # <-- instanciar el cliente de la api

    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"mensaje": "Hola mundo"})

    def test_suma(self):
        response = self.client.get("/suma?a=2&b=3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["resultado"], 5)

    def test_error(self):
        response = self.client.get("/suma?a=2&b=hola")
        self.assertEqual(response.status_code, 422)

