int main()
{
    int value = 0;  // OK
    value = 1;

    int foo = 2;  // TIDY_SAMO_MISSING_CONST

    int combined = 3;  // OK
    combined += 4;

    int bla = {5};  // TIDY_SAMO_MISSING_CONST
    int bar = bla;  // OK
    bar -= value;

    const int readonly{5};            // OK
    const float readonly_flt = 3.4f;  // OK

    constexpr float solid = 5.7F;  // OK

    auto car = solid;  // TIDY_SAMO_MISSING_CONST
    auto see{5};       // TIDY_SAMO_MISSING_CONST

    const int using_ints = value + foo + bar + readonly + see;  // OK
    float using_floats = readonly_flt + solid + car;            // TIDY_SAMO_MISSING_CONST

    const int all_combined = using_ints + static_cast<int>(using_floats);  // OK

    return all_combined;
}
