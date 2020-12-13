import clang
from clang.cindex import CursorKind, Config
import sys
import argparse
import logging


def __configure_logger(logging_level=logging.DEBUG):
    logging.basicConfig(level=logging_level, format="%(levelname)s: %(message)s", datefmt="%H:%M:'%s'")


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


def __load_clang_db(db_directory):
    clangdb = clang.cindex.CompilationDatabase.fromDirectory(db_directory)
    return clangdb


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


def __check_for_file(target, compdb):
    errors = []
    index = clang.cindex.Index.create()
    try:
        # This does not work
        #   target_args = compdb.getCompileCommands(target)
        #   tu = index.parse(target, args=target_args)
        tu = index.parse(target)
        errors = __check_one_class_per_file(tu, target)
    except clang.cindex.TranslationUnitLoadError as e:
        raise e
    return errors


def check_files(compile_db_path, files):
    try:
        compdb = __load_clang_db(compile_db_path)
    except clang.cindex.CompilationDatabaseError as e:
        print(e)
    if files:
        # go through files
        for target in files:
            errors = __check_for_file(target, compdb)
            if len(errors) > 0:
                raise Exception("\n" + "\n".join(errors))
    else:
        # all files in compile db
        commands = compdb.getAllCompileCommands()
        for command in commands:
            if "external/" in command.filename:
                logging.debug("Skipping: '%s'", command.filename)
                continue
            logging.info("Checking file: '%s'", command.filename)
            errors = __check_for_file(command.filename, compdb)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--files", nargs="+")
    args = parser.parse_args()
    __configure_logger(logging.INFO)
    Config.set_library_file("/usr/lib/llvm-8/lib/libclang.so.1")
    if args.db:
        # create temporary directory
        check_files(args.db, args.files)