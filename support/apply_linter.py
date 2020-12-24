#!/usr/bin/env python3

from collections import defaultdict
from pathlib import Path
from pprint import pprint
import os
import subprocess


def apply_black():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    subprocess.call([f"black {os.path.join(dir_path, '..')} --line-length 120"], shell=True)


def apply_removing_duplicates(lines, file_path):
    while remove_duplicated_imports(lines, file_path):
        pass


def apply_sort_functions(lines, file_path):
    new_lines = lines.copy()
    functions = find_functions(lines)
    sort_and_write(functions, new_lines, lines, file_path)


def apply_sort_targets(lines, file_path):
    new_lines = lines.copy()
    targets = find_targets(lines)
    sort_and_write(targets, new_lines, lines, file_path)


def apply_sorting_includes(lines, file_path):
    clusters = get_includes(lines)
    sorted_clusters = sort_includes(clusters)
    write_back(sorted_clusters, file_path)


def bazel_based_lint():
    file_paths = recursive_glob(rootdir="samo_tidy/utils/test", suffix="BUILD")

    print(f"Using bazel files")
    pprint(file_paths)

    print("Sorting targets...")
    loop(file_paths, apply_sort_targets)


def fill_new_lines(sorted_dict_lines, sorted_dict, lines, new_lines):
    new_start = sorted_dict_lines[0][1][0]
    for entry in sorted_dict:
        the_range = entry[1][1] - entry[1][0] - 1
        for i in range(the_range):
            new_lines[new_start + i] = lines[entry[1][0] + i]
        new_start += the_range + 1


def find_functions(lines):
    functions = defaultdict(tuple)

    for idx, line in enumerate(lines):
        if is_function_def(line):
            start = idx
            function_line = line
            for j in range(start + 1, len(lines)):
                if is_function_def(lines[j]) or is_main_attribute(lines[j]) or is_class_attribute(lines[j]):
                    functions[function_line] = (start, j)
                    break
                if j == len(lines) - 1:
                    functions[function_line] = (start, len(lines) + 1)
                    break
    return functions


def find_targets(lines):
    targets = defaultdict(tuple)

    for idx, line in enumerate(lines):
        if is_target_def(line):
            start = idx
            target_line = line.strip() + lines[idx + 1].strip()
            for j in range(start + 1, len(lines)):
                if lines[j].startswith(")"):
                    targets[target_line] = (start, j + 2)
                    break
    return targets


def get_includes(lines):
    clusters = []
    clusters_idx = 0
    clusters.append([])
    for i, line in enumerate(lines):
        if is_import(line):
            clusters[clusters_idx].append((line, i))
        if line == "\n":
            clusters_idx += 1
            clusters.append([])
    return clusters


def is_class_attribute(line):
    return line.strip().startswith("class ")


def is_function_def(line):
    return line.strip().startswith("def ")


def is_import(line):
    return line.startswith("from ") or line.startswith("import ")


def is_main_attribute(line):
    return line.strip().startswith("if __name__")


def is_patch_def(line):
    return line.strip().startswith("@patch ")


def is_target_def(line):
    return (
        False
        or line.strip().startswith("cc_binary")
        or line.strip().startswith("cc_library")
        or line.strip().startswith("cc_test")
        or line.strip().startswith("compilation_database")
        or line.strip().startswith("filegroup")
        or line.strip().startswith("py_binary")
        or line.strip().startswith("py_library")
        or line.strip().startswith("py_test")
        or line.strip().startswith("pycoverage")
        or line.strip().startswith("pylint")
        or line.strip().startswith("sh_test")
    )


def loop(file_paths, apply_function):
    for file_path in file_paths:
        lines = read_lines(file_path)
        apply_function(lines, file_path)


def main():
    python_based_lint()
    bazel_based_lint()


def python_based_lint():
    file_paths = recursive_glob(rootdir=".", suffix=".py")

    print(f"Using python files")
    pprint(file_paths)

    print("Sorting imports...")
    loop(file_paths, apply_sorting_includes)
    print("Removing duplicated imports...")
    loop(file_paths, apply_removing_duplicates)
    print("Sorting methods...")
    loop(file_paths, apply_sort_functions)

    print("Applying black...")
    apply_black()


def read_lines(file_path):
    lines = []
    with open(file_path) as the_file:
        lines = the_file.readlines()
    return lines


def recursive_glob(rootdir=".", suffix=""):
    return [
        os.path.join(looproot, filename)
        for looproot, _, filenames in os.walk(rootdir)
        for filename in filenames
        if filename.endswith(suffix)
    ]


def remove_duplicated_imports(lines, file_path):
    new_lines = lines
    line_dict = defaultdict(int)
    has_changed = False
    for line in lines:
        line_dict[line] += 1
        if is_import(line):
            for i in range(1, line_dict[line]):
                new_lines.remove(line)
                has_changed = True
    with open(file_path, "w") as file_back:
        file_back.writelines(new_lines)
    return has_changed


def sort_and_write(functions, new_lines, lines, file_path):
    sorted_dict = list(sorted(functions.items(), key=lambda item: item[0]))
    sorted_dict_lines = list(sorted(functions.items(), key=lambda item: item[1][0]))

    for function, loc in functions.items():
        for the_loc in range(loc[0], loc[1] - 1):
            new_lines[the_loc] = "\n"

    fill_new_lines(sorted_dict_lines, sorted_dict, lines, new_lines)

    with open(file_path, "w") as file_back:
        file_back.writelines(new_lines)


def sort_includes(clusters):
    sorted_clusters = []
    for cluster in clusters:
        if cluster:
            start = cluster[0][1]
            end = cluster[-1][1]
            sorted_clusters.append((sorted(cluster), (start, end)))
    return sorted_clusters


def write_back(sorted_clusters, file_path):
    lines = []
    with open(file_path, "r+") as file_back:
        lines = file_back.readlines()
        for cluster in sorted_clusters:
            for j, i in enumerate(range(cluster[1][0], cluster[1][1] + 1)):
                lines[i] = cluster[0][j][0]
    with open(file_path, "w") as file_back:
        file_back.writelines(lines)


if __name__ == "__main__":
    main()
