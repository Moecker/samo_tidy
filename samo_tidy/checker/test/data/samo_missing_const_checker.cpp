int main()
{
    int value = 0;
    value = 1;

    int foo = 2;  // TIDY_SAMO_MISSING_CONST

    int combined = 3;
    combined += 4;

    return value + foo;
}
