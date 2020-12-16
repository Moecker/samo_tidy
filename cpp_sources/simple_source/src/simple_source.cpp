#include <cstdint>
#include "simple_source.h"

uint8_t Function()
{
    int foo = MyHeaderFunction();
    return 0u + foo;
}

namespace a
{
    namespace b
    {

    }
} // namespace a
