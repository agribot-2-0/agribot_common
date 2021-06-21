/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <agribot_common/connection/IParser.h>

IParser::IParser(std::unique_ptr<IParsingStrategy> strategy, std::unique_ptr<IFrameFactory> factory)
  : parsing_strategy_(std::move(strategy)), frame_factory_(std::move(factory))
{
}

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
      frame->parse(begin_it, end_it, *parsing_strategy_);
      callCallbacks(id, frame.get());
    }
  }
}

void IParser::callCallbacks(uint64_t id, IFrame* frame)
{
  for (const auto& cb : callback_map_[id])
  {
    cb(*frame);
  }
}
