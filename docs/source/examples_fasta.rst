========================
Starting with a FASTA file
========================

.. note::

   These tutorials are still under active development.

Extract the sequences in FASTA format from the genome sequence by a BED files
-------------------------------------------------

For example, you have a list of genes and want to achieve the following tasks:

- Extract the genes from GTF file
- Get all exons of the selected genes
- Select the transcript which has the most exon number and keep only this transcript
- Extract the sequences of these selected exons and concatenate them in a proper order (starting from exon 1 and each sequence starts from 5 prime end)
- Save the sequences into FASTA file. One file per gene (including multiple exons)

.. code-block:: python

    from genomkit import GAnnotation
    from collections import Counter
    from genomkit import GRegion, GRegions, GSequences

    GTF_PATH = "GRCm39/gencode.vM34.basic.annotation.gtf"
    FASTA_file = "GRCm39/GRCm39.primary_assembly.genome.fa"
    gtf = GAnnotation(file_path=GTF_PATH, file_format="gtf")
    genes = gtf.get_regions(element_type="gene")

    # Loading the names
    with open("gene_names.txt") as f:
        sel_gene_names = [line.strip() for line in f]
    # Load genome FASTA
    fasta = GSequences(name="GRCm39", load=FASTA_file)
    # Iterate genes
    for gene_name in sel_gene_names:
        exons = gtf.filter_elements(element_type="exon", attribute="gene_name", value=gene_name)
        transcript_list = []
        for e in exons:
            transcript_list.append(e["transcript_id"])
        counter = Counter(transcript_list)
        most_transcript, count = counter.most_common(1)[0]
        print(most_transcript, count)
        sel_exons = [e for e in exons if e["transcript_id"] == most_transcript]
        # sort exon by their exon number
        sel_exons = sorted(sel_exons, key=lambda x: int(x['exon_number']))
        exon_regions = GRegions(name=gene_name)
        for e in sel_exons:
            exon_regions.add(GRegion(sequence=e["chr"],
                                     start=e["start"],
                                     end=e["end"],
                                     orientation=e["strand"],
                                     name=e["gene_name"]+"_exon"+e["exon_number"]))
        exon_seqs = fasta.extract_seqs_by_regions(regions=exon_regions)
        exon_seqs.write_FASTA(filename="{}.fasta".format(gene_name))
