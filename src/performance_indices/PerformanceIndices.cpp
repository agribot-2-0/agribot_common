/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <agribot_common/performance_indices/PerformanceIndices.h>

void IndicesCalculator::errorCallback(const std_msgs::Float64& msg)
{
  stop = ros::Time::now();
  ros::Duration wait_ = stop - start;
  ise_.data += pow(msg.data, 2);
  iae_.data += abs(msg.data);
  itse_.data += pow(msg.data * wait_.toSec(), 2);
  itae_.data += abs(msg.data) * wait_.toSec();
  ise_publisher_.publish(ise_);
  iae_publisher_.publish(iae_);
  itse_publisher_.publish(itse_);
  itae_publisher_.publish(itae_);
  start = ros::Time::now();
}

void IndicesCalculator::run()
{
  ros::spin();
}

IndicesCalculator::IndicesCalculator(ros::NodeHandle* nh)
{
  nh_ = nh;
  ise_.data = 0;
  itse_.data = 0;
  itae_.data = 0;
  iae_.data = 0;
  error_subscriber_ = nh_->subscribe("/error", 1, &IndicesCalculator::errorCallback, this);
  ise_publisher_ = nh->advertise<std_msgs::Float64>(nh_->getNamespace() + "/ise", 1);
  itse_publisher_ = nh->advertise<std_msgs::Float64>(nh_->getNamespace() + "/itse", 1);
  iae_publisher_ = nh->advertise<std_msgs::Float64>(nh_->getNamespace() + "/iae", 1);
  itae_publisher_ = nh->advertise<std_msgs::Float64>(nh_->getNamespace() + "/itae", 1);
  start = ros::Time::now();
}
