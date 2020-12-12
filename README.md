# SAMO TIDY
A python based static code analysis engine

# Examples
## Run on a compilation database
`bazel run //samo_tidy/facade:run -- --compdb <WORKSPACE>/samo_tidy/samo_tidy/test/data`

## Dump AST
`bazel run //samo_tidy/utils:cindex_dump -- <WORKSPACE>/samo_tidy/samo_tidy/test/data/source_id1.cpp`

# Installation
## Mac
Get LLVM libraries `brew install llvm`

The library can be found in `/usr/local/opt/llvm/lib/libclang.dylib`

# Compilation Database
## Create compilation database for example CMake project
````
cd cpp_sources
mkdir build && cd build
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON ..
make
````

# Ressource
* https://github.com/pybee/seasnake/tree/master/seasnake
* https://github.com/jbcoe/clang_cpp_code_model