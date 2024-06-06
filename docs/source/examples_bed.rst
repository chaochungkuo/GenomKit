========================
Starting with a BED file
========================

.. note::

   These tutorials are still under active development.

Get the sequences in FASTA format from a BED file
-------------------------------------------------

For example, you have a BED file for all the exons from hg38. Now you want to get their sequences in FASTA format with care of the orientation of the strands.

.. code-block:: python

    from genomkit import GRegions

    exons = GRegions(name="exons", load="hg38_exons.bed")
    exon_seqs = exons.get_GSequences(FASTA_file=FASTA_hg38)
    exon_seqs.write_FASTA(filename="hg38_exons.fasta")


Get TSSs (Transcription Start Sites) and TTSs (Transcription Termination Sites) of genes in a BED file
------------------------------------------------------------------------------------------------------

Given a BED file with gene bodies (:ref:`Please refer to this tutorial <_gtf_all_genes>`), you can get the TSSs or TTSs regions with the size of 100 bp by the following codes:

.. code-block:: python

    from genomkit import GRegions

    genes = GRegions(name="genes", load="hg38_genes.bed")
    TSSs = genes.resize(extend_upstream=50, extend_downstream=50,
                        center="5prime", inplace=False)
    TTSs = genes.resize(extend_upstream=50, extend_downstream=50,
                        center="3prime", inplace=False)
    TSSs.write(filename="hg38_TSSs.bed")
    TTSs.write(filename="hg38_TTSs.bed")


Merging the nearby peaks in a BED file
--------------------------------------

Sometimes the peaks in a BED file are cluster together and you want to combine them if their distance is less than a certain value. For example, you want to combine all the peaks if their distance are below 50 bp.

.. code-block:: python

    from genomkit import GRegions

    peaks = GRegions(name="peaks", load="peaks.bed")
    clustered_peaks = peaks.cluster(max_distance=50)
    clustered_peaks.write(filename="clustered_peaks.bed")


Sampling the regions randomly in a BED file
-------------------------------------------

You can also randomly sample 1000 regions by the codes below:

.. code-block:: python

    from genomkit import GRegions

    peaks = GRegions(name="peaks", load="peaks.bed")
    samples = peaks.sampling(size=1000, seed=42)
    samples.write(filename="peaks_1000_samples.bed")


Find the peaks in one BED file close to the regions in another BED file
-----------------------------------------------------------------------

Often you want to find the interaction between two BED files, but not simply by overlapping. For example, now you have `hg38_promoters.bed` and `TFBSs.bed` and you want to find the TFBSs which are close to the promoters within 1000 bp.

.. code-block:: python

    from genomkit import GRegions

    promoters = GRegions(name="promoters", load="hg38_promoters.bed")
    promoters.extend(upstream=1000, downstream=1000, inplace=True)
    TFBSs = GRegions(name="TFBSs", load="TFBSs.bed")
    close_TFBSs = TFBSs.intersect(target=promoters, mode="ORIGINAL")
    close_TFBSs.write(filename="TFBSs_close_to_promoters.bed")

Generate a heapmap from two BED files: one BED file is used as windows and the other used as the signal
-------------------------

Sometimes your signals (scores) are stored in a BED file (column 5), instead of BEDGraph or BigWig. And now you want to visualize the interactions between these two BED files. For example, `DMSs.bed` contains the differential methylated CpGs with the score for hypermethylation or hypomethylation. And `TSSs.bed` include all transcription start sites with a window of 2000 bp. Now you want to visualize their interaction with a heatmap.


============================
Starting with many BED files
============================


When you have multiple BED files and want to investigate the interactions among those sets of genomic elements, you need to use `GRegionsSet` class. Below are some usage cases.

Test the relevance of multiple peaks in BED files to different biotypes in GTF
---------------------------

For example, you have 4 BED files for different peaks:

- `peaks_A.bed`
- `peaks_B.bed`
- `peaks_C.bed`
- `peaks_D.bed`

And you have generated some BED files for different biotypes in human (:ref:`Please refer to this tutorial <_gtf_genes_biotypes>`).

- `hg38_protein_coding_genes.bed`
- `hg38_lncRNA_genes.bed`
- `hg38_snRNA_genes.bed`
- `hg38_miRNA_genes.bed`

Now you want to check the overlaps of the peaks with the genes.

.. code-block:: python

    from genomkit import GRegionsSet
    # load peaks
    peaks_dict = {"A": "./peaks_A.bed",
                  "B": "./peaks_B.bed",
                  "C": "./peaks_C.bed",
                  "D": "./peaks_D.bed",}
    peaks = GRegionsSet(name="peaks", load_dict=peaks_dict)
    # load biotypes
    biotypes_dict = {"protein_coding": "./hg38_protein_coding_genes.bed",
                     "lncRNA": "./hg38_lncRNA_genes.bed",
                     "snRNA": "./hg38_snRNA_genes.bed",
                     "miRNA": "./hg38_miRNA_genes.bed",}
    biotypes = GRegionsSet(name="biotypes", load_dict=biotypes_dict)
    # Get a dataframe for overlapping counts
    overlaps = peaks.count_overlaps(query_set=biotypes)
    # Visualization

    # Testing the association
    peaks.test_