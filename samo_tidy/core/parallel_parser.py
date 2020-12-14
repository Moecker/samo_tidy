class TranslationUnitWrapper:
    def __init__(self, tu):
        self.tu = tu

    def __getstate__(self):
        pass

    def __setstate__(self):
        pass


def parse_from_commands(args):
    start, end, commands = args
    translation_units = []

    for i in range(start, end):
        translation_unit = parse_single_command(command)
        translation_units.append(translation_unit)
    return translation_units


def parallel_parse_compdb(compdb):
    commands = compdb.getAllCompileCommands()

    translation_units = []
    number_of_skipped_files = 0

    # TODO Does not work: ValueError: ctypes objects containing pointers cannot be pickled
    translation_units = utils.parallel(commands, 4, parse_from_commands)
    return translation_units
