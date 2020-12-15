from clang import cindex
import logging
import platform
import sys


def setup_clang():
    # The cindex.Config class is of global state.
    # TODO When executing test in parallel - for instance - we run into problems.
    cindex.Config.loaded = False
    if platform.system() == "Linux":
        lib_location_file = "/usr/lib/llvm-10/lib/libclang-10.so"
        logging.info("Searching libclang file in '%s'", lib_location_file)
        cindex.Config.set_library_file(lib_location_file)
    elif platform.system() == "Darwin":
        lib_location_path = "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib"
        logging.info("Searching libclang path in '%s'", lib_location_path)
        cindex.Config.set_library_path(lib_location_path)
    elif platform.system() == "Windows":
        sys.exit("Windows is not supported")
    else:
        sys.exit("Unknown OS")
