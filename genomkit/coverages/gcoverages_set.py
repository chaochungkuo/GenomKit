from genomkit import GCoverages
from collections import OrderedDict


class GCoveragesSet:
    """
    GCoveragesSet module

    This module contains functions and classes for working with multiple
    collections of genomic coverages. It provides utilities for handling and
    analyzing the interactions of many genomic coverages.
    """

    def __init__(self, name: str = "", load_dict=None):
        """Initiate a GCoveragesSet object which can contain multiple
        GCoverages.

        :param name: Define the name, defaults to ""
        :type name: str, optional
        :param load_dict: Given the file paths of multiple GCoverages as a
                          dictionary with names as keys and values as file
                          paths, defaults to None
        :type load_dict: dict, optional
        """
        self.collection = OrderedDict()
        if load_dict:
            for name, filename in load_dict.items():
                self.add(name=name,
                         regions=GCoverages(name=name,
                                          load=filename))