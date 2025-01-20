import unittest
from datetime import datetime
from main import SpaceXAPI_client
from module_features import Spacex_features


class Test_launch_tracking(unittest.TestCase):
    def setUp(self) -> None:
        self.client = SpaceXAPI_client()
        self.features = Spacex_features(self.client)

    def test_filter_by_date_range(self) -> None:
        """Test filtering by date range."""
        start_date: datetime = datetime(2007, 1, 1)
        end_date: datetime = datetime(2008, 1, 1)
        result: list[dict] = self.features.launch_tracking(date_range=(start_date, end_date))
        self.assertEqual(result[0]['name'], "DemoSat")

    def test_filter_by_rocket_name(self) -> None:
        """ Test filtering by rocket name """
        result: list[dict] = self.features.launch_tracking(rocket_name="Falcon 1")
        self.assertEqual(result[0]['name'], "FalconSat")

    def test_filter_by_success(self) -> None:
        """ Test filtering by success status """
        result: list[dict] = self.features.launch_tracking(success=False)
        self.assertEqual(result[0]['name'], "FalconSat")

    def test_filter_by_launch_site(self) -> None:
        """ Test filtering by launch site """
        result: list[dict] = self.features.launch_tracking(launch_site="Kwajalein Atoll")
        self.assertEqual(result[0]['name'], "FalconSat")
