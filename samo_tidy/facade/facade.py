import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.core.summary as summary
import samo_tidy.facade.facade_lib as facade_lib


def apply_checkers_for_translation_units(translation_units):
    for translation_unit in translation_units:
        facade_lib.run_for_translation_unit(translation_unit)


def run_serial(compdb, files=None):
    translation_units = compdb_parser.parse_compdb(compdb, files)
    apply_checkers_for_translation_units(translation_units)


def main():
    facade_lib.main(run_serial)


if __name__ == "__main__":
    main()
