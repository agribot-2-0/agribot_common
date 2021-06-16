/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <cstdint>
#include <string>
#include <vector>

class IParsingStrategy
{
public:
  IParsingStrategy() = default;
  ~IParsingStrategy() = default;
  virtual uint8_t getUint8(std::vector<uint8_t>::iterator it) = 0;
  virtual uint16_t getUint16(std::vector<uint8_t>::iterator it) = 0;
  virtual uint32_t getUint32(std::vector<uint8_t>::iterator it) = 0;
  virtual uint64_t getUint64(std::vector<uint8_t>::iterator it) = 0;
  virtual float getFloat(std::vector<uint8_t>::iterator it) = 0;
  virtual double getDouble(std::vector<uint8_t>::iterator it) = 0;
  virtual std::string getString(std::vector<uint8_t>::iterator begin_it, std::vector<uint8_t>::iterator end_it) = 0;
};
