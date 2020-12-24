#ifndef SIMPLE_SOURCE_INCLUDE_SIMPLE_SOURCE_H
#define SIMPLE_SOURCE_INCLUDE_SIMPLE_SOURCE_H

#include <cstdint>

int MyHeaderFunction();
inline int MyHeaderFunction()
{
    return 5;
}
std::uint8_t Function();

int Foo();
inline int Foo()
{
    std::uint8_t const a = 0u;
    return a;
}

#endif  // SIMPLE_SOURCE_INCLUDE_SIMPLE_SOURCE_H
