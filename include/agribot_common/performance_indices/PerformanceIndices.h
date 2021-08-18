/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <ros/ros.h>
#include <std_msgs/Float64.h>

class IndicesCalculator
{
public:
  explicit IndicesCalculator(ros::NodeHandle* nh);
  std_msgs::Float64 iae_, itae_, ise_, itse_;
  void errorCallback(const std_msgs::Float64& msg);
  void run();

private:
  ros::Time start;
  ros::Time stop;
  ros::NodeHandle* nh_;
  ros::Subscriber error_subscriber_;
  ros::Publisher iae_publisher_;
  ros::Publisher itae_publisher_;
  ros::Publisher ise_publisher_;
  ros::Publisher itse_publisher_;
};
