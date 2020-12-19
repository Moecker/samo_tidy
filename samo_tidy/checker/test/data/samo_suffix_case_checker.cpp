#include <cstdint>

std::uint8_t Function();
std::uint8_t Function()
{
    std::uint8_t variable1 = 0u;  // TIDY_SAMO_SUFFIX_CASE
    std::uint8_t variable2 = 0U;  // OK
    return variable1 + variable2;
}
