/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_msgs/AgribotNavigationManagerResult.h>
#include <string_view>

namespace common_functions
{
std::string_view navigationManagerResultToString(agribot_msgs::AgribotNavigationManagerResult result)
{
  switch (result.result)
  {
    case result.NOACTION:
      return "NOACTION";
    case result.ACTIVE:
      return "ACTIVE";
    case result.PREEMPTED:
      return "PREEMPTED";
    case result.SUCCES:
      return "SUCCES";
    case result.ABORTED:
      return "ABORTED";
    case result.FAILED:
      return "FAILED";
    case result.RECALLED:
      return "RECALLED";
    case result.PAUSED:
      return "PAUSED";
    case result.COMPLETED:
      return "COMPLETED";
    default:
      return "result code unknown";
  }
}

}  // namespace common_functions
