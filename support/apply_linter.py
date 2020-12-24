#!/usr/bin/env python3

from collections import defaultdict
from pathlib import Path
from pprint import pprint
import subprocess


import os


def recursive_glob(rootdir=".", suffix=""):
    return [
        os.path.join(looproot, filename)
        for looproot, _, filenames in os.walk(rootdir)
        for filename in filenames
        if filename.endswith(suffix)
    ]


def is_import(line):
    return line.startswith("from ") or line.startswith("import ")


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


def sort_includes(clusters):
    sorted_clusters = []
    for cluster in clusters:
        if cluster:
            start = cluster[0][1]
            end = cluster[-1][1]
            sorted_clusters.append((sorted(cluster), (start, end)))
    return sorted_clusters


def read_lines(file_path):
    lines = []
    with open(file_path) as the_file:
        lines = the_file.readlines()
    return lines


def write_back(sorted_clusters, file_path):
    lines = []
    with open(file_path, "r+") as file_back:
        lines = file_back.readlines()
        for cluster in sorted_clusters:
            for j, i in enumerate(range(cluster[1][0], cluster[1][1] + 1)):
                lines[i] = cluster[0][j][0]
    with open(file_path, "w") as file_back:
        file_back.writelines(lines)


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


def apply_sorting_includes(lines, file_path):
    clusters = get_includes(lines)
    sorted_clusters = sort_includes(clusters)
    write_back(sorted_clusters, file_path)


def apply_removing_duplicates(lines, file_path):
    while remove_duplicated_imports(lines, file_path):
        pass


def is_function_def(line):
    return line.strip().startswith("def ")


def is_main_attr(line):
    return line.strip().startswith("if __name__")


def apply_sort_function(lines, file_path):
    new_lines = lines.copy()
    functions = defaultdict(tuple)

    for i, line in enumerate(lines):
        if is_function_def(line):
            function_line = line
            for j in range(i + 1, len(lines)):
                if is_function_def(lines[j]) or is_main_attr(line) or j == len(lines) - 1:
                    functions[function_line] = (i, j - 1)
                    break

    sorted_dict = list(sorted(functions.items(), key=lambda item: item[0]))
    sorted_dict_lines = list(sorted(functions.items(), key=lambda item: item[1][0]))

    for function, loc in functions.items():
        for the_loc in range(loc[0], loc[1]):
            new_lines[the_loc] = "\n"

    start = sorted_dict_lines[0][1][0]
    end = sorted_dict_lines[-1][1][1]
    new_start = start
    for entry in sorted_dict:
        the_range = entry[1][1] - entry[1][0]
        for i in range(the_range):
            new_lines[new_start + i] = lines[entry[1][0] + i]
        new_start += the_range + 1

    with open(file_path, "w") as file_back:
        file_back.writelines(new_lines)


def loop(file_paths, apply_function):
    for file_path in file_paths:
        lines = read_lines(file_path)
        apply_function(lines, file_path)


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_paths = recursive_glob(rootdir="samo_tidy/fixit", suffix=".py")
    print(f"Using files {file_paths}")

    loop(file_paths, apply_sorting_includes)
    loop(file_paths, apply_removing_duplicates)
    loop(file_paths, apply_sort_function)

    subprocess.call([f"black {os.path.join(dir_path, '..')} --line-length 120"], shell=True)


if __name__ == "__main__":
    main()
