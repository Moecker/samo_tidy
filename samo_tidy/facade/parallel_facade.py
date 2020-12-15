import logging
import argparse
import time
import multiprocessing

import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.facade.facade_lib as facade_lib
import samo_tidy.utils.utils as utils
import samo_tidy.checker.clang_warning_checker as clang_warning_checker


def single_run(args):
    utils.setup_clang()
    start, end, commands = args

    for i in range(start, end):
        translation_unit = compdb_parser.parse_single_command(commands[i])
        if translation_unit:
            clang_warning_checker.check_for_clang_warnings(translation_unit)
    return []


class CompileCommandsWrapper:
    def __init__(self, filename, directory, arguments):
        self.filename = filename
        self.directory = directory
        self.arguments = arguments


def wrap_commands(commands):
    wrapped_commands = []
    for command in commands:
        wrapped_command = CompileCommandsWrapper(command.filename, command.directory, list(command.arguments))
        wrapped_commands.append(wrapped_command)
    return wrapped_commands


def run_parallel(compdb, files=None):
    commands = compdb.getAllCompileCommands()
    wrapped_commands = wrap_commands(commands)
    utils.parallel(wrapped_commands, multiprocessing.cpu_count() - 1, single_run)


def main():
    facade_lib.main(run_parallel)


if __name__ == "__main__":
    main()
