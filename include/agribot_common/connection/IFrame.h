/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/connection/IParsingStrategy.h>

#include <cstdint>
#include <vector>

struct IFrame
{
  IFrame() = default;
  virtual ~IFrame() = default;
  IFrame(const IFrame& other) = delete;
  IFrame(IFrame&& other) = delete;
  IFrame& operator=(const IFrame& other) = delete;
  IFrame& operator=(IFrame&& other) = delete;

  virtual void deserialize(std::vector<uint8_t>::iterator begin_it, std::vector<uint8_t>::iterator end_it) = 0;
  virtual void serialize(std::vector<uint8_t>::iterator begin_it, std::vector<uint8_t>::iterator end_it) = 0;
};
