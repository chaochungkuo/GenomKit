import os
from genomkit import GRegion


###########################################################################
# IO functions
###########################################################################

def load_BED(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"The file '{filename}' does not exist.")
    else:
        res = GRegions()
        with open(filename, 'r') as file:
            for line in file:
                if not line.startswith("#"):
                    infos = line.strip().split()
                    res.add(GRegion(sequence=infos[0],
                                    start=int(infos[1]), end=int(infos[2]),
                                    orientation=infos[5],
                                    name=infos[3], score=infos[4]))
        return res


###########################################################################
# GRegions
###########################################################################


class GRegions:
    """
    GRegions module

    This module contains functions and classes for working with a collection of
    genomic regions. It provides utilities for handling and analyzing the
    interactions of many genomic coordinates.
    """
    def __init__(self, name: str = "", load: str = ""):
        """Create an empty GRegions object. If a path to a BED file is defined
        in "load", all the regions will be loaded.

        :param name: Name of this GRegions, defaults to ""
        :type name: str, optional
        :param load: Path to a BED file, defaults to ""
        :type load: str, optional
        """
        self.elements = []
        self.sorted = False
        self.name = name
        if load:
            self.load(load)

    def __len__(self):
        """Return the number of regions in this GRegions.

        :return: Number of regions
        :rtype: int
        """
        return len(self.elements)

    def __getitem__(self, key):
        return self.elements[key]

    def __iter__(self):
        return iter(self.elements)

    def add(self, region):
        """Append a GRegion at the end of the elements of GRegions.

        :param region: A GRegion
        :type region: GRegion
        """
        self.elements.append(region)
        self.sorted = False

    def load(self, filename):
        """Load a BED file into the GRegions.

        :param filename: Path to the BED file
        :type filename: str
        """
        regions = load_BED(filename=filename)
        self.elements = regions.elements
        self.sorted = False

    def sort(self, key=None, reverse=False):
        """Sort elements by criteria defined by a GenomicRegion.

        :param key: Given the key for comparison.
        :type key: str
        :param reverse: Reverse the sorting result.
        :type reverse: bool
        """
        if key:
            self.elements.sort(key=key, reverse=reverse)
        else:
            self.elements.sort()
            self.sorted = True

    def get_chrom(self, unique=False):
        """Return all chromosomes.

        :param unique: Only the unique names.
        :type unique: bool
        :return: A list of all chromosomes.
        :rtype: list
        """
        res = [r.sequence for r in self]
        if unique:
            res = list(set(res))
        return res

    def get_names(self):
        """Return a list of all region names. If the name is None,
        it return the region string.

        :return: A list of all regions' names.
        :rtype: list
        """
        names = [r.name if r.name else r.toString() for r in self]
        return names

    def extend(self, upstream: int = 0, downstream: int = 0,
               strandness: bool = False, inplace: bool = True):
        """Perform extend step for every element. The extension length can also
        be negative values which shrinkages the regions.

        :param upstream: Define how many bp to extend toward upstream
                         direction. If percentage is set True, it takes float
                         as percentage. 0.5 for 50%, for example.
        :type upstream: int or float
        :param downstream: Define how many bp to extend toward downstream
                          direction. If percentage is set True, it takes float
                          as percentage. 0.5 for 50%, for example.
        :type downstream: int or float
        :param percentage: Define whether the input is percentage.
        :type percentage: boolean
        :param inplace: Define whether this operation will be applied on the
                        same object (True) or return a new object..
        :type inplace: boolean
        :return: None
        """
        if inplace:
            for region in self.elements:
                region.extend(upstream=upstream,
                              downstream=downstream,
                              strandness=strandness,
                              inplace=True)
        else:
            output = GRegions(name=self.name)
            for region in self.elements:
                r = region.extend(upstream=upstream,
                                  downstream=downstream,
                                  strandness=strandness,
                                  inplace=False)
                output.add(r)
            return output

    def extend_fold(self, upstream: float = 0.0, downstream: float = 0.0,
                    strandness: bool = False, inplace: bool = True):
        """Perform extend step for every element. The extension length can also
        be negative values which shrinkages the regions.

        :param upstream: Define how many bp to extend toward upstream
                         direction. If percentage is set True, it takes float
                         as percentage. 0.5 for 50%, for example.
        :type upstream: int or float
        :param downstream: Define how many bp to extend toward downstream
                          direction. If percentage is set True, it takes float
                          as percentage. 0.5 for 50%, for example.
        :type downstream: int or float
        :param percentage: Define whether the input is percentage.
        :type percentage: boolean
        :param inplace: Define whether this operation will be applied on the
                        same object (True) or return a new object..
        :type inplace: boolean
        :return: None
        """
        if inplace:
            for region in self.elements:
                region.extend_fold(upstream=upstream,
                                   downstream=downstream,
                                   strandness=strandness,
                                   inplace=True)
        else:
            output = GRegions(name=self.name)
            for region in self.elements:
                r = region.extend_fold(upstream=upstream,
                                       downstream=downstream,
                                       strandness=strandness,
                                       inplace=False)
                output.add(r)
            return output
