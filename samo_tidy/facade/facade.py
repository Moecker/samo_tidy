import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.core.summary as summary
import samo_tidy.facade.facade_lib as facade_lib


def run_serial(compdb, log_level, workers, files):
    commands = compdb_parser.parse_compdb(compdb)
    facade_lib.run_all(commands, files)
    return summary.get_summary()


def main():
    facade_lib.main(run_serial)


if __name__ == "__main__":
    main()
