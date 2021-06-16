/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <agribot_common/connection/IParser.h>

void IParser::registerCallback(uint64_t id, const std::function<void(IFrame&)>& callback)
{
  callback_map_[id].push_back(callback);
}

void IParser::processBuffer(Buffer& buffer)
{
  for (auto [begin_it, end_it] : split(buffer))
  {
    // TODO(olek) - notify about eventual errors
    if (checkCrc(begin_it))
    {
      auto id = getId(begin_it);
      auto frame = frame_factory_->createFrame(id);
      frame.parse(begin_it, end_it, *parsing_strategy_);
      callCallbacks(id, frame);
    }
  }
}

void IParser::callCallbacks(uint64_t id, IFrame& frame)
{
  for (const auto& cb : callback_map_[id])
  {
    cb(frame);
  }
}
