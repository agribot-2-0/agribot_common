/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <cmath>

namespace common_functions
{

inline double radians(const double degrees)
{
  return degrees * M_PI / 180.0;
}

inline double degrees(const double radians)
{
  return radians * 180.0 / M_PI;
}

}  // namespace common_functions
