import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.core.summary as summary
import samo_tidy.facade.facade_lib as facade_lib


def run_serial(the_config, compdb):
    commands = compdb_parser.parse_compdb(compdb)
    facade_lib.apply_checkers_for_commands(commands, the_config)
    # TODO The global state of summary is hard to test
    # Returning the global summary object
    return summary.get_summary()


def main():
    facade_lib.main(run_serial)


if __name__ == "__main__":
    main()
