=========================
Examples with FASTQ files
=========================

Trimming a FASTQ file for both sequences and quality
----------------------------------------------------

Sometimes you might want to trim the reads, for example, removing UMIs and adaptor from the first 20 bp in R2.

.. code-block:: python

    from genomkit import GSequences
    fastq = GSequences(name="R2", load=FASTQ_R2)
    fastq.trim(start=20, end=0)
    fastq.write_FASTQ(filename="R2_trimmed.fastq", gz=False)