import os


class Summary:
    analyzed_translation_units = set()
    analyzed_file_names = set()

    def __repr__(self):
        return {
            "files": Summary.files,
        }

    def __str__(self):
        return "Summary(files=" + Summary.files + ")"


def present():
    return {
        "Analyzed Translation Units": Summary.analyzed_translation_units,
        "Analyzed Files": Summary.analyzed_file_names,
    }


def add_translation_unit(file_path):
    Summary.analyzed_translation_units.add(os.path.basename(file_path))


def add_filename(file_path):
    Summary.analyzed_file_names.add(os.path.basename(file_path))
