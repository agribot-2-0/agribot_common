#include <stdexcept>

namespace agribot_exceptions
{
// Uses concept of Inheriting constructors
// More information: https://en.cppreference.com/w/cpp/language/using_declaration
struct ParameterNotSet : public std::invalid_argument
{
  using invalid_argument::invalid_argument;
};

}  // namespace agribot_exceptions
