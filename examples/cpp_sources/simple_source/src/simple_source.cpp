#include "simple_source.h"
#include <cstdint>

uint8_t Function()
{
    int const foo = MyHeaderFunction();
    return 0U + static_cast<uint8_t>(foo);
}

