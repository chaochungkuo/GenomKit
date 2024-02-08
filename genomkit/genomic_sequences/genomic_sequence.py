from collections import Counter


class GSequence:
    """
    GSequence module

    This module contains functions and classes for working with a genomic
    sequence.
    """
    __slot__ = ["sequence", "quality", "name", "data"]

    def __init__(self, sequence: str, name: str = "", data: list = []):
        self.sequence = sequence.uppercase()
        self.name = name
        self.data = data

    def __len__(self):
        """
        Return the length of the sequence.

        :return: length
        :rtype: int
        """
        return len(self.sequence)

    def __hash__(self):
        return hash((self.sequence, self.name))

    def __eq__(self, other):
        return self.sequence == other.sequence

    def complement(self):
        conversion = {"A": "T",
                      "T": "A",
                      "C": "G",
                      "G": "C"}
        self.sequence = ''.join(conversion.get(char, char)
                                for char in self.sequence)

    def reverse(self):
        self.sequence = self.sequence[::-1]

    def reverse_complement(self):
        self.reverse()
        self.complement()

    def trim(self, start: int = 0, end: int = 0):
        if start:
            self.sequence = self.sequence[start:]
        if end:
            self.sequence = self.sequence[:-end]

    def dna2rna(self):
        self.sequence = self.sequence.replace("T", "U")

    def rna2dna(self):
        self.sequence = self.sequence.replace("U", "T")

    def count_table(self):
        return Counter(self.sequence)
