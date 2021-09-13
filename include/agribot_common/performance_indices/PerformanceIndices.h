/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <ros/ros.h>
#include <std_msgs/Float64.h>
#include <std_srvs/Trigger.h>

class IndicesCalculator
{
public:
  explicit IndicesCalculator(ros::NodeHandle* nh);
  void run();

private:
  std_msgs::Float64 iae_, itae_, ise_, itse_;
  void errorCallback(const std_msgs::Float64& msg);
  bool resetIndices(std_srvs::Trigger::Request& req, std_srvs::Trigger::Response& res);  // NOLINT (runtime/references)
  ros::Time start_time_;
  ros::Time stop_time_;
  ros::NodeHandle* nh_;
  ros::Subscriber error_subscriber_;
  ros::ServiceServer reset_service_;
  ros::Publisher iae_publisher_;
  ros::Publisher itae_publisher_;
  ros::Publisher ise_publisher_;
  ros::Publisher itse_publisher_;
};
