from genomkit import GAnnotation

hg38 = GAnnotation(file_format="gtf",
                   file_path="/Users/ckuo/Downloads/gencode.v45.primary_assembly.annotation.gtf.gz")

for key, value in hg38.genes.items():
    print(key, ":", value)
    break
# print(len(hg38.transcripts))
# print(len(hg38.exons))

genes = hg38.get_gene_names()
gene = hg38.get_gene("RANP4")
print(gene)
res = hg38.filter_elements(element_type="gene",
                           attribute="gene_name", value="RANP4")
print(res)
