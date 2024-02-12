import pyBigWig
import numpy as np
import pysam


class GCoverage:
    def __init__(self, bin_size: int = 1):
        """Initialize GCoverage object.

        :param bin_size: Size of the bin for coverage calculation.
                         Defaults to 1 (single nucleotide resolution).
        :type bin_size: str
        """
        self.coverage = {}
        self.bin_size = bin_size

    def load_coverage_from_bigwig(self, file_path: str):
        """Load coverage data from a bigwig file.

        :param file_path: Path to the bigwig file.
        :type file_path: str
        """
        bw = pyBigWig.open(file_path)
        chromosomes = bw.chroms()
        for chrom, chrom_length in chromosomes.items():
            coverage = bw.values(chrom, 0, chrom_length, numpy=True)
            if self.bin_size > 1:
                coverage = [np.mean(coverage[i:i+self.bin_size])
                            for i in range(0, len(coverage), self.bin_size)]
            self.coverage[chrom] = coverage
        bw.close()

    def calculate_coverage_from_bam(self, file_path: str):
        """Calculate coverage from a BAM file.

        :param file_path: Path to the BAM file.
        :type file_path: str
        """
        bam = pysam.AlignmentFile(file_path, "rb")
        for pileupcolumn in bam.pileup():
            chrom = bam.get_reference_name(pileupcolumn.reference_id)
            if chrom not in self.coverage:
                self.coverage[chrom] = [0] * bam.get_reference_length(chrom)
            self.coverage[chrom][pileupcolumn.reference_pos] += 1
        bam.close()
        # Adjust for bin size
        for chrom in self.coverage:
            if self.bin_size > 1:
                self.coverage[chrom] = [sum(self.coverage[chrom]
                                            [i:i+self.bin_size])
                                        / self.bin_size
                                        for i in range(0,
                                        len(self.coverage[chrom]),
                                        self.bin_size)]

    def get_coverage(self, chromosome: str):
        """Get coverage data for a specific chromosome.

        :param chromosome: Chromosome name.
        :type chromosome: str
        :return: Coverage data for the specified chromosome.
        :rtype: numpy array
        """
        return self.coverage.get(chromosome, [])

    def filter_regions_coverage(self, regions):
        """Filter regions for their coverages.

        :param regions: GRegions object containing regions.
        :type regions: GRegions
        :return: Dictionary where keys are region objects and values are
                 coverage lists.
        :rtype: dict
        """
        filtered_coverages = {}
        for region in regions:
            if region.sequence in self.coverage:
                start = region.start - 1  # 0-based indexing
                end = region.end
                coverage = self.coverage[region.sequence][start:end]
                filtered_coverages[region] = coverage
        return filtered_coverages
