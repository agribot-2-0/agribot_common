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
  virtual ~IFrame() = default;
  virtual void parse(std::vector<uint8_t>::iterator begin_it, std::vector<uint8_t>::iterator end_it,
                     IParsingStrategy& strategy) = 0;  // NOLINT(runtime/references)

protected:
  IFrame() = default;
  IFrame(const IFrame& other) = default;
  IFrame(IFrame&& other) = default;
  IFrame& operator=(const IFrame& other) = default;
  IFrame& operator=(IFrame&& other) = default;
};
