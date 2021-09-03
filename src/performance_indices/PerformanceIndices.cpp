/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <agribot_common/performance_indices/PerformanceIndices.h>

void IndicesCalculator::errorCallback(const std_msgs::Float64& msg)
{
  stop = ros::Time::now();
  ros::Duration wait_ = stop - start;
  start = ros::Time::now();
  ise_.data += pow(msg.data * wait_.toSec(), 2);
  iae_.data += abs(msg.data * wait_.toSec());
  itse_.data += pow(msg.data * pow(wait_.toSec(), 2), 2);
  itae_.data += abs(msg.data) * pow(wait_.toSec(), 2);
  ise_publisher_.publish(ise_);
  iae_publisher_.publish(iae_);
  itse_publisher_.publish(itse_);
  itae_publisher_.publish(itae_);
}

void IndicesCalculator::run()
{
  ros::spin();
}

IndicesCalculator::IndicesCalculator(ros::NodeHandle* nh)
{
  nh_ = nh;
  error_subscriber_ = nh_->subscribe("/error", 1, &IndicesCalculator::errorCallback, this);
  reset_service_ =
      nh_->advertiseService(nh_->getNamespace() + "/reset_performance_indices", &IndicesCalculator::resetIndices, this);
  ise_publisher_ = nh->advertise<std_msgs::Float64>(nh_->getNamespace() + "/ise", 1);
  itse_publisher_ = nh->advertise<std_msgs::Float64>(nh_->getNamespace() + "/itse", 1);
  iae_publisher_ = nh->advertise<std_msgs::Float64>(nh_->getNamespace() + "/iae", 1);
  itae_publisher_ = nh->advertise<std_msgs::Float64>(nh_->getNamespace() + "/itae", 1);
  ise_.data = 0;
  iae_.data = 0;
  itse_.data = 0;
  itae_.data = 0;
  start = ros::Time::now();
}

bool IndicesCalculator::resetIndices(std_srvs::Trigger::Request& req,   // NOLINT (runtime/references)
                                     std_srvs::Trigger::Response& res)  // NOLINT (runtime/references)

{
  static_cast<void>(req);
  ise_.data = 0;
  iae_.data = 0;
  itse_.data = 0;
  itae_.data = 0;
  start = ros::Time::now();
  res.success = true;
  return true;
}
