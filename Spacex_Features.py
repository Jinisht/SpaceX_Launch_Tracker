from datetime import datetime
import pandas as pd
from typing import Optional, Tuple, List, Dict


class Spacex_features:

    def __init__(self, client):
        self.client = client
        self.launches = self.client.fetch_launches()
        self.rockets = self.client.fetch_rockets()
        self.launchpads = self.client.fetch_launchpads()
        self.rocket_id_and_name = {r['id']: r['name'] for r in self.rockets}
        self.launchpads_id_and_name = {lp['id']: lp['name'] for lp in self.launchpads}

    def display_launch_key_details(self):
        """ Display a list of launches and its key details."""
        launch_key_details= []
        for launch in self.launches:
            launch_name = launch["name"]
            rocket_id = launch["rocket"]
            launchpad_id = launch["launchpad"]
            success = launch['success']
            rocket_name = self.rocket_id_and_name[rocket_id]
            launchpad_name = self.launchpads_id_and_name[launchpad_id]
            launch_key_details.append({"name": launch_name, "rocket": rocket_name, "launch site": launchpad_name,
                                       "success": success })
        print("Launch key Details")
        for data in launch_key_details:
            print(f'Launch name :{data["name"]} | Rocket name: {data["rocket"]} '
                  f'| Launch site: {data["launch site"]} | Success: {data["success"]}')

    def launch_tracking(self, date_range: Optional[Tuple[Optional[datetime], Optional[datetime]]] = (None, None),
                        rocket_name: Optional[str] = None, success: Optional[bool] = None,
                        launch_site: Optional[str] = None ) -> list[dict]:
        """ Display a list of launches with given filtering.
        :rtype: object
        """
        filtered_launches: List[Dict] = []
        start, end = date_range if date_range else (None, None)
        for launch in self.launches:
            if launch["date_utc"]:
                launch_date = datetime.fromisoformat(launch['date_utc'].replace("Z", ""))
            else:
                launch_date = None
            if start and end and launch_date and not (start <= launch_date <= end):
                continue


            rocket_id = launch['rocket']  # Filter by rocket name
            rocket_name_in_rockets = self.rocket_id_and_name[rocket_id]
            if rocket_name and  rocket_name_in_rockets != rocket_name:
                continue

            success_value =launch['success'] # Filter by success/failure
            if success is not None and success_value != success:
                continue

            launch_pad_id = launch['launchpad']  # Filter by launch site
            launch_pad_name = self.launchpads_id_and_name[launch_pad_id]
            if launch_site and launch_pad_name != launch_site:
                continue

            filtered_launches.append({"name": launch['name'], "date": launch_date, "rocket": rocket_name_in_rockets,
                                      "success": success_value, "launchpad": launch_pad_name })

        for data in filtered_launches:
            if data["success"]:
                success_status = "Success"
            else:
                success_status = "Failure"
            print(f"Date={data['date']} | Rocket= {data['rocket']} | Status = {success_status}  "
                  f"| Launch site = {data['launchpad']}")
        return filtered_launches

    def statistics_generation(self) -> None:
        """ Display the statistics such as success rates, total number of launches per site and
            launch frequency"""
        success_rate_by_rocket: Dict = {}
        for rocket in self.rockets:
            rocket_name = rocket["name"]
            success_rate = rocket["success_rate_pct"]
            success_rate_by_rocket[rocket_name] = success_rate
            print(f" Rocket = {rocket_name} | Success rate = {success_rate}")

        total_number_of_launches: Dict= {}
        for launchpad in self.launchpads:
            launch_site_name = launchpad["name"]
            total_launches = launchpad["launch_attempts"]
            total_number_of_launches[launch_site_name] = total_launches
            print(f" Launch site = {launch_site_name} | Total number of launches = {total_launches}")

        launch_date: List = []
        for launch in self.launches:
            date = datetime.fromisoformat(launch['date_utc'].replace("Z", ""))
            launch_date.append({'date_utc': date})

        df = pd.DataFrame(launch_date)
        df['year'] = df['date_utc'].dt.year
        df['month'] = df['date_utc'].dt.month
        launches_per_year = df['year'].value_counts().sort_index().reset_index()
        launches_per_month = df.groupby(['year', 'month']).size().reset_index(name='count')
        print(f"\nLaunches per year:\n{launches_per_year}\n\nLaunches per month:\n{launches_per_month}")
