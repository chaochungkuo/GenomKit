from abc import ABC, abstractmethod


class GRegions(ABC):
    """
    Represents a collection of genomic regions.
    """

    def __init__(self, name: str = "", load: str = "", implementation: str = "iterative"):
        pass

    def __new__(self, name: str = "", load: str = "", implementation: str = "iterative"):
        """
        :type implementation: str, "iterative" / "tree", defaults to "iterative"
        """
        from genomkit import GRegionsIterative, GRegionsTree

        implementation_mapping = {
            "iterative": GRegionsIterative,
            "tree": GRegionsTree,
        }

        if implementation not in implementation_mapping:
            raise ValueError("Invalid implementation type. Must be 'iterative' or 'tree'")

        subclass = implementation_mapping[implementation]
        return object.__new__(subclass)  # Call subclass's __new__

    def intersect(self, target):
        assert self.implementation == target.implementation, "Both Gregions objects must have the same implementation"

    def close_regions(self, target):
        assert self.implementation == target.implementation, "Both Gregions objects must have the same implementation"

    def intersect_array(self, target):
        assert self.implementation == target.implementation, "Both Gregions objects must have the same implementation"

    def overlap_count(self, target):
        assert self.implementation == target.implementation, "Both Gregions objects must have the same implementation"
