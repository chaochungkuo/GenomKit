========
Examples
========

Extract exon, intron, and intergenetic regions in BED format from a GTF file
----------------------------------------------------------------------------

``GTF`` ``BED``

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

``GTF`` ``BED``


Extract the genes by their biotypes from a GTF file
---------------------------------------------------

