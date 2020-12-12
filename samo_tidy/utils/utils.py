import logging
from pprint import pformat
import clang
from clang import cindex


def setup_clang():
    cindex.Config.set_library_file("/usr/local/opt/llvm/lib/libclang.dylib")


def debug_file_content(file_path):
    with open(file_path) as f:
        logging.debug("File %s looks like: %s", file_path, pformat(f.readlines()))
