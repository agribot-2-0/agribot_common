/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <agribot_common/tools/rosbag_snapshot_processor/RosbagSnapshotProcessor.h>

#include <agribot_common/tools/rosbag_snapshot_processor/SaveImageProcessor.h>
#include <iostream>

RosbagSnapshotProcessor::RosbagSnapshotProcessor(const std::string& bag_path)
{
  bag_.open(bag_path, rosbag::bagmode::Read);
}

std::vector<std::string> RosbagSnapshotProcessor::getTopicsList()
{
  std::vector<std::string> topics;

  for (const auto& [topic, processor] : processors_map_)
  {
    static_cast<void>(processor);
    topics.push_back(topic);
  }

  return topics;
}

void RosbagSnapshotProcessor::registerProcessor(const std::string& topic, std::unique_ptr<IProcessor> processor)
{
  processors_map_[topic].push_back(std::move(processor));
  std::cout << "Registering " << topic << std::endl;
}

void RosbagSnapshotProcessor::prepareData()
{
  auto topics = getTopicsList();

  std::cout << "Topics list\n";
  for (const auto& t : topics)
  {
    std::cout << t << std::endl;
  }

  // TODO - get tf buffer

  // TODO - split data loading and snapshot taking (closests message selection_ - allows to make multiple snapshots
  // after one load

  std::cout << "\n\nTopics found\n";

  for (const auto& msg : rosbag::View(bag_, rosbag::TopicQuery(topics)))
  {
    if (processors_map_.find(msg.getTopic()) != processors_map_.end())
    {
      std::cout << msg.getTopic() << std::endl;
      for (const auto& processor : processors_map_[msg.getTopic()])
      {
        static_cast<void>(processor);
        // TODO - maybe tmeplated addData in IProcessor and template specializations in specific processors?
        // Message type registered with processor? or held by processor?
        processor->addData(*(msg.instantiate<sensor_msgs::Image>()));
        // TODO - add tfbuffer to processor
      }
    }
  }
}

bool RosbagSnapshotProcessor::makeSnapshot(double snapshot_time_s, bool print_debug_info)
{
  static_cast<void>(print_debug_info);

  for (const auto& kv : processors_map_)
  {
    for (const auto& processor : kv.second)
    {
      processor->process(snapshot_time_s);
    }
  }

  // TODO
  static_cast<void>(snapshot_time_s);

  // TODO - Find closests messages for each topic

  // TODO - process closest message
  // for (const auto& processor : processors_map_[msg.getTopic()])
  // {
  //   // TODO - process message
  // }

  return true;
}

int main()
{
  std::string bag_path = "/home/olek/agribot/logs/08_2021/11_08_2021/begin_end_line_v1.bag";

  try
  {
    RosbagSnapshotProcessor snapshot_processor(bag_path);
    snapshot_processor.registerProcessor("/zed2_node/rgb/image_rect_color",
                                         std::move(std::make_unique<SaveImageProcessor>()));
    // TODO - register processors

    // Prepare data for snapshot taking
    snapshot_processor.prepareData();

    // Make multiple snapshots
    snapshot_processor.makeSnapshot(10.0, true);
    snapshot_processor.makeSnapshot(20.0, true);
    snapshot_processor.makeSnapshot(30.0, true);
  }
  catch (const rosbag::BagException& e)
  {
    std::cerr << e.what() << '\n';
  }

  return 0;
}
