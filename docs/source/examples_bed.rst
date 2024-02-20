=======================
Examples with BED files
=======================

Extract exon, intron, and intergenetic regions in BED format from a GTF file
----------------------------------------------------------------------------

``GTF_hg38`` is the path to the hg38 GTF file for annotation. Now you want to generate 3 BED files as below:

- hg38_exons.bed
- hg38_introns.bed
- hg38_intergenic_regions.bed

.. code-block:: python

    from genomkit import GRegions
    from genomkit import GAnnotation

    gtf = GAnnotation(file_path=GTF_hg38, file_format="gtf")
    genes = gtf.get_regions(element_type="gene")
    exons = gtf.get_regions(element_type="exon")
    introns = genes.subtract(exons, inplace=False)

    chromosomes = GRegions(name="chromosomes")
    chromosomes.get_chromosomes(organism="hg38")
    intergenic_regions = chromosomes.subtract(genes, inplace=False)
    exons.write(filename="hg38_exons.bed")
    introns.write(filename="hg38_introns.bed")
    intergenic_regions.write(filename="hg38_intergenic_regions.bed")


Get all promoter regions in BED format from a GTF file
------------------------------------------------------

``GTF_hg38`` is the path to the hg38 GTF file for annotation. Now you want to generate 3 BED files as below:

.. code-block:: python

    from genomkit import GAnnotation

    gtf = GAnnotation(file_path=GTF_hg38, file_format="gtf")
    genes = gtf.get_regions(element_type="gene")
    promoters = genes.resize(extend_upstream=2000,
                            extend_downstream=0,
                            center="5prime", inplace=False)
    promoters.write(filename="hg38_promoters.bed")

Extract the genes by their biotypes from a GTF file
---------------------------------------------------

``GTF_hg38`` is the path to the hg38 GTF file for annotation. Now you want to generate BED files for the biotypes below:

- protein_coding
- lncRNA
- snRNA
- miRNA

.. code-block:: python

    from genomkit import GAnnotation

    gtf = GAnnotation(file_path=GTF_hg38, file_format="gtf")
    target_biotypes = ["protein_coding", "lncRNA", "snRNA", "miRNA"]
    for biotype in target_biotypes:
        genes = gtf.get_regions(element_type="gene",
                                attribute="gene_type", value=biotype)
        genes.write(filename="hg38_genes_"+biotype+".bed")

Get the sequences in FASTA format from a BED file
-------------------------------------------------

For example, you have a BED file for all the exons from hg38. Now you want to get their sequences in FASTA format with care of the orientation of the strands.

.. code-block:: python

    from genomkit import GRegions

    exons = GRegions(name="exons", load="hg38_exons.bed")
    exon_seqs = exons.get_GSequences(FASTA_file=FASTA_hg38)
    exon_seqs.write_fasta(filename="hg38_exons.fasta")
