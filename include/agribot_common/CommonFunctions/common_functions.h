/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <cmath>

namespace common_functions
{

inline double degreesToRadians(const double degrees)
{
  return degrees * M_PI / 180;
}

inline double radiansToDegrees(const double radians)
{
  return radians * 180 / M_PI;
}

}  // namespace common_functions
