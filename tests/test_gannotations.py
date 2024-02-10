from genomkit import GAnnotation

hg38 = GAnnotation(file_format="gtf",
                   file_path="/Users/ckuo/Downloads/gencode.v45.primary_assembly.annotation.gtf.gz")
print(len(hg38.genes))
print(len(hg38.transcripts))
print(len(hg38.exons))
