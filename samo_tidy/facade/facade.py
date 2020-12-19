import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.core.summary as summary
import samo_tidy.facade.facade_lib as facade_lib

# TODO Rename file into "serial_facade"
def run_serial(the_config, compdb):
    commands = compdb_parser.parse_compdb(compdb)
    facade_lib.apply_checkers_for_commands(commands, the_config)
    return summary.get_summary()


def main():
    facade_lib.main(run_serial)


if __name__ == "__main__":
    main()
