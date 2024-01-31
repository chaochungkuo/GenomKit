import sys
# sys.path.append("/Users/jovesus/github/genomkit")
from genomkit.io import bed

bedreader = bed.ParserBED()
regions = bedreader.load("/Users/jovesus/sciebo/Projects/DNMT1_Efna5_Zimmer-Bensch/230817_ChIPseq/peaks_MACS2/common_peaks/ChIPseq_DNMT1_peaks_Control.bed")
print(len(regions))
print(regions[2])