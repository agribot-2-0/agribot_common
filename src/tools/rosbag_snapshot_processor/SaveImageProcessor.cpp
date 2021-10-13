/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <agribot_common/tools/rosbag_snapshot_processor/SaveImageProcessor.h>

void SaveImageProcessor::process(double snapshot_time_s)
{
  static_cast<void>(snapshot_time_s);
  std::cout << "SaveImageProcessor at time: " << snapshot_time_s << std::endl;
}

void SaveImageProcessor::addData(const sensor_msgs::Image& image)
{
  static_cast<void>(image);
}
