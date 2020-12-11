# SAMO TIDY
A python based static code analysis engine

# Examples
## Example run
`bazel run //samo_tidy/core:run -- --compdb ~/Github/samo_tidy/samo_tidy/test/data --verbose`

# Installation
## Mac
Get LLVM libraries `brew install llvm`

The library can be found in `/usr/local/opt/llvm/lib/libclang.dylib`

# Compilation Database
## Create compilation database for example CMake project
````
cd cpp_sources
mkdir build
cd build
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON ..
````
