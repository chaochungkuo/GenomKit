import os
from genomkit import GRegion
import copy


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
                         direction.
        :type upstream: int
        :param downstream: Define how many bp to extend toward downstream
                          direction.
        :type downstream: int
        :param strandness: Define whether strandness is considered.
        :type strandness: bool
        :param inplace: Define whether this operation will be applied on the
                        same object (True) or return a new object.
        :type inplace: bool
        :return: None or a GRegions object
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

        :param upstream: Define the percentage of the region length to extend
                         toward upstream direction.
        :type upstream: float
        :param downstream: Define the percentage of the region length to extend
                           toward downstream direction.
        :type downstream: float
        :param strandness: Define whether strandness is considered.
        :type strandness: bool
        :param inplace: Define whether this operation will be applied on the
                        same object (True) or return a new object..
        :type inplace: bool
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

    def intersect(self, target, mode="OVERLAP",
                  rm_duplicates=False):
        """Return a GRegions for the intersections between the two given
        GRegions objects. There are three modes for overlapping:

        *mode = "OVERLAP"*

            Return a new GRegions including only the overlapping regions
            with target GRegions.

            .. note:: it will merge the regions.

            ::

                self       ----------              ------
                target            ----------                    ----
                Result            ---

        *mode = "ORIGINAL"*

            Return the regions of original GenomicRegionSet which have any
            intersections with target GRegions.

            ::

                self       ----------              ------
                target          ----------                    ----
                Result     ----------

        *mode = "COMP_INCL"*

            Return region(s) of the GenomicRegionSet which are 'completely'
            included by target GRegions.

            ::

                self        -------------             ------
                target              ----------      ---------------       ----
                Result                                ------

        :param target: A target GRegions for finding overlaps.
        :type target: GRegions
        :param mode: The mode should be one of the followings: "OVERLAP",
                     "ORIGINAL", or "COMP_INCL".
        :type mode: str
        :param rm_duplicates: Define whether remove the duplicates.
        :type rm_duplicates: bool
        :return: A GRegions.
        :rtype: GRegions
        """
        new_regions = GRegions(self.name)
        if len(self) == 0 or len(target) == 0:
            return new_regions
        else:
            a = copy.deepcopy(self)
            b = copy.deepcopy(target)
            if not a.sorted:
                a.sort()
            if not b.sorted:
                b.sort()
            if mode == "OVERLAP":
                a.merge()
                b.merge()

            iter_a = iter(a)
            s = next(iter_a)
            last_j = len(b) - 1
            j = 0
            cont_loop = True
            pre_inter = 0
            cont_overlap = False
            # OVERLAP ###############################
            if mode == "OVERLAP":
                while cont_loop:
                    # When the regions overlap
                    if s.overlap(b[j]):
                        new_regions.add(GRegion(sequence=s.chrom,
                                                start=max(s.start, b[j].start),
                                                end=min(s.end, b[j].end),
                                                name=s.name,
                                                orientation=s.orientation,
                                                data=s.data))
                        if not cont_overlap:
                            pre_inter = j
                        if j == last_j:
                            try:
                                s = next(iter_a)
                            except StopIteration:
                                cont_loop = False
                        else:
                            j += 1
                        cont_overlap = True

                    elif s < b[j]:
                        try:
                            s = next(iter_a)
                            if s.chrom == b[j].chrom and pre_inter > 0:
                                j = pre_inter
                            cont_overlap = False
                        except StopIteration:
                            cont_loop = False

                    elif s > b[j]:
                        if j == last_j:
                            cont_loop = False
                        else:
                            j += 1
                            cont_overlap = False
                    else:
                        try:
                            s = next(iter_a)
                        except StopIteration:
                            cont_loop = False

            # ORIGINAL ###############################
            if mode == "ORIGINAL":
                while cont_loop:
                    # When the regions overlap
                    if s.overlap(b[j]):
                        new_regions.add(s)
                        try:
                            s = next(iter_a)
                        except StopIteration:
                            cont_loop = False
                    elif s < b[j]:
                        try:
                            s = next(iter_a)
                        except StopIteration:
                            cont_loop = False
                    elif s > b[j]:
                        if j == last_j:
                            cont_loop = False
                        else:
                            j += 1
                    else:
                        try:
                            s = next(iter_a)
                        except StopIteration:
                            cont_loop = False
            # COMP_INCL ###############################
            if mode == "COMP_INCL":
                while cont_loop:
                    # When the regions overlap
                    if s.overlap(b[j]):
                        if s.initial >= b[j].initial and s.final <= b[j].final:
                            new_regions.add(s)
                        if not cont_overlap:
                            pre_inter = j
                        if j == last_j:
                            try:
                                s = next(iter_a)
                            except StopIteration:
                                cont_loop = False
                        else:
                            j += 1
                        cont_overlap = True

                    elif s < b[j]:
                        try:
                            s = next(iter_a)
                            if s.chrom == b[j].chrom and pre_inter > 0:
                                j = pre_inter
                            cont_overlap = False
                        except StopIteration:
                            cont_loop = False

                    elif s > b[j]:
                        if j == last_j:
                            cont_loop = False
                        else:
                            j += 1
                            cont_overlap = False
                    else:
                        try:
                            s = next(iter_a)
                        except StopIteration:
                            cont_loop = False

            if rm_duplicates:
                new_regions.remove_duplicates()
            # new_regions.sort()
            return new_regions

    def remove_duplicates(self, sort=True):
        """
        Remove any duplicate regions (sorted, by default).
        """
        self.elements = list(set(self.elements))
        if sort:
            self.sort()
