========================
Starting with a GTF file
========================

.. note::

   These tutorials are still under active development.

Because ``GAnnotation`` is able to handle both ``GTF`` and ``GFF``, you can replace the GTF file in the tutorials below with the GFF file. Here we show only GTFs as examples.

.. _gtf_all_genes:

Get all the genes from a GTF file
---------------------------------------------------

``GTF_hg38`` is the path to the hg38 GTF file for annotation.

.. code-block:: python

    from genomkit import GAnnotation

    gtf = GAnnotation(file_path=GTF_hg38, file_format="gtf")
    genes = gtf.get_regions(element_type="gene")
    genes.write(filename="hg38_genes.bed")


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

.. _gtf_genes_biotypes:

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

