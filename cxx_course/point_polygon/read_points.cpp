#include "read_points.h"
#include <cstdio>
#include <fstream>
#include <iostream>

ReadPointsError check_file(const std::string &filename, int &n)
{
    double temp = 0;
    n = 0;
    std::ifstream file(filename);
    if (!file)
    {
        return ReadPointsError::THE_FILE_CANNOT_BE_OPENED;
    }
    while (true)
    {
        file >> temp;
        n++;
        if (file.fail())
        {
            return ReadPointsError::READING_FILE_IS_NOT_CORRECT;
        }
        if (file.eof())
        {
            break;
        }
    }

    if (!file)
    {
        return ReadPointsError::THE_FILE_CANNOT_BE_OPENED;
    }

    if (double tmp = 0; (file >> tmp, !file.fail()))
    {
        return ReadPointsError::READING_FILE_IS_NOT_CORRECT;
    }

    if (n % 2 != 0)
    {
        return ReadPointsError::THE_FILE_CONTAINS_AN_ODD_NUMBER_OF_POINTS;
    }
    n /= 2;
    if (n < 3)
    {
        return ReadPointsError::TOO_FEW_POINTS_TO_BUILD_A_POLYGON;
    }
    return ReadPointsError::SUCCESS;
}

ReadPointsError read_points(const std::string &filename, int n, double *x, double *y)
{
    std::ifstream file(filename);
    if (!file)
    {
        return ReadPointsError::THE_FILE_CANNOT_BE_OPENED;
    }
    for (int i = 0; i < n; i++)
    {
        file >> x[i] >> y[i];
        if (file.fail())
        {
            return ReadPointsError::READING_FILE_IS_NOT_CORRECT;
        }
    }
    if (double tmp = 0; (file >> tmp, !file.fail()))
    {
        return ReadPointsError::READING_FILE_IS_NOT_CORRECT;
    }
    if (!file.eof())
    {
        return ReadPointsError::READING_FILE_IS_NOT_CORRECT;
    }
    return ReadPointsError::SUCCESS;
}

std::string get_read_point_error_name(ReadPointsError err_info)
{
    switch (err_info)
    {
        case ReadPointsError::THE_FILE_CANNOT_BE_OPENED:
            return "The file cannot be opened";
        case ReadPointsError::READING_FILE_IS_NOT_CORRECT:
            return "Reading file is not correct";
        case ReadPointsError::THE_FILE_CONTAINS_AN_ODD_NUMBER_OF_POINTS:
            return "The file contains an odd number of points";
        case ReadPointsError::SUCCESS:
            return "No error";
        default:
            return "Unknown error"; 
    }
    return "Unknown error"; 
}