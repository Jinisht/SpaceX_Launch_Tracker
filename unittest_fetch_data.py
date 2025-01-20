import unittest
from unittest.mock import patch
from main import SpaceXAPI_client


class Test_spaceX_API(unittest.TestCase):
    def setUp(self):
        self.client = SpaceXAPI_client

    @patch("main.SpaceXAPI_client.fetch_data")
    def test_fetch_data_from_cache(self, mock_fetch_data) -> None:
        mock_fetch_data.return_value = {"key": "value"}
        data: dict[str, str] = self.client.fetch_data("launches")
        self.assertEqual(data, {"key": "value"})

