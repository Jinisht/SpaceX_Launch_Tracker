import os
import json
import requests
import time
from datetime import datetime
from module_features import Spacex_features
from typing import Any

BASE_URL = "https://api.spacexdata.com/v4"
CACHE_FILE = "Spacex_cache.json"
CACHE_DURATION = 3600  # in seconds


class SpaceXAPI_client:
    def __init__(self, base_url=BASE_URL, cache_file=CACHE_FILE, cache_duration=CACHE_DURATION):
        self.base_url = base_url
        self.cache_file = cache_file
        self.cache_duration = cache_duration

    def _is_cache_valid(self, endpoint: str) -> bool:
        """ Check if the cache file exists and contains valid data for the given endpoint."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as file:
                    cache = json.load(file)
                if endpoint in cache and time.time() - cache[endpoint]["timestamp"] < self.cache_duration:
                    return True
            except (json.JSONDecodeError, KeyError):
                return False
        return False

    def _read_cache(self, endpoint: str) -> list:
        """ Read cached data from the given endpoint. """
        with open(self.cache_file, "r") as file:
            cache = json.load(file)
        return cache[endpoint]["data"]

    def _write_cache(self, endpoint: str, data: list) -> None:
        """ Write data to the cache file from the given endpoint. """
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as file:
                    cache = json.load(file)
            except (json.JSONDecodeError, KeyError):
                cache = {}
        else:
            cache = {}
        cache[endpoint] = {"data": data, "timestamp": time.time()}
        with open(self.cache_file, "w") as file:
            json.dump(cache, file, indent=4)

    def fetch_data(self, endpoint: str) -> Any:
        """ Fetch data from the SpaceX API or cache file."""
        if self._is_cache_valid(endpoint):
            print(f"Serving data from cache for {endpoint}.")
            return self._read_cache(endpoint)
        try:
            url = f"{self.base_url}{endpoint}"
            print(f"Fetching data from API: {url}")
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self._write_cache(endpoint, data)
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {endpoint}: {e}")
            if self._is_cache_valid(endpoint):
                print("Serving stale data from cache.")
                return self._read_cache(endpoint)
            else:
                raise RuntimeError(f"Failed to fetch data from API and no cache available for {endpoint}.")

    def fetch_launches(self) -> dict:
        """ Fetch data from endpoint launches."""
        return self.fetch_data("/launches")

    def fetch_rockets(self) -> dict:
        """Fetch data from endpoint rockets."""
        return self.fetch_data("/rockets")

    def fetch_launchpads(self) -> dict:
        """Fetch data from endpoint launchpads."""
        return self.fetch_data("/launchpads")


if __name__ == "__main__":
    client = SpaceXAPI_client()
    features = Spacex_features(client)
    features.display_launch_key_details()
    date_range = (datetime(2000, 1, 1), datetime(2022, 12, 31))
    rocket_name = 'Falcon 9'
    success = True
    launch_site = "KSC LC 39A"

    features.launch_tracking(date_range, rocket_name, success, launch_site)
    features.statistics_generation()
    features.export_data()
