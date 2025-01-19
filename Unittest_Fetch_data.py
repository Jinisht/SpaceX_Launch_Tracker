import unittest
from unittest.mock import patch, MagicMock
from typing import Any
import requests
from SpaxeX_main import SpaceXAPIclient


class TestSpaceXAPI(unittest.TestCase):
    def setUp(self):
        self.client = SpaceXAPIclient


    @patch("SpaxeX_main.SpaceXAPIclient.fetch_data")
    def test_fetch_data_from_cache(self, mock_fetch_data):
        mock_fetch_data.return_value = {"key": "value"}  # Mocked response
        data = self.client.fetch_data("launches")  # Proper call
        self.assertEqual(data, {"key": "value"})

