/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/connection/frame/IFrame.h>

#include <memory>

class IFrameFactory
{
public:
  IFrameFactory() = default;
  virtual ~IFrameFactory() = default;
  IFrameFactory(const IFrameFactory& other) = delete;
  IFrameFactory(IFrameFactory&& other) = delete;
  IFrameFactory& operator=(const IFrameFactory& other) = delete;
  IFrameFactory& operator=(IFrameFactory&& other) = delete;

  virtual std::unique_ptr<IFrame> createFrame(uint64_t id) const = 0;
};
