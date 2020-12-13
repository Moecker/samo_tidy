def __translation_unit_basename_and_extension(translation_unit_name):
    from os.path import splitext, basename

    filename, extension = splitext(translation_unit_name)
    bname = basename(translation_unit_name)
    return bname, extension


def __swap_target(source_file, target_name):
    import os.path as pathutil
    import shutil
    import massedit
    import tempfile

    target_directory = tempfile.TemporaryDirectory()
    destination_file = pathutil.join(target_directory.name, target_name)
    shutil.copyfile(source_file, destination_file)
    massedit.edit_files([destination_file], ["re.sub(r'^#include','//#include',line)"], dry_run=False)
    return destination_file


def __compute_expected_name(classes, translation_unit_name):
    import re

    basename, extension = __translation_unit_basename_and_extension(translation_unit_name)
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    computed_name = pattern.sub("_", classes[0]).lower()
    computed_name += extension
    return computed_name, basename


def __check_one_class_per_file(tu, target):
    errors = []
    classes = []
    target_name, text = __translation_unit_basename_and_extension(target)
    if text == ".cpp":
        target = __swap_target(target, target_name)

    for token in tu.cursor.walk_preorder():
        if token.kind == CursorKind.CLASS_DECL:
            classes.append(token.spelling)
        elif token.kind == CursorKind.TRANSLATION_UNIT:
            translation_unit_name = token.spelling

    if len(classes) != 0:
        computed_name, basename = __compute_expected_name(classes, translation_unit_name)
        if computed_name != basename:
            errors.append(
                "FileNameMismatchException: " + target + " (expected: " + basename + " current: " + computed_name + ")"
            )

        if len(classes) > 1:
            errors.append("MultipleClassesWithinTranslationUnitException: " + target_name + " -- " + str(classes))
    classes = []
    for token in tu.cursor.walk_preorder():
        if token.kind == CursorKind.CLASS_DECL:
            classes.append(token.spelling)
        elif token.kind == CursorKind.TRANSLATION_UNIT:
            translation_unit_name = token.spelling

    if len(classes) != 0:
        computed_name, basename = __compute_expected_name(classes, translation_unit_name)
        if computed_name != basename:
            errors.append(
                "FileNameMismatchException: " + target + " (expected: " + basename + " current: " + computed_name + ")"
            )

        if len(classes) > 1:
            errors.append("MultipleClassesWithinTranslationUnitException: " + target_name + " -- " + str(classes))
    return errors
