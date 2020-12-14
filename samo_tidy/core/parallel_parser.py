import samo_tidy.utils.utils as utils

import samo_tidy.core.compdb_parser as compdb_parser


class TranslationUnitWrapper:
    def __init__(self):
        pass


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


def wrap_translation_unit(translation_unit):
    wrapped_translation_unit = TranslationUnitWrapper()
    return wrapped_translation_unit


def parse_from_commands(args):
    start, end, commands = args
    translation_units = []

    # We are in a multiprocessing environment which does not know about the global state (assumed)
    utils.setup_clang()

    for i in range(start, end):
        translation_unit = compdb_parser.parse_single_command(commands[i])
        wrapped_translation_unit = wrap_translation_unit(translation_unit)
        translation_units.append(wrapped_translation_unit)
    return translation_units


def parallel_parse_compdb(compdb):
    commands = compdb.getAllCompileCommands()
    wrapped_commands = wrap_commands(commands)

    translation_units = []
    number_of_skipped_files = 0

    # TODO Does not work: ValueError: ctypes objects containing pointers cannot be pickled
    translation_units = utils.parallel(wrapped_commands, 4, parse_from_commands)
    return translation_units
