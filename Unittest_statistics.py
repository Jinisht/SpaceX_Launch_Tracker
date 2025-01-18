import unittest
from unittest.mock import patch
from datetime import datetime
import pandas as pd

class TestStatisticsGeneration(unittest.TestCase):
    def setUp(self):
        # Mock instance attributes
        self.rockets = [
            {"name": "Falcon 1", "success_rate_pct": 40},
            {"name": "Falcon 9", "success_rate_pct": 98},
        ]
        self.launchpads = [
            {"name": "Kwajalein Atoll", "launch_attempts": 5},
            {"name": "Cape Canaveral", "launch_attempts": 110},
        ]
        self.launches = [
            {"date_utc": "2006-03-24T22:30:00Z"},
            {"date_utc": "2007-03-21T01:10:00Z"},
            {"date_utc": "2010-06-04T18:45:00Z"},
            {"date_utc": "2010-12-08T15:43:00Z"},
            {"date_utc": "2022-12-11T17:38:00Z"},
        ]

    @patch("builtins.print")
    def test_statistics_generation(self, mock_print):
        # The function under test
        def statistics_generation():
            success_rate_by_rocket = {}
            for rocket in self.rockets:
                rocket_name = rocket["name"]
                success_rate = rocket["success_rate_pct"]
                success_rate_by_rocket[rocket_name] = success_rate
                print(f" Rocket = {rocket_name} | Success rate = {success_rate}")

            total_number_of_launches = {}
            for launchpad in self.launchpads:
                launch_site_name = launchpad["name"]
                total_launches = launchpad["launch_attempts"]
                total_number_of_launches[launch_site_name] = total_launches
                print(f" Launch site = {launch_site_name} | Total number of launches = {total_launches}")

            launch_date = []
            for launch in self.launches:
                date = datetime.fromisoformat(launch['date_utc'].replace("Z", ""))
                launch_date.append({'date_utc': date})

            df = pd.DataFrame(launch_date)
            df['year'] = df['date_utc'].dt.year
            df['month'] = df['date_utc'].dt.month
            launches_per_year = df['year'].value_counts().sort_index().reset_index()
            launches_per_month = df.groupby(['year', 'month']).size().reset_index(name='count')
            print("Launches per year:")
            print(launches_per_year)

            print("\nLaunches per month:")
            print(launches_per_month)

        # Execute the function
        statistics_generation()

        # Assertions for rocket success rates
        mock_print.assert_any_call(" Rocket = Falcon 1 | Success rate = 40")
        mock_print.assert_any_call(" Rocket = Falcon 9 | Success rate = 98")

        # Assertions for launch site total launches
        mock_print.assert_any_call(" Launch site = Kwajalein Atoll | Total number of launches = 5")
        mock_print.assert_any_call(" Launch site = Cape Canaveral | Total number of launches = 110")

        # Assertions for launches per year
        expected_launches_per_year = pd.DataFrame({
            "index": [2006, 2007, 2010, 2022],
            "year": [1, 1, 2, 1],
        })
        expected_launches_per_month = pd.DataFrame({
            "year": [2006, 2007, 2010, 2010, 2022],
            "month": [3, 3, 6, 12, 12],
            "count": [1, 1, 1, 1, 1],
        })

        # Assert the print outputs contain the expected DataFrames
        launches_per_year_str = str(expected_launches_per_year)
        launches_per_month_str = str(expected_launches_per_month)
        self.assertIn(launches_per_year_str, str(mock_print.call_args_list))
        self.assertIn(launches_per_month_str, str(mock_print.call_args_list))


if __name__ == "__main__":
    unittest.main()