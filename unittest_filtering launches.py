import unittest
from datetime import datetime
from main import SpaceXAPI_client
from module_features import Spacex_features

class TestLaunchTracking(unittest.TestCase):
    def setUp(self):
        self.client = SpaceXAPI_client()
        self.features = Spacex_features(self.client)

    def test_filter_by_date_range(self):
        """Test filtering by date range."""
        start_date = datetime(2007, 1, 1)
        end_date = datetime(2008, 1, 1)
        result = self.features.launch_tracking(date_range=(start_date, end_date))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "DemoSat")

    def test_filter_by_rocket_name(self):
        """ Test filtering by rocket name """
        result = self.features.launch_tracking(rocket_name="Falcon 1")
        self.assertTrue(len(result)> 1)
        self.assertEqual(result[0]['name'], "FalconSat")

    def test_filter_by_success(self):
        """ Test filtering by success status """
        result = self.features.launch_tracking(success=False)
        self.assertTrue(len(result)> 1)
        self.assertEqual(result[0]['name'], "FalconSat")

    def test_filter_by_launch_site(self):
        """ Test filtering by launch site """
        result = self.features.launch_tracking("Kwajalein Atoll")
        self.assertTrue(len(result)> 1)
        self.assertEqual(result[0]['name'], "Falcon 1")







if __name__ == "__main__":
    unittest.main()