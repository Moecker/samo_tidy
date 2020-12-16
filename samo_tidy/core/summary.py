import os


class Summary:
    analyzed_file_names = set()
    analyzed_translation_units = set()
    ignored_translation_units = set()
    skipped_commands = set()
    skipped_filenames = set()


def limit_set_display(the_set):
    MAX_DISPLAY = 1
    list_to_show = list(the_set)[0:MAX_DISPLAY]
    remaining = len(the_set) - MAX_DISPLAY
    if remaining > 0:
        list_to_show.append(
            f"and {remaining} more",
        )

    return ", ".join(list_to_show)


def present():
    return {
        "Analyzed Files": limit_set_display(Summary.analyzed_file_names),
        "Analyzed Translation Units": limit_set_display(Summary.analyzed_translation_units),
        "Ignored Translation Units": limit_set_display(Summary.ignored_translation_units),
        "Skipped Commands": limit_set_display(Summary.skipped_commands),
        "Skipped Files": limit_set_display(Summary.skipped_filenames),
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
