#pragma once // avoid double include of header

#include <string> // C++ standard header to work with strings (C++98 and above)

// For C++ it is highly reccomended to use enum class.
// It produces something like namespace, so constants are not in the global namespace.
// Also type control is better - it is not allowed to assign variables of different enum class without type cast.
enum class ParseErrors 
{
    INSUFFICIENT_ARGUMENTS = -3, // We may set values for all, but may set only for some of them or even for none of them
    TO_MUCH_ARGUMENTS = -2,
    NOT_A_NUMBER = -1,
    SUCCESS = 0
};

// If function returns error status we probably really want user to use it, so he is sure that obtained data is correct.
// To raise a compiler warning if function result is unused there is [[nodiscard]] mark in C++17 and later
[[nodiscard]] ParseErrors parse_arguments(int argc, char **argv, std::string &filename, double &x, double &y); // Function return error status

std::string get_error_name(ParseErrors err_info); // return string with error description fo given error status
