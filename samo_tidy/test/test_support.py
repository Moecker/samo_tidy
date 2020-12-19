import logging
import os
import shutil
import sys
import tempfile
import unittest

import samo_tidy.utils.clang_setup as clang_setup
import samo_tidy.utils.logger as logger
import samo_tidy.utils.utils as utils


def set_arguments(arguments):
    sys.argv = [sys.argv[0]]
    sys.argv.extend(arguments)


# Control the verbosity of the tests
def get_default_log_level_for_tests():
    return "debug"


def default_test_setup():
    logger.setup_logger(get_default_log_level_for_tests())
    clang_setup.setup_clang()
    unittest.main()


def make_file_string(the_list):
    return "\n".join(the_list) + "\n"


def is_absolute_path(desired_file):
    return os.path.basename(desired_file) != desired_file


def create_tempfile(content, desired_file=None):
    the_string = make_file_string(content)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        if not desired_file:
            desired_name = tmp.name + ".cpp"
        elif not is_absolute_path(desired_file):
            desired_name = desired_file
        else:
            os.makedirs(os.path.dirname(desired_file), exist_ok=True)
            desired_name = desired_file
        logging.debug("Writing file to '%s'", tmp.name)
        with open(tmp.name, "w") as f:
            f.write(the_string)
        shutil.copy(tmp.name, desired_name)
        utils.debug_file_content(desired_name)
    return desired_name
