/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/connection/IParsingStrategy.h>

#include <cstring>
#include <string>
#include <vector>

class MsbFirstParsingStrategy : public IParsingStrategy
{
public:
  MsbFirstParsingStrategy() = default;
  ~MsbFirstParsingStrategy() = default;
  uint8_t getUint8(std::vector<uint8_t>::iterator it) override;
  uint16_t getUint16(std::vector<uint8_t>::iterator it) override;
  uint32_t getUint32(std::vector<uint8_t>::iterator it) override;
  uint64_t getUint64(std::vector<uint8_t>::iterator it) override;
  float getFloat(std::vector<uint8_t>::iterator it) override;
  double getDouble(std::vector<uint8_t>::iterator it) override;
  std::string getString(std::vector<uint8_t>::iterator begin_it, std::vector<uint8_t>::iterator end_it) override;
};
