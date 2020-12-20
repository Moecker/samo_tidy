import os
from collections import defaultdict


def get_summary():
    """Summars is being used as a singleton, returns the singleton instance.
    Note that there will be a instance per process"""
    return the_summary


def clear_summary():
    """Clears summary, purpose is testing or multiprocessing"""
    the_summary = Summary()


def limit_set_display(the_set):
    """Beautify output"""
    MAX_DISPLAY = 10
    list_to_show = list(the_set)[0:MAX_DISPLAY]
    remaining = len(the_set) - MAX_DISPLAY
    if remaining > 0:
        list_to_show.append(
            f"and {remaining} more",
        )

    return list_to_show


def merge(list_of_summaries):
    """Merges multiple summaries, return the merged one"""
    result = Summary()
    for a_summary in list_of_summaries:
        result.analyzed_file_names.update(a_summary.analyzed_file_names)
        result.analyzed_translation_units.update(a_summary.analyzed_translation_units)
        result.failed_translation_units.update(a_summary.failed_translation_units)
        result.ignored_translation_units.update(a_summary.ignored_translation_units)
        result.skipped_commands.update(a_summary.skipped_commands)
        result.skipped_filenames.update(a_summary.skipped_filenames)
        result.number_of_violations.update(a_summary.number_of_violations)
    return result


class Summary:
    def __init__(self):
        self.analyzed_file_names = set()
        self.analyzed_translation_units = set()
        self.failed_translation_units = set()
        self.ignored_translation_units = set()
        self.number_of_violations = defaultdict(set)
        self.skipped_commands = set()
        self.skipped_filenames = set()

    def present(self):
        return {
            "Analyzed Files": limit_set_display(self.analyzed_file_names),
            "Analyzed Translation Units": limit_set_display(self.analyzed_translation_units),
            "Failed Translation Units with parse errors": limit_set_display(self.failed_translation_units),
            "Ignored External Translation Units": limit_set_display(self.ignored_translation_units),
            "Skipped Commands from Files Filter": limit_set_display(self.skipped_commands),
            "Skipped External Files": limit_set_display(self.skipped_filenames),
            "Number of Violations": limit_set_display(
                [f"{key}:{entry}" for key, entry in self.number_of_violations.items()]
            ),
        }

    def add_analyzed_filename(self, file_path):
        self.analyzed_file_names.add(os.path.basename(file_path))

    def add_analyzed_translation_unit(self, file_path):
        self.analyzed_translation_units.add(os.path.basename(file_path))

    def add_ignored_translation_unit(self, file_path):
        self.ignored_translation_units.add(os.path.basename(file_path))

    def add_skipped_commands(self, file_path):
        self.skipped_commands.add(os.path.basename(file_path))

    def add_skipped_filename(self, file_path):
        self.skipped_filenames.add(os.path.basename(file_path))

    def add_number_of_violations(self, tu_name, violations_tuple):
        self.number_of_violations[os.path.basename(tu_name)] = violations_tuple

    def add_failed_translation_units(self, file_path):
        self.failed_translation_units.add(os.path.basename(file_path))


the_summary = Summary()
