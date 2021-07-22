/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/connection/buffer/Buffer.h>
#include <agribot_common/connection/frame/IFrame.h>
#include <agribot_common/connection/frame/IFrameFactory.h>
#include <agribot_common/connection/parsing_strategy/IParsingStrategy.h>

#include <cstdint>
#include <functional>
#include <memory>
#include <unordered_map>
#include <utility>
#include <vector>

class IParser
{
public:
  using Callback = std::function<void(IFrame&)>;

  IParser() = default;
  virtual ~IParser() = default;
  IParser(const IParser& other) = delete;
  IParser(IParser&& other) = delete;
  IParser& operator=(const IParser& other) = delete;
  IParser& operator=(IParser&& other) = delete;

  virtual void splitPacketBufferToFrameBuffers(Buffer& packet_buffer) = 0;  // NOLINT(runtime/references)
  virtual bool haveFrameBufferToParse() const = 0;
  virtual void parseFrameBuffer() = 0;
  virtual void registerCallback(uint64_t id, const Callback& callback) = 0;
};
