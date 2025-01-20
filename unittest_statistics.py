import unittest
from datetime import datetime
from unittest.mock import MagicMock
from module_features import Spacex_features



class TestStatisticsGeneration(unittest.TestCase):
    def setUp(self) -> None:
        """Set up test data for the statistics"""
        mock_client = MagicMock()
        self.features = Spacex_features(client=mock_client)
        """ Mock data for rockets, launchpads, and launches"""
        self.features.rockets = [{"name": "Falcon 9", "success_rate_pct": 98}, {"name": "Falcon Heavy",
                                 "success_rate_pct": 95.0}]
        self.features.launchpads = [{"name": "VAFB SLC 3W", "launch_attempts": 0}, {"name": "CCSFS SLC 40",
                                    "launch_attempts": 99}]
        self.features.launches = [
            {"date_utc": "2023-07-10T22:00:00.000Z"}, {"date_utc": "2022-05-15T12:30:00.000Z"},
            {"date_utc": "2023-11-20T01:01:00.000Z"}, {"date_utc": "2022-03-05T08:00:00.000Z"}]

    def test_statistics_generation(self) -> None:
        """ Test success rate, number of launches and launch_date"""
        self.features.statistics_generation()
        expected_success_rate_by_rocket: dict = {"Falcon 9": 98, "Falcon Heavy": 95.0}
        self.assertEqual(self.features.success_rate_by_rocket, expected_success_rate_by_rocket)

        expected_total_number_of_launches: dict = {"VAFB SLC 3W": 0, "CCSFS SLC 40": 99}
        self.assertEqual(self.features.total_number_of_launches, expected_total_number_of_launches)

        expected_dates: list[dict] = [
            {'date_utc': datetime(2023, 7, 10, 22, 0)},
            {'date_utc': datetime(2022, 5, 15, 12, 30)},
            {'date_utc': datetime(2023, 11, 20, 1, 1)},
            {'date_utc': datetime(2022, 3, 5, 8, 0)}]
        self.assertEqual(self.features.launch_date, expected_dates)

