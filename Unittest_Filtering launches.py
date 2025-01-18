import unittest
from unittest.mock import patch
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class TestLaunchTracking(unittest.TestCase):
    def setUp(self):
        # Mocked instance attributes
        self.launches = [
            {
                "name": "FalconSat",
                "date_utc": "2006-03-24T22:30:00Z",
                "rocket": "rocket_1",
                "success": False,
                "launchpad": "launchpad_1"
            },
            {
                "name": "DemoSat",
                "date_utc": "2007-03-21T01:10:00Z",
                "rocket": "rocket_2",
                "success": True,
                "launchpad": "launchpad_2"
            }
        ]
        self.rocket_id_and_name = {
            "rocket_1": "Falcon 1",
            "rocket_2": "Falcon 9"
        }
        self.launchpads_id_and_name = {
            "launchpad_1": "Kwajalein Atoll",
            "launchpad_2": "Cape Canaveral"
        }

    def launch_tracking(self, date_range: Optional[Tuple[Optional[datetime], Optional[datetime]]] = (None, None),
                        rocket_name: Optional[str] = None,
                        success: Optional[bool] = None,
                        launch_site: Optional[str] = None) -> List[Dict]:
        """Display a list of launches with optional filtering."""
        filtered_launches: List[Dict] = []
        for launch in self.launches:
            # Filter by date range
            launch_date = datetime.fromisoformat(launch['date_utc'].replace("Z", ""))
            if date_range:
                start, end = date_range
                if start and launch_date < start:
                    continue
                if end and launch_date > end:
                    continue

            rocket_id = launch['rocket']  # Filter by rocket name
            rocket_name_in_rockets = self.rocket_id_and_name[rocket_id]
            if rocket_name and rocket_name_in_rockets != rocket_name:
                continue

            success_value = launch['success']  # Filter by success/failure
            if success is not None and success_value != success:
                continue

            launch_pad_id = launch['launchpad']  # Filter by launch site
            launch_pad_name = self.launchpads_id_and_name[launch_pad_id]
            if launch_site and launch_pad_name != launch_site:
                continue

            filtered_launches.append({"name": launch['name'], "date": launch_date, "rocket": rocket_name_in_rockets,
                                      "success": success_value, "launchpad": launch_pad_name})
        return filtered_launches

    def test_filter_by_date_range(self):
        # Test filtering by date range
        start_date = datetime(2007, 1, 1)
        end_date = datetime(2008, 1, 1)
        result = self.launch_tracking(date_range=(start_date, end_date))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "DemoSat")

    def test_filter_by_rocket_name(self):
        # Test filtering by rocket name
        result = self.launch_tracking(rocket_name="Falcon 1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "FalconSat")

    def test_filter_by_success(self):
        # Test filtering by success status
        result = self.launch_tracking(success=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "DemoSat")

        result = self.launch_tracking(success=False)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "FalconSat")

    def test_filter_by_launch_site(self):
        # Test filtering by launch site
        result = self.launch_tracking(launch_site="Cape Canaveral")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "DemoSat")

        result = self.launch_tracking(launch_site="Kwajalein Atoll")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "FalconSat")

    def test_combined_filters(self):
        # Test combined filters
        start_date = datetime(2007, 1, 1)
        end_date = datetime(2008, 1, 1)
        result = self.launch_tracking(date_range=(start_date, end_date), rocket_name="Falcon 9", success=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "DemoSat")

    def test_no_filters(self):
        # Test no filters applied
        result = self.launch_tracking()
        self.assertEqual(len(result), 2)  # All launches should be included


if __name__ == "__main__":
    unittest.main()