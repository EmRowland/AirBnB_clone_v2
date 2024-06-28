#!/usr/bin/python3
import unittest
from models.engine.file_storage import FileStorage
from models.state import State

"""
Test file for delete task

"""


class TestFileStorageDelete(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.storage = FileStorage()
        self.storage._FileStorage__objects = {}

    def test_delete(self):
        """Test that delete method removes object from storage"""
        state = State()
        state.name = "California"
        self.storage.new(state)
        self.storage.save()

        self.assertIn(f"State.{state.id}", self.storage.all())

        self.storage.delete(state)
        self.assertNotIn(f"State.{state.id}", self.storage.all())

    def test_delete_non_existent(self):
        """Test that delete method does nothing if object does not exist"""
        state = State()
        state.name = "California"
        self.storage.delete(state)  # Should not raise an exception


if __name__ == "__main__":
    unittest.main()
