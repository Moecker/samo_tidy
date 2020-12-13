import unittest
import logging
import tempfile
import shutil

from samo_tidy.utils.utils import setup_clang
from samo_tidy.utils.utils import debug_file_content


def default_test_setup():
    logging.basicConfig(level=logging.DEBUG)
    setup_clang()
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
        debug_file_content(desired_name)
    return desired_name
