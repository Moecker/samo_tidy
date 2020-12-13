# SAMO TIDY
A python based static code analysis engine

# Test
### Default
`bazel test /...`

### Verbose
`bazel test /... --test_output all`

# Examples
### Run on a compilation database
`bazel run //samo_tidy/facade:run -- --compdb <WORKSPACE>/samo_tidy/samo_tidy/test/data`

### Dump AST
`bazel run //samo_tidy/utils:cindex_dump -- <WORKSPACE>/samo_tidy/samo_tidy/test/data/source_id1.cpp`

# Installation
### Mac
Use XCode. The library can be found in `/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib`

Or get LLVM libraries: `brew install llvm`. The library can be found in `/usr/local/opt/llvm/lib/libclang.dylib`

### Linux
Install via apt: `sudo apt-get install libclang-dev`. The library can be found `/usr/lib/llvm-10/lib/libclang-10.so`

# Compilation Database
### Create compilation database for example CMake project
````
cd cpp_sources
mkdir build && cd build
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON ..
make
````

# Ressources
* https://github.com/llvm-mirror/clang/tree/master/bindings/python
* https://github.com/pybee/seasnake/tree/master/seasnake
* https://github.com/jbcoe/clang_cpp_code_model
