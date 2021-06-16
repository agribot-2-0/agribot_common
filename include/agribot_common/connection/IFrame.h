/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/connection/IParsingStrategy.h>

#include <cstdint>
#include <vector>

class IFrame
{
public:
  IFrame() = default;
  ~IFrame() = default;
  virtual void parse(std::vector<uint8_t>::iterator begin_it, std::vector<uint8_t>::iterator end_it,
                     IParsingStrategy& strategy);  // NOLINT(runtime/references)
};
