from termcolor import colored
import logging
import multiprocessing

import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.core.summary as summary
import samo_tidy.facade.facade_lib as facade_lib
import samo_tidy.utils.clang_setup as clang_setup
import samo_tidy.utils.logger as logger
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
    start, end, commands, function_args = args
    files, log_level = function_args

    # TODO Respect the log_file attribute
    logger.setup_logger(log_level)
    worker_id = multiprocessing.current_process()._identity[0]
    logging.debug("Spawning worker with id %s", worker_id)

    clang_setup.setup_clang()
    facade_lib.run_all(commands[start:end], files)

    return [summary.get_summary()]


def run_parallel(compdb, log_level, workers, files=None):
    logging.info(colored("Using %d parallel worker(s)", attrs=["dark"]), workers)
    commands = compdb.getAllCompileCommands()
    wrapped_commands = wrap_commands(commands)
    all_summaries = parallel.execute_parallel(wrapped_commands, workers, single_run, function_args=(files, log_level))
    return summary.merge(all_summaries)


def main():
    facade_lib.main(run_parallel)


if __name__ == "__main__":
    main()
