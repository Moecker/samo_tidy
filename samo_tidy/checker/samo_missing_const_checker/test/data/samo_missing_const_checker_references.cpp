void Change(int& reference, const int& const_reference, int by_value);
int NoChange(int& value);
void UsedInFunctions();

void Change(int& reference, const int& const_reference, int by_value)
{
    reference++;
    reference += const_reference;
    reference = by_value;
}

int NoChange(int& value)
{
    return value + 1;
}

void UsedInFunctions()
{
    int change_me = 0;           // OK
    int do_not_change_me = {1};  // TIDY_SAMO_MISSING_CONST
    int by_value{2};             // TIDY_SAMO_MISSING_CONST
    Change(change_me, do_not_change_me, by_value);

    int not_changed = 3;  // OK (TODO This is actually wrong)
    NoChange(not_changed);
}
