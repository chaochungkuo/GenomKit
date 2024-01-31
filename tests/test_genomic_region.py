import unittest
from genomkit import GRegion


class TestGRegion(unittest.TestCase):

    def test_len(self):
        region = GRegion(name="test", sequence="chr1", start=3, end=6)
        self.assertEqual(len(region), 3)

    def test_str(self):
        region = GRegion(name="test", sequence="chr1", start=3, end=6)
        self.assertEqual(str(region), "chr1:3-6 test .")

    def test_compare(self):
        region1 = GRegion(name="test", sequence="chr1", start=3, end=6)
        region2 = GRegion(name="test", sequence="chr1", start=7, end=10)
        self.assertEqual(region1 < region2, True)

        region1 = GRegion(name="test", sequence="chr1", start=3, end=6)
        region2 = GRegion(name="test", sequence="chr1", start=4, end=6)
        self.assertEqual(region1 < region2, True)

        region1 = GRegion(name="test", sequence="chr1", start=3, end=60)
        region2 = GRegion(name="test", sequence="chr1", start=4, end=6)
        self.assertEqual(region1 < region2, True)

        region1 = GRegion(name="test", sequence="chr1", start=3, end=6)
        region2 = GRegion(name="test", sequence="chr2", start=1, end=2)
        self.assertEqual(region1 < region2, True)

    def test_extend(self):
        region = GRegion(name="test", sequence="chr1", start=3, end=6)
        region.extend(upstream=1)
        self.assertEqual(len(region), 4)
        region.extend(downstream=10)
        self.assertEqual(len(region), 14)
        region.extend(upstream=-5)
        self.assertEqual(len(region), 9)
        region.extend(upstream=10)
        self.assertEqual(region.start, 0)

    def test_extend_fold(self):
        region = GRegion(name="test", sequence="chr1", start=10, end=20)
        region.extend_fold(upstream=0.1)
        self.assertEqual(region.start, 9)
        region.extend_fold(downstream=2)
        self.assertEqual(len(region), 33)


if __name__ == '__main__':
    unittest.main()
