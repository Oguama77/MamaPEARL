#!/usr/bin/env python3
"""
Comprehensive endpoint testing script for Medical AI Assistant
Tests all available endpoints with various scenarios
"""

import requests
import json
import sys
import time
from typing import Dict, List
import os


class EndpointTester:

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {}

    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def wait_for_server(self, timeout: int = 30):
        """Wait for the server to be ready"""
        self.log("Waiting for server to be ready...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{self.base_url}/docs", timeout=5)
                if response.status_code == 200:
                    self.log("Server is ready!")
                    return True
            except requests.exceptions.RequestException:
                time.sleep(1)

        self.log("Server failed to start within timeout", "ERROR")
        return False

    def test_endpoint(self,
                      method: str,
                      endpoint: str,
                      data=None,
                      files=None,
                      description: str = ""):
        """Test a single endpoint"""
        url = f"{self.base_url}{endpoint}"
        self.log(f"Testing {method} {endpoint} - {description}")

        try:
            if method.upper() == "GET":
                response = requests.get(url, timeout=30)
            elif method.upper() == "POST":
                if files:
                    response = requests.post(url, files=files, timeout=30)
                elif data:
                    response = requests.post(url, json=data, timeout=30)
                else:
                    response = requests.post(url, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            result = {
                "status_code": response.status_code,
                "success": 200 <= response.status_code < 300,
                "response_time": response.elapsed.total_seconds(),
                "content_type": response.headers.get("content-type", ""),
            }

            try:
                result["response"] = response.json()
            except json.JSONDecodeError:
                result[
                    "response"] = response.text[:
                                                500]  # First 500 chars if not JSON

            if result["success"]:
                self.log(
                    f"SUCCESS - {endpoint} ({result['status_code']}) - {result['response_time']:.2f}s"
                )
            else:
                self.log(
                    f"FAILED - {endpoint} ({result['status_code']}) - {result['response_time']:.2f}s",
                    "ERROR")

        except requests.exceptions.RequestException as e:
            result = {
                "status_code": None,
                "success": False,
                "error": str(e),
                "response_time": None,
            }
            self.log(f"ERROR - {endpoint} - {str(e)}", "ERROR")

        return result

    def test_chat_endpoints(self):
        """Test chat-related endpoints"""
        self.log("=== Testing Chat Endpoints ===")

        # Test general chat
        test_cases = [{
            "data": {
                "message": "What is diabetes?"
            },
            "description": "General health question"
        }, {
            "data": {
                "message": "Tell me about preeclampsia risk"
            },
            "description": "Preeclampsia-related question"
        }, {
            "data": {
                "message": "What are the symptoms of high blood pressure?"
            },
            "description": "Specific medical question"
        }, {
            "data": {
                "message": ""
            },
            "description": "Empty message"
        }]

        results = []
        for test_case in test_cases:
            result = self.test_endpoint("POST",
                                        "/chat",
                                        data=test_case["data"],
                                        description=test_case["description"])
            results.append(result)

        self.results["chat"] = results

    def test_prediction_endpoints(self):
        """Test prediction-related endpoints"""
        self.log("=== Testing Prediction Endpoints ===")

        # Sample variables for testing (30 float values as expected by the model)
        sample_variables = [
            75.0, 165.0, 27.5, 1.0, 0.0, 120.0, 80.0, 98.0, 36.8, 72.0, 14.2,
            4.5, 142.0, 4.2, 98.0, 24.0, 1.2, 45.0, 3.5, 1.8, 150.0, 8.5, 35.0,
            0.9, 7.4, 2.1, 0.8, 12.0, 180.0, 95.0
        ]

        test_cases = [
            {
                "data": {
                    "variables": sample_variables
                },
                "description": "Valid prediction with sample data"
            },
            {
                "data": {
                    "variables": sample_variables[:10]
                },  # Too few variables
                "description": "Insufficient variables"
            },
            {
                "data": {
                    "variables": []
                },
                "description": "Empty variables list"
            },
            {
                "data": {
                    "variables": ["invalid", "data"]
                },
                "description": "Invalid data types"
            }
        ]

        results = []
        for test_case in test_cases:
            result = self.test_endpoint("POST",
                                        "/predict",
                                        data=test_case["data"],
                                        description=test_case["description"])
            results.append(result)

        self.results["prediction"] = results

    def test_variable_endpoints(self):
        """Test variable normalization endpoints"""
        self.log("=== Testing Variable Endpoints ===")

        test_cases = [
            {
                "data":
                "75, 165, 27.5, 1, 0, 120, 80, 98, 36.8, 72, 14.2, 4.5, 142, 4.2, 98, 24, 1.2, 45, 3.5, 1.8, 150, 8.5, 35, 0.9, 7.4, 2.1, 0.8, 12, 180, 95",
                "description": "Valid comma-separated variables"
            },
            {
                "data": "invalid input format",
                "description": "Invalid format"
            },
            {
                "data": "",
                "description": "Empty input"
            },
            {
                "data": "1,2,3",  # Too few values
                "description": "Insufficient variables"
            }
        ]

        results = []
        for test_case in test_cases:
            # The endpoint expects the data to be sent with a specific format
            payload = {"user_input": test_case["data"]}
            result = self.test_endpoint("POST",
                                        "/normalize_variables",
                                        data=payload,
                                        description=test_case["description"])
            results.append(result)

        self.results["variables"] = results

    def test_image_endpoints(self):
        """Test image extraction endpoints"""
        self.log("=== Testing Image Endpoints ===")

        # Create a dummy image file for testing
        dummy_image_content = b"dummy image content for testing"

        test_cases = [{
            "files": {
                "files": ("test_image.png", dummy_image_content, "image/png")
            },
            "description": "Upload dummy image file"
        }, {
            "files": {
                "files": ("test_document.txt", b"not an image", "text/plain")
            },
            "description": "Upload non-image file"
        }]

        results = []
        for test_case in test_cases:
            result = self.test_endpoint("POST",
                                        "/extract",
                                        files=test_case["files"],
                                        description=test_case["description"])
            results.append(result)

        # Test with no file
        result = self.test_endpoint("POST",
                                    "/extract",
                                    description="No file uploaded")
        results.append(result)

        self.results["image"] = results

    def test_docs_endpoint(self):
        """Test FastAPI automatic documentation"""
        self.log("=== Testing Documentation Endpoints ===")

        endpoints = [("/docs", "Swagger UI documentation"),
                     ("/redoc", "ReDoc documentation"),
                     ("/openapi.json", "OpenAPI schema")]

        results = []
        for endpoint, description in endpoints:
            result = self.test_endpoint("GET",
                                        endpoint,
                                        description=description)
            results.append(result)

        self.results["docs"] = results

    def run_all_tests(self):
        """Run all endpoint tests"""
        self.log("Starting comprehensive endpoint testing...")

        if not self.wait_for_server():
            self.log("Cannot proceed with tests - server not ready", "ERROR")
            return False

        # Run all test suites
        self.test_docs_endpoint()
        self.test_chat_endpoints()
        self.test_prediction_endpoints()
        self.test_variable_endpoints()
        self.test_image_endpoints()

        return True

    def generate_report(self):
        """Generate a comprehensive test report"""
        self.log("=== TEST REPORT ===")

        total_tests = 0
        passed_tests = 0
        failed_tests = 0

        for category, tests in self.results.items():
            self.log(f"\n{category.upper()} ENDPOINTS:")
            category_passed = 0
            category_total = len(tests)

            for i, test in enumerate(tests, 1):
                status = "PASS" if test.get("success", False) else "FAIL"
                response_time = f" ({test['response_time']:.2f}s)" if test.get(
                    "response_time") else ""
                status_code = f" [{test['status_code']}]" if test.get(
                    "status_code") else ""

                self.log(f"  {i}. {status}{status_code}{response_time}")

                if test.get("success", False):
                    category_passed += 1
                    passed_tests += 1
                else:
                    failed_tests += 1
                    if "error" in test:
                        self.log(f"     Error: {test['error']}")
                    elif "response" in test and isinstance(
                            test["response"],
                            dict) and "error" in test["response"]:
                        self.log(
                            f"     API Error: {test['response']['error']}")

                total_tests += 1

            self.log(
                f"  Category Summary: {category_passed}/{category_total} passed"
            )

        self.log(f"\n=== OVERALL SUMMARY ===")
        self.log(f"Total Tests: {total_tests}")
        self.log(f"Passed: {passed_tests}")
        self.log(f"Failed: {failed_tests}")
        self.log(f"Success Rate: {(passed_tests/total_tests*100):.1f}%"
                 if total_tests > 0 else "N/A")

        return {
            "total":
            total_tests,
            "passed":
            passed_tests,
            "failed":
            failed_tests,
            "success_rate":
            (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "details":
            self.results
        }


def main():
    """Main function to run the endpoint tests"""
    base_url = "http://localhost:8000"

    # Check if custom URL is provided
    if len(sys.argv) > 1:
        base_url = sys.argv[1]

    print(f"Testing endpoints at: {base_url}")
    print("=" * 50)

    tester = EndpointTester(base_url)

    if tester.run_all_tests():
        report = tester.generate_report()

        # Save detailed report to file
        with open("endpoint_test_report.json", "w") as f:
            json.dump(report, f, indent=2)

        tester.log("Detailed report saved to endpoint_test_report.json")

        # Exit with appropriate code
        sys.exit(0 if report["failed"] == 0 else 1)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
