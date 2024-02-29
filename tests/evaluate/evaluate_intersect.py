from genomkit import GRegions
import os
import timeit
# import pybedtools
import memory_profiler


script_path = os.path.dirname(__file__)

# genes_bed_file = os.path.join(script_path,
#                               "../test_files/bed/example.bed")
# peaks_bed_file = os.path.join(script_path,
#                               "../test_files/bed/example2.bed")
genes_bed_file = os.path.join(script_path,
                              "../test_files/bed/genes_Gencode_mm10.bed")
peaks_bed_file = os.path.join(script_path,
                              "../test_files/bed/consensus_peaks.bed")
genes = GRegions(name="genes", load=genes_bed_file)
# print(len(genes))
peaks = GRegions(name="genes", load=peaks_bed_file)
# print(len(peaks))


@profile # noqa
def time_intersect_python():
    intersect = peaks.intersect(genes)


@profile # noqa
def time_intersect_array():
    intersect = peaks.intersect_array(genes)

repeat_num = 2
execution_time = timeit.timeit(time_intersect_python, number=repeat_num)
print('[{:<20}]'.format('intersect_python'), '{:<5.2f}'.format(execution_time), "seconds")
execution_time = timeit.timeit(time_intersect_array, number=repeat_num)
print('[{:<20}]'.format('intersect_array'), '{:<5.2f}'.format(execution_time), "seconds")
# print(len(intersect))
# intersect.write("intersect_python.bed")
# print(len(intersect))
# intersect.write("intersect_array.bed")

# # Load the BED files using pybedtools
# genes_bed = pybedtools.BedTool(genes_bed_file)
# peaks_bed = pybedtools.BedTool(peaks_bed_file)

# # Get the intersection of the two BED files
# intersection = genes_bed.intersect(peaks_bed, u=True)

# # Convert the intersection to a list of intervals
# intersection_list = list(intersection)
# print(len(intersection_list))
