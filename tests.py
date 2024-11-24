import json
import unittest

from app import app


class TestSentimentAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})

    def test_sentiment_prediction(self):
        data = {"text": "I love this product!"}
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("sentiment", response.json)
        self.assertIn("score", response.json)


if __name__ == "__main__":
    unittest.main()
