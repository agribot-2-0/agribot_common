/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <sensor_msgs/Image.h>

class IProcessor
{
private:
public:
  IProcessor() = default;
  virtual ~IProcessor() = default;
  IProcessor(const IProcessor& other) = delete;
  IProcessor(IProcessor&& other) = default;
  IProcessor& operator=(const IProcessor& other) = delete;
  IProcessor& operator=(IProcessor&& other) = default;

  virtual void process(double snapshot_time_s) = 0;
  virtual void addData(const sensor_msgs::Image& image) = 0;
};
