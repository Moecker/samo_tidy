import os


class Summary:
    analyzed_file_names = set()
    analyzed_translation_units = set()
    ignored_translation_units = set()
    skipped_commands = set()
    skipped_filenames = set()


def present():
    return {
        "Analyzed Files": Summary.analyzed_file_names,
        "Analyzed Translation Units": Summary.analyzed_translation_units,
        "Ignored Translation Units": Summary.ignored_translation_units,
        "Skipped Commands": Summary.skipped_commands,
        "Skipped Files": Summary.skipped_filenames,
    }


def add_filename(file_path):
    Summary.analyzed_file_names.add(os.path.basename(file_path))


def add_translation_unit(file_path):
    Summary.analyzed_translation_units.add(os.path.basename(file_path))


def add_ignored_translation_unit(file_path):
    Summary.ignored_translation_units.add(os.path.basename(file_path))


def add_skipped_commands(file_path):
    Summary.skipped_commands.add(os.path.basename(file_path))


def add_skipped_filename(file_path):
    Summary.skipped_filenames.add(os.path.basename(file_path))
