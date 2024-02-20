from genomkit import GRegions
from collections import OrderedDict


class GRegionsSet:
    """
    GRegionsSet module

    This module contains functions and classes for working with a collection of
    multiple GRegions.
    """
    def __init__(self, name: str = "", load_dict=None):
        self.collection = OrderedDict()
        if load_dict:
            for name, filename in load_dict.items():
                self.add(name=name,
                         regions=GRegions(name=name,
                                          load=filename))

    def add(self, name: str, regions):
        self.collection[name] = regions

    def __len__(self):
        return len(self.collection)

    def __getattr__(self, key):
        if key in self.collection:
            return self.collection[key]
        else:
            raise AttributeError(
                f"'{self.collection.__class__.__name__}'"
                f" object has no attribute '{key}'"
                )

    def __setattr__(self, key, value):
        self.collection[key] = value

    def get_names(self):
        return list(self.collection.keys())

    def get_lengths(self):
        res = OrderedDict()
        for name, regions in self.collection.items():
            res[name] = len(regions)
        return res
