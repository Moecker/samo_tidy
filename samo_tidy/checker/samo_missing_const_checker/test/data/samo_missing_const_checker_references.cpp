void Change(int& reference);
void UsedInFunctions();

void Change(int& reference)
{
    reference++;
}

void UsedInFunctions()
{
    int change_me;
    Change(change_me);
}
