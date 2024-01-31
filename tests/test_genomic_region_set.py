import unittest
from genomkit import GRegionSet
import os

script_path = os.path.dirname(__file__)


class TestGRegionSet(unittest.TestCase):

    def test_len(self):
        regions = GRegionSet(name="test")
        regions.load(filename=os.path.join(script_path,
                                           "test_files/example.bed"))
        self.assertEqual(len(regions), 4)


if __name__ == '__main__':
    unittest.main()
