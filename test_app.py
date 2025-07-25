# test_app.py
import unittest
import app # Import your Flask app

class TestApp(unittest.TestCase):
    """
    Unit tests for the Flask application.
    """

    def setUp(self):
        """
        Set up the test client before each test.
        This allows us to simulate requests to the Flask app.
        """
        self.app = app.app.test_client()
        self.app.testing = True # Enable testing mode

    def test_hello_world(self):
        """
        Test the root endpoint to ensure it returns the expected greeting.
        """
        response = self.app.get('/')
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the response data matches the expected string
        self.assertEqual(response.data.decode('utf-8'), "Hello from Python App!")

    def test_health_check(self):
        """
        Test the health check endpoint.
        """
        response = self.app.get('/health')
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check if the JSON response contains the expected status
        self.assertEqual(response.json, {"status": "OK"})

if __name__ == '__main__':
    # Run all tests when the script is executed directly.
    unittest.main()
