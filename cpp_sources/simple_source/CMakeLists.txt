file(GLOB SRC_FILES src/*.cpp)
add_library (SimpleSource ${SRC_FILES})
target_include_directories (SimpleSource PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
