/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */
#include <ros/ros.h>
#include <agribot_common/performance_indices/PerformanceIndices.h>

int main(int argc, char** argv)
{
  ros::init(argc, argv, "performance_indices_node");
  ros::NodeHandle nh("~");
  IndicesCalculator calc(&nh);
  Calc.run();
}
