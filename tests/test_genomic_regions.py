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
        regions = GRegions(name="test")
        regions.load(filename=os.path.join(script_path,
                                           "test_files/genes_Gencode_hg38_chr22.bed"))
        self.assertEqual(len(regions), 1372)

    def test_extend(self):
        regions = GRegions(name="test")
        regions.load(filename=os.path.join(script_path,
                                           "test_files/example.bed"))
        self.assertEqual(regions.extend(upstream=100,
                                        inplace=False)[0].start, 900)
        self.assertEqual(regions.extend(upstream=100,
                                        inplace=False)[1].start, 2900)
        self.assertEqual(regions.extend(upstream=100, strandness=True,
                                        inplace=False)[1].start, 3000)
        self.assertEqual(regions.extend(downstream=100, strandness=True,
                                        inplace=False)[1].start, 2900)

    def test_extend_fold(self):
        regions = GRegions(name="test")
        regions.load(filename=os.path.join(script_path,
                                           "test_files/example.bed"))
        self.assertEqual(regions.extend_fold(upstream=0.1,
                                             inplace=False)[0].start, 900)
        self.assertEqual(regions.extend_fold(upstream=0.1,
                                             inplace=False)[1].start, 2900)
        self.assertEqual(regions.extend_fold(upstream=0.1, strandness=True,
                                             inplace=False)[1].start, 3000)
        self.assertEqual(regions.extend_fold(downstream=0.1, strandness=True,
                                             inplace=False)[1].start, 2900)

    def test_get_sequences(self):
        regions = GRegions(name="test")
        regions.load(filename=os.path.join(script_path,
                                           "test_files/example.bed"))
        self.assertEqual(regions.get_sequences(),
                         ["chr1", "chr1", "chr2", "chr2"])
        self.assertEqual(regions.get_sequences(unique=True),
                         ["chr1", "chr2"])

    def test_get_names(self):
        regions = GRegions(name="test")
        regions.load(filename=os.path.join(script_path,
                                           "test_files/example.bed"))
        self.assertEqual(regions.get_names(), ["Feature1", "Feature2",
                                               "Feature3", "Feature4"])
        self.assertEqual(regions.get_names(unique=True),
                         ["Feature1", "Feature2", "Feature3", "Feature4"])


if __name__ == '__main__':
    unittest.main()
