class ExternClass;  // OK

class FirstClass  // TIDY_SAMO_MULTIPLE_CLASSES
{
};

class SecondClass  // TIDY_SAMO_MULTIPLE_CLASSES
{
  private:
    FirstClass a_;

  public:
    FirstClass GetFirstClass() { return a_; }
};
