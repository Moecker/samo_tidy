#!/usr/bin/env python3

from pathlib import Path
import os

import os


def recursive_glob(rootdir=".", suffix=""):
    return [
        os.path.join(looproot, filename)
        for looproot, _, filenames in os.walk(rootdir)
        for filename in filenames
        if filename.endswith(suffix)
    ]


def get_includes(lines):
    clusters = []
    clusters_idx = 0
    clusters.append([])
    for i, line in enumerate(lines):
        if line.startswith("from") or line.startswith("import"):
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


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_paths = recursive_glob(rootdir="../samo_tidy/fixit", suffix=".py")
    for file_path in file_paths:
        lines = read_lines(file_path)
        clusters = get_includes(lines)
        sorted_clusters = sort_includes(clusters)
        write_back(sorted_clusters, file_path)


if __name__ == "__main__":
    main()
