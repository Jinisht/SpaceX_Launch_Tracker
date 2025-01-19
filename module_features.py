from datetime import datetime
import pandas as pd
from typing import Optional, Tuple, List, Dict
from pandas import DataFrame


class Spacex_features:
    launches_per_year: DataFrame
    launches_per_month: DataFrame

    def __init__(self, client):
        self.client = client
        self.launches: List[Dict] = self.client.fetch_launches()
        self.rockets: List[Dict] = self.client.fetch_rockets()
        self.launchpads: List[Dict] = self.client.fetch_launchpads()
        self.rocket_id_and_name: Dict[str, str] = {r['id']: r['name'] for r in self.rockets}
        self.launchpads_id_and_name: Dict[str, str] = {lp['id']: lp['name'] for lp in self.launchpads}
        self.filtered_launches: List[Dict] = []
        self.launch_key_details: List[Dict] = []
        self.success_rate_by_rocket: Dict = {}
        self.total_number_of_launches: Dict = {}
        self.launch_date: List = []

    def display_launch_key_details(self):
        """ Display a list of launches and its key details."""

        for launch in self.launches:
            launch_name: str = launch["name"]
            rocket_id: str = launch["rocket"]
            launchpad_id: str = launch["launchpad"]
            success: bool = launch['success']
            rocket_name:str = self.rocket_id_and_name[rocket_id]
            launchpad_name: str = self.launchpads_id_and_name[launchpad_id]
            self.launch_key_details.append({"name": launch_name, "rocket": rocket_name, "launch site": launchpad_name,
                                            "success": success})
        print("Launch key Details")
        for data in self.launch_key_details:
            print(f'Launch name :{data["name"]} | Rocket name: {data["rocket"]} '
                  f'| Launch site: {data["launch site"]} | Success: {data["success"]}')

    def launch_tracking(self, date_range: Optional[Tuple[Optional[datetime], Optional[datetime]]] = (None, None),
                        rocket_name: Optional[str] = None, success: Optional[bool] = None,
                        launch_site: Optional[str] = None) -> list[dict]:
        """ Display a list of launches with given filtering.  """

        start, end = date_range if date_range else (None, None)
        for launch in self.launches:
            if launch["date_utc"]:
                launch_date = datetime.fromisoformat(launch['date_utc'].replace("Z", ""))
            else:
                launch_date = None
            if start and end and launch_date and not (start <= launch_date <= end):
                continue

            rocket_id: str = launch['rocket']  # Filter by rocket name
            rocket_name_in_rockets: str = self.rocket_id_and_name[rocket_id]
            if rocket_name and rocket_name_in_rockets != rocket_name:
                continue

            success_value: bool = launch['success']  # Filter by success/failure
            if success is not None and success_value != success:
                continue

            launch_pad_id: str = launch['launchpad']  # Filter by launch site
            launch_pad_name: str = self.launchpads_id_and_name[launch_pad_id]
            if launch_site and launch_pad_name != launch_site:
                continue

            self.filtered_launches.append(
                {"name": launch['name'], "date": launch_date, "rocket": rocket_name_in_rockets,
                 "success": success_value, "launchpad": launch_pad_name})

        for data in self.filtered_launches:
            if data["success"]:
                success_status = "Success"
            else:
                success_status = "Failure"
            print(f"Date={data['date']} | Rocket= {data['rocket']} | Status = {success_status}  "
                  f"| Launch site = {data['launchpad']}")
        return self.filtered_launches

    def statistics_generation(self) -> None:
        """ Display the statistics such as success rates, total number of launches per site and
            launch frequency"""
        for rocket in self.rockets:
            rocket_name: str = rocket["name"]
            success_rate: float = rocket["success_rate_pct"]
            self.success_rate_by_rocket[rocket_name]: Dict[str, float] = success_rate
            print(f" Rocket = {rocket_name} | Success rate = {success_rate}")

        for launchpad in self.launchpads:
            launch_site_name: str = launchpad["name"]
            total_launches: float = launchpad["launch_attempts"]
            self.total_number_of_launches[launch_site_name]: Dict[str, float] = total_launches
            print(f" Launch site = {launch_site_name} | Total number of launches = {total_launches}")

        self.launch_date: List = []
        for launch in self.launches:
            date = datetime.fromisoformat(launch['date_utc'].replace("Z", ""))
            self.launch_date.append({'date_utc': date})

        df = pd.DataFrame(self.launch_date)
        df['year'] = df['date_utc'].dt.year
        df['month'] = df['date_utc'].dt.month
        self.launches_per_year = df['year'].value_counts().sort_index().reset_index()
        self.launches_per_month = df.groupby(['year', 'month']).size().reset_index(name='count')
        print(f"\nLaunches per year:\n{self.launches_per_year}\n\nLaunches per month:\n{self.launches_per_month}")

    def export_data(self):
        output_file = 'SpaceX_Launch_Data.xlsx'
        launch_key_data = pd.DataFrame(self.launch_key_details)
        launch_tracking_data = pd.DataFrame(self.filtered_launches)
        launch_success_rate = pd.DataFrame(list(self.success_rate_by_rocket.items()),
                                           columns = ["Rocket", "Success Rate (%)"])
        total_launches = pd.DataFrame(list(self.total_number_of_launches.items()),
                                      columns = ["Launch site","Total number of launches"])

        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            launch_key_data.to_excel(writer, sheet_name='Launches_key_details', index=False)
            launch_tracking_data.to_excel(writer, sheet_name='Launches_tracking', index=False)
            launch_success_rate.to_excel(writer, sheet_name='Success_rate', index=False)
            total_launches.to_excel(writer, sheet_name='Total_launches', index=False)
            self.launches_per_year.to_excel(writer, sheet_name='Launches_per_year', index=False)
            self.launches_per_month.to_excel(writer, sheet_name='Launches_per_month', index=False)

        print(f"Data exported to {output_file}.")
