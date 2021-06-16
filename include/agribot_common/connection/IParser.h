/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/connection/Buffer.h>
#include <agribot_common/connection/IFrame.h>
#include <agribot_common/connection/IFrameFactory.h>
#include <agribot_common/connection/IParsingStrategy.h>

#include <cstdint>
#include <functional>
#include <memory>
#include <unordered_map>
#include <utility>
#include <vector>

class IParser
{
private:
  std::unique_ptr<IParsingStrategy> parsing_strategy_;
  std::unique_ptr<IFrameFactory> frame_factory_;
  std::unordered_map<uint64_t, std::vector<std::function<void(IFrame&)>>> callback_map_;
  void callCallbacks(uint64_t id, IFrame& frame);  // NOLINT(runtime/references)

public:
  IParser() = delete;
  ~IParser();
  void registerCallback(uint64_t id, const std::function<void(IFrame&)>& callback);
  void processBuffer(Buffer& buffer);  // NOLINT(runtime/references)
  virtual bool checkCrc(std::vector<uint8_t>::iterator begin_it) = 0;
  virtual uint64_t getId(std::vector<uint8_t>::iterator begin_it) = 0;
  virtual std::vector<std::pair<std::vector<uint8_t>::iterator, std::vector<uint8_t>::iterator>>
  split(Buffer& buffer) = 0;  // NOLINT(runtime/references)
};
