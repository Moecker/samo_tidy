from clang import cindex
import logging
from termcolor import colored
import platform
import sys


def setup_clang():
    """Sets up thee cindex.Config class which is of global state."""
    # TODO When executing test in parallel - for instance - we run into (unknown) problems.
    #      This results in flaky tests
    cindex.Config.loaded = False
    if platform.system() == "Linux":
        lib_location_file = "/usr/lib/llvm-10/lib/libclang-10.so"
        logging.info(colored("Searching libclang file in '%s'", attrs=["dark"]), lib_location_file)
        cindex.Config.set_library_file(lib_location_file)
    elif platform.system() == "Darwin":
        lib_location_path = "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib"
        logging.info(colored("Searching libclang path in '%s'", attrs=["dark"]), lib_location_path)
        cindex.Config.set_library_path(lib_location_path)
    elif platform.system() == "Windows":
        sys.exit("ERROR: Windows is not supported")
    else:
        sys.exit("ERROR: Unknown OS")
