/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <sensor_msgs/Image.h>

#include <agribot_common/tools/rosbag_snapshot_processor/IProcessor.h>

class SaveImageProcessor : public IProcessor
{
private:
  std::vector<sensor_msgs::Image> images_;

public:
  SaveImageProcessor() = default;
  void process(double snapshot_time_s) override;
  void addData(const sensor_msgs::Image& image);
};
