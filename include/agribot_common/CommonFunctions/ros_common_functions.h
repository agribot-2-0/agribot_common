/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <ros/ros.h>
#include <string>

namespace ros_common_functions
{
template <class T>
inline T getRosParam(const std::string& parameter_name)
{
  std::string key;
  if (!ros::param::has(parameter_name))
  {
    throw parameter_name + " param not set.";
  }
  T value;
  ros::param::get(parameter_name, value);
  return value;
}

}  // namespace ros_common_functions
