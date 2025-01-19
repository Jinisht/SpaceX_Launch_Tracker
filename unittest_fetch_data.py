import unittest
from unittest.mock import patch
from main import SpaceXAPI_client


class TestSpaceXAPI(unittest.TestCase):
    def setUp(self):
        self.client = SpaceXAPI_client


    @patch("SpaxeX_main.SpaceXAPIclient.fetch_data")
    def test_fetch_data_from_cache(self, mock_fetch_data):
        mock_fetch_data.return_value = {"key": "value"}  # Mocked response
        data = self.client.fetch_data("launches")
        self.assertEqual(data, {"key": "value"})

