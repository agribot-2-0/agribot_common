/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <rosbag/bag.h>
#include <rosbag/view.h>

#include <algorithm>
#include <memory>
#include <string>
#include <unordered_map>

#include <agribot_common/tools/rosbag_snapshot_processor/IProcessor.h>

class RosbagSnapshotProcessor
{
private:
  rosbag::Bag bag_;
  std::unordered_map<std::string, std::vector<std::unique_ptr<IProcessor>>> processors_map_;
  std::vector<std::string> getTopicsList();

public:
  RosbagSnapshotProcessor() = delete;
  RosbagSnapshotProcessor(const std::string& bag_path);
  void registerProcessor(const std::string& topic, std::unique_ptr<IProcessor> processor);
  void prepareData();
  bool makeSnapshot(double snapshot_time_s, bool print_debug_info = false);
  bool close();
};
