/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/connection/IFrame.h>

#include <memory>

class IFrameFactory
{
public:
  virtual ~IFrameFactory() = default;
  virtual std::unique_ptr<IFrame> createFrame(uint64_t id) = 0;

protected:
  IFrameFactory() = default;
  IFrameFactory(const IFrameFactory& other) = default;
  IFrameFactory(IFrameFactory&& other) = default;
  IFrameFactory& operator=(const IFrameFactory& other) = default;
  IFrameFactory& operator=(IFrameFactory&& other) = default;
};
