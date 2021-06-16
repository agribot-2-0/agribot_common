/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/connection/IFrame.h>

class IFrameFactory
{
public:
  IFrameFactory() = default;
  ~IFrameFactory() = default;
  virtual IFrame createFrame(uint64_t id) = 0;
};
