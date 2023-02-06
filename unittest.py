import unittest
import requests
import json

class TestModelTrainingAPI(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:5000/train"

    def test_train_model(self):
        data = {
            "model_type": "regression",
            "hyperparameters": {
                "param1": "value1",
                "param2": "value2"
            }
        }
        response = requests.post(self.url, json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], "Model training started")

    def test_get_model_types(self):
        response = requests.get("http://localhost:5000/model_types")
        self.assertEqual(response.status_code, 200)
        model_types = response.json()['model_types']
        self.assertIn("regression", model_types)
        self.assertIn("classification", model_types)
        self.assertIn("RandomForest", model_types)

class TestModelPredictionAPI(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:5000/predict"

    def test_make_prediction(self):
        data = {
            "model_id": 1,
            "input_data": [1, 2, 3]
        }
        response = requests.post(self.url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("prediction", response.json())

if __name__ == '__main__':
    unittest.main()