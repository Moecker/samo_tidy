#include "simple_source.h"
#include <cstdint>

uint8_t Function()
{
    int foo = MyHeaderFunction();
    return 0u + static_cast<uint8_t>(foo);
}

