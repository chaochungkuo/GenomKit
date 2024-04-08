###################################################################################################
######################### File should be run from the root of the repository ######################
############### Command: python -m memory_profiler tests/evaluate/evaluate_intersect.py ###########
###################################################################################################

# Evaluate the performance of the intersect method of the GRegions class
# versus the intersect method of the gregions_tree class

import os
import timeit
import itertools
import memory_profiler
import pandas as pd
from tqdm import tqdm

from genomkit import GRegions


# Define test cases
def generate_test_cases():
    # Define test files
    genes_bed_file = "tests/test_files/bed/genes_Gencode_mm10.bed"
    peaks_bed_file = "tests/test_files/bed/consensus_peaks.bed"

    bed_paths = [genes_bed_file, peaks_bed_file]
    modes = ["OVERLAP", "ORIGINAL", "COMP_INCL"]
    test_cases = []

    for i, (path1, path2, mode) in enumerate(itertools.product(bed_paths, bed_paths, modes), start=1):
        test_cases.append((f"Test Case: {i}", path1, path2, mode))

    return test_cases


# test_cases = [
#     (
#         "Test Case 1",
#         genes_bed_file,
#         peaks_bed_file,
#     ),
#     (
#         "Test Case 2",
#         peaks_bed_file,
#         genes_bed_file,
#     ),
#     (
#         "Test Case 3",
#         genes_bed_file,
#         genes_bed_file,
#     ),
#     (
#         "Test Case 4",
#         peaks_bed_file,
#         peaks_bed_file,
#     ),
# ]


# Define functions to be profiled
@profile
def time_intersect_python(regions1, regions2, mode):
    intersect = regions1.intersect(regions2)
    return intersect


@profile
def time_intersect_tree(regions1, regions2, mode):
    intersect = regions1.intersect(regions2)
    return intersect


def get_raw_intervals_from_python(regions):
    intervals = []
    for interval in regions:
        raw_interval = (interval.start, interval.end)
        intervals.append(raw_interval)
    return intervals


def are_intervals_identical(result_python, result_tree):
    """
    Check if two sets of intervals are identical.

    Args:
        result_python (list): List of intervals from the Python implementation.
        result_tree (list): List of intervals from the tree implementation.

    Returns:
        bool: True if the sets of intervals are identical, False otherwise.
    """
    tree_intervals = get_raw_intervals_from_python(result_tree)
    python_intervals = get_raw_intervals_from_python(result_python)
    return set(tree_intervals) == set(python_intervals)


repeat_num = 1
results = []
test_cases = generate_test_cases()
print("number of test cases: ", len(test_cases))

# Measure execution time and memory consumption for each test case
for case_name, regions1_file_path, regions2_file_path, mode in tqdm(test_cases):
    ############# GRegions Evaluation #############
    start_time = timeit.default_timer()
    regions1 = GRegions(name="genes", load=regions1_file_path)
    regions2 = GRegions(name="genes", load=regions2_file_path)
    construction_time_regions = timeit.default_timer() - start_time
    execution_time_python = timeit.timeit(lambda: time_intersect_python(regions1, regions2, mode), number=repeat_num)
    mem_usage_python = memory_profiler.memory_usage((time_intersect_python, (regions1, regions2, mode)))

    ############# GRegionsTree Evaluation #############
    start_time = timeit.default_timer()
    regions1 = GRegions(name="genes", load=regions1_file_path, implementation="tree")
    regions2 = GRegions(name="genes", load=regions2_file_path, implementation="tree")
    construction_time_tree = timeit.default_timer() - start_time
    execution_time_tree = timeit.timeit(lambda: time_intersect_tree(regions1, regions2, mode), number=repeat_num)
    mem_usage_tree = memory_profiler.memory_usage((time_intersect_tree, (regions1, regions2, mode)))

    # Compare results, to make sure they are identical
    result_python = regions1.intersect(regions2)
    result_tree = regions1.intersect(regions2)
    results_are_identical = are_intervals_identical(result_python, result_tree)

    results.append(
        (
            case_name,
            os.path.basename(regions1_file_path),
            os.path.basename(regions2_file_path),
            mode,
            construction_time_regions,
            execution_time_python,
            construction_time_regions + execution_time_python,
            max(mem_usage_python),
            construction_time_tree,
            execution_time_tree,
            construction_time_tree + execution_time_tree,
            max(mem_usage_tree),
            results_are_identical,
        )
    )
    print()

# Create a DataFrame from the results list
df = pd.DataFrame(
    results,
    columns=[
        "Test Case",
        "Regions1 File",
        "Regions2 File",
        "Mode",
        "Construction Time (Python)",
        "Execution Time (Python)",
        "Overall Time (intersect_python)",
        "Memory Usage Python (MB)",
        "Construction Time (GRegionsTree)",
        "Execution Time (Tree)",
        "Overall Time (intersect_tree)",
        "Memory Usage Tree(MB)",
        "Identical Results",
    ],
)

# Write the DataFrame to a file
df.to_csv("tests/evaluate/output.csv", index=False)

print("Results saved to output.csv")
