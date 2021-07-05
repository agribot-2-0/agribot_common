/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/connection/parsing_strategy/IParsingStrategy.h>

#include <cstring>
#include <string>
#include <vector>

struct LsbFirstParsingStrategy : public IParsingStrategy
{
  uint8_t getUint8(std::vector<uint8_t>::const_iterator it) const override;
  uint16_t getUint16(std::vector<uint8_t>::const_iterator it) const override;
  uint32_t getUint32(std::vector<uint8_t>::const_iterator it) const override;
  uint64_t getUint64(std::vector<uint8_t>::const_iterator it) const override;
  float getFloat(std::vector<uint8_t>::const_iterator it) const override;
  double getDouble(std::vector<uint8_t>::const_iterator it) const override;
  std::string getString(std::vector<uint8_t>::const_iterator begin_it,
                        std::vector<uint8_t>::const_iterator end_it) const override;
};
