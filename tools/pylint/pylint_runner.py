import argparse
import pylint.lint
import multiprocessing


def get_disabled_rules():
    return [
        "missing-module-docstring",
        "empty-docstring",
        "missing-function-docstring",
        "missing-class-docstring",
    ]


def run_lint(paths):
    disabled_rules = ",".join(get_disabled_rules())
    pylint_args = []
    pylint_args.extend(["-j", str(multiprocessing.cpu_count())])
    pylint_args.extend([f"--disable={disabled_rules}"])
    pylint_args.extend(paths)
    pylint.lint.Run(pylint_args)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--modules", nargs="+", help="List of modules to analyze", required=True)
    args = parser.parse_args()

    run_lint(args.modules)


if __name__ == "__main__":
    main()