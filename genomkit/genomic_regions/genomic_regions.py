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

    def __init__(self, name: str = "", load: str = ""):
        self.elements = []
        self.sorted = False
        self.name = name
        if load:
            self.load(load)

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, key):
        return self.elements[key]

    def __iter__(self):
        return iter(self.elements)

    def add(self, region):
        self.elements.append(region)
        self.sorted = False

    def load(self, filename):
        regions = load_BED(filename=filename)
        self.elements = regions.elements
        self.sorted = False

    def sort(self, key=None, reverse=False):
        """Sort Elements by criteria defined by a GenomicRegion.

        *Keyword arguments:*

            - key -- given the key for comparison.
            - reverse -- reverse the sorting result.
        """
        if key:
            self.elements.sort(key=key, reverse=reverse)
        else:
            self.elements.sort()
            self.sorted = True

    def get_chrom(self):
        """Return all chromosomes."""
        return [r.sequence for r in self]

    def get_names(self):
        """Return a list of all region names. If the name is None,
        it return the region string."""
        names = []
        for r in self:
            if r.name:
                names.append(r.name)
            else:
                names.append(r.toString())
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