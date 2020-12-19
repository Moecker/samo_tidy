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
    the_config = function_args

    # TODO Respect the log_file attribute
    logger.setup_logger(the_config.log_level)
    worker_id = multiprocessing.current_process()._identity[0]
    logging.debug("Spawning worker with id %s", worker_id)

    clang_setup.setup_clang()
    violations = facade_lib.apply_checkers_for_commands(commands[start:end], the_config)

    # TODO Return the violations
    return [summary.get_summary()]


def run_parallel(the_config, compdb):
    logging.info(colored("Using %d parallel worker(s)", attrs=["dark"]), the_config.workers)
    commands = compdb_parser.parse_compdb(compdb)
    wrapped_commands = wrap_commands(commands)

    logging.info(colored("Starting parallel tasks", attrs=["dark"]))
    all_summaries = parallel.execute_parallel(
        wrapped_commands, the_config.workers, single_run, function_args=(the_config)
    )
    return summary.merge(all_summaries)


def main():
    facade_lib.main(run_parallel)


if __name__ == "__main__":
    main()
