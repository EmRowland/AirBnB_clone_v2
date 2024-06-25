#!/usr/bin/python3
""" Test Console Module """

import unittest
from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place
from io import StringIO
from unittest.mock import patch


class TestHBNBCommand(unittest.TestCase):

    @patch("sys.stdout", new_callable=StringIO)
    def test_create_with_parameters(self, mock_stdout):
        """Test create command with parameters"""
        cmd = HBNBCommand()

        # Test creating a State object
        cmd.onecmd('create State name="California"')
        state_id = mock_stdout.getvalue().strip()
        state = storage.all()[f"State.{state_id}"]
        self.assertEqual(state.name, "California")

        # Test creating a Place object
        cmd.onecmd(
            "create Place "
            'city_id="0001" '
            'user_id="0001" '
            'name="My_little_house" '
            "number_rooms=4 "
            "number_bathrooms=2 "
            "max_guest=10 "
            "price_by_night=300 "
            "latitude=37.773972 "
            "longitude=-122.431297"
        )
        place_id = mock_stdout.getvalue().strip().split()[-1]
        place = storage.all()[f"Place.{place_id}"]
        self.assertEqual(place.city_id, "0001")
        self.assertEqual(place.user_id, "0001")
        self.assertEqual(place.name, "My_little_house")
        # Ensure consistent naming
        self.assertEqual(place.number_rooms, 4)
        self.assertEqual(place.number_bathrooms, 2)
        self.assertEqual(place.max_guest, 10)
        self.assertEqual(place.price_by_night, 300)
        self.assertEqual(place.latitude, 37.773972)
        self.assertEqual(place.longitude, -122.431297)
        # Add more tests as needed for edge cases, error handling, etc.


if __name__ == "__main__":

    unittest.main()
