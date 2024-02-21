========================
Starting with a BED file
========================

Get the sequences in FASTA format from a BED file
-------------------------------------------------

For example, you have a BED file for all the exons from hg38. Now you want to get their sequences in FASTA format with care of the orientation of the strands.

.. code-block:: python

    from genomkit import GRegions

    exons = GRegions(name="exons", load="hg38_exons.bed")
    exon_seqs = exons.get_GSequences(FASTA_file=FASTA_hg38)
    exon_seqs.write_fasta(filename="hg38_exons.fasta")
