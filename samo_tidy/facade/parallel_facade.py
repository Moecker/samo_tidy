import logging
import multiprocessing

import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.facade.facade_lib as facade_lib
import samo_tidy.utils.clang_setup as clang_setup
import samo_tidy.utils.parallel as parallel
import samo_tidy.utils.utils as utils


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


def single_run(args):
    clang_setup.setup_clang()

    start, end, commands = args

    for i in range(start, end):
        translation_unit = compdb_parser.parse_single_command(commands[i])
        facade_lib.run_for_translation_unit(translation_unit)
    return []


def run_parallel(compdb, files=None):
    commands = compdb.getAllCompileCommands()
    wrapped_commands = wrap_commands(commands)
    parallel.execute_parallel(wrapped_commands, multiprocessing.cpu_count() - 1, single_run)


def main():
    facade_lib.main(run_parallel)


if __name__ == "__main__":
    main()
