# Samo Tidy
![samo_tidy](ressources/samo_tidy.jpg)

A python based static code analysis engine.

Goal of this project is to provide a simple framework to write own static code analysis checks based on the Abstract Syntax Tree (AST) provided by the LLVM libclang tooling.

The tool takes a compilation database (`compile_commands.json`) which can be generated with CMake or Bazel.

# Usage (Samo Tidy)
Check the help output
```
bazel run //samo_tidy/facade:run -- --help
```
Results in
```
  -h, --help            show this help message and exit
  --compdb COMPDB       Directory which contains the 'compile_comands.json' file
  --files FILES [FILES ...]
                        List of files from compdb to be analyzed. Treated as substrings. Default: All files
                        Example: '--files .cpp' would match every file which has '.cpp' in its name
  --checkers CHECKERS [CHECKERS ...]
                        List of checkers to be applied. Treated as substrings. Default: All checkers
                        Example: '--checkers SAMO_TIDY_SUFFIX' would apply every checker which has 'SAMO_TIDY_SUFFIX' in its name
  --fix                 Apply fixes. Caution! This will change source files
  --log_file LOG_FILE   Full path to a log file
  --log_level LOG_LEVEL
                        Log level. One of {DEBUG, INFO, WARN, ERROR, CRITICAL}. Default: INFO
  --workers [1-12]      Number of workers for parallel execution. Default: Number of CPUs which is 12
```

# Usage (CIndex Dump)
Check the help output
```
bazel run //samo_tidy/dump:cindex_dump -- --help
```
Results in
```
  -h, --help            show this help message and exit
  --file FILE           Filepath to be analyzed
  --compdb COMPDB       Compilation Database for detailed build instructions
  --arguments ARGUMENTS [ARGUMENTS ...]
                        Arguments for parsing the file (such as -I flags)
  --diagnostics_only    Only show diagnostics
  --details             Show more details per node
  --max_depth MAX_DEPTH
                        Limit cursor expansion to depth
```

# Examples
## Run on a example compilation database
### Serial execution:
Run on all files in a compdb
```
bazel run //samo_tidy/facade:run -- --compdb /path/to/compdb/directory
```

Only on selected files in a compdb
```
bazel run //samo_tidy/facade:run -- --compdb /path/to/compdb/directory --files source_id1.cpp source_id2.cpp
```

### Parallel execution:
Run in parallel on all files in a compdb:
```
bazel run //samo_tidy/facade:run_parallel -- --compdb /path/to/compdb/directory
```

## Dump AST for an example file
Dump a file w/o arguments
```
bazel run //samo_tidy/dump:cindex_dump -- --file <WORKSPACE>/samo_tidy/samo_tidy/test/data/source_id1.cpp
```

Dump a file with arguments from compdb
```
bazel run //samo_tidy/dump:cindex_dump -- --file source_id1.cpp --compdb /path/to/compdb/directory
```

# Tests
## Execute all project tests
```
bazel test /...
```

# Installation
## Mac
Use XCode. The library can be found in `/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib`

Or get LLVM libraries: `brew install llvm`. The library can be found in `/usr/local/opt/llvm/lib/libclang.dylib`

## Linux
Install via apt: `sudo apt-get install libclang-dev`. The library can be found `/usr/lib/llvm-10/lib/libclang-10.so`

# Compilation Database
## Create compilation database for example CMake project
```
cd cpp_sources
mkdir build && cd build
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON ..
make
```

# Clang-Tidy
Run clang-tidy
```
bazel run //tools/clang_tidy:run-clang-tidy -- -p /path/to/compdb/directory -header-filter=".*"
```

# Ressources
* https://github.com/llvm/llvm-project/tree/main/clang/bindings/python
* https://github.com/llvm/llvm-project/blob/main/clang-tools-extra/clang-tidy
