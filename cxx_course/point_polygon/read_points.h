#pragma once

#include <string>


enum class ReadPointsError
{
    THE_FILE_CANNOT_BE_OPENED = -7,
    READING_FILE_IS_NOT_CORRECT,
    THE_FILE_CONTAINS_AN_ODD_NUMBER_OF_POINTS,
    TOO_FEW_POINTS_TO_BUILD_A_POLYGON,
    SUCCESS = 0
};


ReadPointsError check_file(const std::string &filename, int &n);

ReadPointsError read_points(const std::string &filename, int n, double *x, double *y);

std::string get_read_point_error_name(ReadPointsError err_info);
