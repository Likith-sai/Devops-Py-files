import pytest
from unittest import TestCase
from src.metrics import calculate_metrics

class TestCalculateMetrics(TestCase):
    def test_200_requests(self):
        request_results =[
            {"status_code": 200, "response_time": 0.1},
            {"status_code": 201, "response_time": 0.2},
            {"status_code": 299, "response_time": 0.3},
        ]
        results = calculate_metrics(request_results)
        expected = {
        "total_requests": 3,
        "successful_requests": 3,
        "error_requests": 0,
        "max_latency": 0.3,
        "avg_latency": 0.2,
        "error_rate": 0
        }
        self.assertEqual(results["total_requests"], expected["total_requests"])
        self.assertEqual(results["successful_requests"], expected["successful_requests"])
        self.assertEqual(results["error_requests"], expected["error_requests"])
        self.assertEqual(results["max_latency"], expected["max_latency"])
        self.assertEqual(results["avg_latency"], pytest.approx(0.2, abs=0.001))
        self.assertEqual(results["error_rate"], expected["error_rate"])

    def test_mixed_requests(self):
        request_results =[
            {"status_code": 200, "response_time": 0.1},
            {"status_code": 404, "response_time": 0.2},
            {"status_code": 500, "response_time": 0.3},
            {"status_code": 401, "response_time": 0.4},
            {"status_code": 201, "response_time": 0.3},
        ]
        results = calculate_metrics(request_results)
        expected = {
        "total_requests": 5,
        "successful_requests": 2,
        "error_requests": 3,
        "max_latency": 0.4,
        "avg_latency": 0.26,
        "error_rate": 0.6
        }
        self.assertEqual(results["total_requests"], expected["total_requests"])
        self.assertEqual(results["successful_requests"], expected["successful_requests"])
        self.assertEqual(results["error_requests"], expected["error_requests"])
        self.assertEqual(results["max_latency"], expected["max_latency"])
        self.assertEqual(results["avg_latency"], pytest.approx(expected["avg_latency"], abs=0.001))
        self.assertEqual(results["error_rate"], pytest.approx(expected["error_rate"], abs=0.001))

    def test_missing_status_code(self):
        request_results = [
            {"status_code": None, "response_time": 0.1},
            {"status_code": 200, "response_time": 0.2},
            {"status_code": 404, "response_time": 0.3},
            {"response_time": 0.4}
        ]
        results = calculate_metrics(request_results)
        expected = {
        "total_requests": 4,
        "successful_requests": 1,
        "error_requests": 3,
        "max_latency": 0.4,
        "avg_latency": 0.25,
        "error_rate": 0.75
        }
        self.assertEqual(results["total_requests"], expected["total_requests"])
        self.assertEqual(results["successful_requests"], expected["successful_requests"])
        self.assertEqual(results["error_requests"], expected["error_requests"])
        self.assertEqual(results["max_latency"], expected["max_latency"])
        self.assertEqual(results["avg_latency"], pytest.approx(expected["avg_latency"], abs=0.001))
        self.assertEqual(results["error_rate"], pytest.approx(expected["error_rate"], abs=0.001))

    def test_latency_calculation(self):
        request_results = [
            {"status_code": 200, "response_time": 0.1},
            {"status_code": 500, "response_time": 0.2},
            {"status_code": 200, "response_time": None},
            {"status_code": 500}
        ]
        results = calculate_metrics(request_results)
        expected = {
        "total_requests": 4,
        "successful_requests": 2,
        "error_requests": 2,
        "max_latency": 0.2,
        "avg_latency": 0.15,
        "error_rate": 0.5
        }
        self.assertEqual(results["total_requests"], expected["total_requests"])
        self.assertEqual(results["successful_requests"], expected["successful_requests"])
        self.assertEqual(results["error_requests"], expected["error_requests"])
        self.assertEqual(results["max_latency"], expected["max_latency"])
        self.assertEqual(results["avg_latency"], pytest.approx(expected["avg_latency"], abs=0.001))
        self.assertEqual(results["error_rate"], pytest.approx(expected["error_rate"], abs=0.001))

    def test_no_requests(self):
        request_results = []
        results = calculate_metrics(request_results)
        expected = {
        "total_requests": 0,
        "successful_requests": 0,
        "error_requests": 0,
        "max_latency": None,
        "avg_latency": 0,
        "error_rate": 0
        }
        self.assertEqual(results["total_requests"], expected["total_requests"])
        self.assertEqual(results["successful_requests"], expected["successful_requests"])
        self.assertEqual(results["error_requests"], expected["error_requests"])
        self.assertEqual(results["max_latency"], expected["max_latency"])   
        self.assertEqual(results["avg_latency"], expected["avg_latency"])
        self.assertEqual(results["error_rate"], expected["error_rate"])