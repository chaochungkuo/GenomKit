from .io import load_FASTA, load_FASTA_from_file, \
                load_FASTQ, load_FASTQ_from_file
import gzip


###########################################################################
# GSequences
###########################################################################
class GSequences:
    """
    GSequences module

    This module contains functions and classes for working with a collection of
    genomic sequences. It provides utilities for handling and analyzing the
    interactions of many genomic sequences.
    """
    def __init__(self, name: str = "", load: str = ""):
        self.elements = []
        self.name = name
        if load:
            self.load(load)

    def __len__(self):
        """Return the number of regions in this GSequences.

        :return: Number of sequences
        :rtype: int
        """
        return len(self.elements)

    def __getitem__(self, key):
        return self.elements[key]

    def add(self, sequence):
        """Append a GSequence at the end of the elements of GSequences.

        :param sequence: A GSequence
        :type sequence: GSequence
        """
        self.elements.append(sequence)

    def load(self, filename: str):
        """Load a FASTA/FASTQ file into the GSequences.

        :param filename: Path to the FASTA/FASTQ file
        :type filename: str
        """
        if filename.endswith(".fasta") or filename.endswith(".fa"):
            res = load_FASTA(filename)
        elif filename.endswith(".fastq") or filename.endswith(".fq"):
            res = load_FASTQ(filename)
        elif filename.endswith(".fasta.gz") or filename.endswith(".fa.gz"):
            with gzip.open(filename, 'rt') as f:
                res = load_FASTA_from_file(f)
        elif filename.endswith(".fastq.gz") or filename.endswith(".fq.gz"):
            with gzip.open(filename, 'rt') as f:
                res = load_FASTQ_from_file(f)
        else:
            raise ValueError("Unsupported file format")
        self.elements = res.elements
