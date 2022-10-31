#include "parse_arguments.h" // As always, it is highly recommended to include header with function declaration to file with its implementation
#include <sstream> // C++ standard header to manpulate with string streams (C++98 and above)
#include <cstdio> // C++ standard header to include C standard header <stdio.h> for input/output manipulations (C++98 and above)
                  // It is not recommended to mix usage of C++ streams and C stdio.
                  // But in this file we do this to show how to do the same operation with both approaches.

ParseErrors parse_arguments(int argc, char **argv, std::string &filename, double &x, double &y)
{
    // Return corresponding errors if number of arguments is wrong
    if (argc < 4)
    {
        return ParseErrors::INSUFFICIENT_ARGUMENTS;
    }
    if (argc > 4)
    {
        return ParseErrors::TO_MUCH_ARGUMENTS;
    }

    // Set C++ string (std::string) to C-style string (char *)
    filename = std::string(argv[1]);
    
    // Initialize input string stream with C-style string (also possible to initialize with C++ string)
    // This allow to read data of this string as from any other stream such as std::cin
    std::istringstream iss(argv[2]);

    // Read from stream
    iss >> x;

    // In single if we: check that read from string was successfull, perform C-like read from another string and check if that read was also successfull.
    if (iss.fail() || (sscanf(argv[3], "%lf", &y) != 1))
    {
        return ParseErrors::NOT_A_NUMBER; // If any of them is not successfull return corresponding error.
    }
    return ParseErrors::SUCCESS; // If everything was OK, return corresponding error status.
}

std::string get_error_name(ParseErrors err_info)
{
    switch (err_info) // Simple switch returning error description depending on error status
                      // Breaks can be omitted as we have return in each case
    {
        case ParseErrors::INSUFFICIENT_ARGUMENTS:
            return "Not enough arguments";
        case ParseErrors::TO_MUCH_ARGUMENTS:
            return "To much arguments";
        case ParseErrors::NOT_A_NUMBER:
            return "Can not convert input argument to double";
        case ParseErrors::SUCCESS:
            return "No error";
        default:
            return "Unknown error"; // Should never go here, but better to have this for the case we changes our enum class
    }
    return "Unknown error"; // We will never reach this statement.
                            // But from point of view of many compilers function should return something even if none of switch cases is selected.
                            // Otherwise compiler raise a warning.
                            // To avoid this warning we put dummy return statement at the end of function
}
