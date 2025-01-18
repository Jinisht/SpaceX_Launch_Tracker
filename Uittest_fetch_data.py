import unittest
from unittest.mock import patch, MagicMock
from typing import Any
import requests
from SpaxeX_main import SpaceXAPIClient


class TestSpaceXAPI(unittest.TestCase):
    def setUp(self):
        self.client = SpaceXAPIClient
        class MockAPI:
            def __init__(self):
                self.base_url = "https://api.spacexdata.com/v4/"

            def _is_cache_valid(self, endpoint: str) -> bool:
                return False  # Mocked; overridden later in specific tests

            def _read_cache(self, endpoint: str) -> Any:
                return {}  # Mocked; overridden later in specific tests

            def _write_cache(self, endpoint: str, data: Any) -> None:
                pass  # Mocked; overridden later in specific tests

            def fetch_data(self, endpoint: str) -> Any:
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

        self.api = MockAPI()

    @patch("requests.get")
    def test_fetch_data_from_api(self, mock_get):
        # Mock successful API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "test"}

        # Mock cache methods
        with patch.object(self.api, "_is_cache_valid", return_value=False), \
                patch.object(self.api, "_write_cache") as mock_write_cache:
            data = self.api.fetch_data("launches")
            self.assertEqual(data, {"data": "test"})
            mock_get.assert_called_once_with("https://api.spacexdata.com/v4/launches")
            mock_write_cache.assert_called_once_with("launches", {"data": "test"})

    @patch("requests.get")
    def test_fetch_data_from_cache(self, mock_get):
        # Mock cache is valid
        with patch.object(self.api, "_is_cache_valid", return_value=True), \
                patch.object(self.api, "_read_cache", return_value={"data": "cached"}):
            data = self.api.fetch_data("launches")
            self.assertEqual(data, {"data": "cached"})
            mock_get.assert_not_called()

    @patch("requests.get")
    def test_fetch_data_with_api_error_and_valid_cache(self, mock_get):
        # Mock API error
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        # Mock cache methods
        with patch.object(self.api, "_is_cache_valid", return_value=True), \
                patch.object(self.api, "_read_cache", return_value={"data": "cached"}):
            data = self.api.fetch_data("launches")
            self.assertEqual(data, {"data": "cached"})
            mock_get.assert_called_once_with("https://api.spacexdata.com/v4/launches")

    @patch("requests.get")
    def test_fetch_data_with_api_error_and_no_cache(self, mock_get):
        # Mock API error
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        # Mock cache is invalid
        with patch.object(self.api, "_is_cache_valid", return_value=False):
            with self.assertRaises(RuntimeError) as context:
                self.api.fetch_data("launches")
            self.assertIn("Failed to fetch data from API and no cache available", str(context.exception))
            mock_get.assert_called_once_with("https://api.spacexdata.com/v4/launches")


if __name__ == "__main__":
    unittest.main()
