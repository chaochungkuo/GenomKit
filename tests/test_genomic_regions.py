import unittest
from genomkit import GRegions
import os

script_path = os.path.dirname(__file__)


class TestGRegions(unittest.TestCase):

    def test_len(self):
        regions = GRegions(name="test")
        regions.load(filename=os.path.join(script_path,
                                           "test_files/example.bed"))
        self.assertEqual(len(regions), 4)


if __name__ == '__main__':
    unittest.main()
