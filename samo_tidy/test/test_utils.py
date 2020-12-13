import unittest
import logging
import tempfile
import shutil

import samo_tidy.utils.utils as utils


def default_test_setup():
    logging.basicConfig(level=logging.DEBUG)
    utils.setup_clang()
    unittest.main()


def make_file_string(the_list):
    return "\n".join(the_list) + "\n"


def create_temp_file_for(content):
    the_string = make_file_string(content)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        desired_name = tmp.name + ".cpp"
        logging.debug("Writing file to: '%s'", tmp.name)
        with open(tmp.name, "w") as f:
            f.write(the_string)
        shutil.copy(tmp.name, desired_name)
        utils.debug_file_content(desired_name)
    return desired_name
