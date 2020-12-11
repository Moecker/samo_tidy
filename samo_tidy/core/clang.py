import clang
from clang import cindex
import logging

clang.cindex.Config.set_library_file("/usr/local/opt/llvm/lib/libclang.dylib")


def setup():
    pass


def load_compilation_db(directory):
    try:
        logging.info("Opening compilation database from directory '%s'", directory)
        compilation_database = clang.cindex.CompilationDatabase.fromDirectory(directory)
        return compilation_database
    except clang.cindex.CompilationDatabaseError as e:
        logging.error(e)
    return None


def parse_compilation_database(compilation_database):
    commands = compilation_database.getAllCompileCommands()
    for command in commands:
        print(command.filename)
        print(list(command.arguments))
        create_translation_unit(command.filename, list(command.arguments))


def create_translation_unit(source_file, args):
    index = cindex.Index.create()
    translation_unit = index.parse(source_file, args=[])


def parse_compilation_database2(compilation_database):
    index = cindex.Index.create()

    # Step 2: query compilation flags
    try:
        source_file_path = "/Users/q367607/Github/samo_tidy/cpp_sources/src/foo.cpp"
        file_args = compilation_database.getCompileCommands(source_file_path)
        print(file_args)
        translation_unit = index.parse(source_file_path, file_args)
        file_nodes = get_nodes_in_file(translation_unit.cursor, source_file_path)
        print([p.spelling for p in file_nodes])
    except clang.cindex.CompilationDatabaseError:
        print("Could not load compilation flags for", source_file_path)


def parse_compilation_database1(compdb):
    target_args = compdb.getCompileCommands("foo.cpp")
    index = clang.cindex.Index.create()
    tu = index.parse(target, args=target_args)
    print(target_args)


def foo():
    return "foo"
