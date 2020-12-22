namespace a
{
namespace b  // TIDY_SAMO_NESTED_NAMESPACE
{

}
}  // namespace a

namespace c
{

}

namespace d
{
namespace e  // TIDY_SAMO_NESTED_NAMESPACE
{
namespace f  // TIDY_SAMO_NESTED_NAMESPACE
{

}

}  // namespace e

}  // namespace d

namespace
{
namespace g  // OK
{

}

}  // namespace

namespace
{
namespace h  // OK
{
namespace i  // TIDY_SAMO_NESTED_NAMESPACE
{

}

}  // namespace h

}  // namespace
