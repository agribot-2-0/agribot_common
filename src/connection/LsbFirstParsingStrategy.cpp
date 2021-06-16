/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <agribot_common/connection/LsbFirstParsingStrategy.h>

uint8_t LsbFirstParsingStrategy::getUint8(std::vector<uint8_t>::iterator it)
{
  return *it;
}

uint16_t LsbFirstParsingStrategy::getUint16(std::vector<uint8_t>::iterator it)
{
  return (static_cast<uint16_t>(*it) | static_cast<uint16_t>(*(it + 1)) << 8);
}

uint32_t LsbFirstParsingStrategy::getUint32(std::vector<uint8_t>::iterator it)
{
  return (static_cast<uint32_t>(*it) | static_cast<uint32_t>(*(it + 1)) << 8 | static_cast<uint32_t>(*(it + 2)) << 16 |
          static_cast<uint32_t>(*(it + 3)) << 24);
}

uint64_t LsbFirstParsingStrategy::getUint64(std::vector<uint8_t>::iterator it)
{
  return (static_cast<uint64_t>(*it) | static_cast<uint64_t>(*(it + 1)) << 8 | static_cast<uint64_t>(*(it + 2)) << 16 |
          static_cast<uint64_t>(*(it + 3)) << 24 | static_cast<uint64_t>(*(it + 4)) << 32 |
          static_cast<uint64_t>(*(it + 5)) << 40 | static_cast<uint64_t>(*(it + 6)) << 48 |
          static_cast<uint64_t>(*(it + 7)) << 56);
}

float LsbFirstParsingStrategy::getFloat(std::vector<uint8_t>::iterator it)
{
  auto parsed_uint32 = getUint32(it);
  float parsed_float;
  std::memcpy(&parsed_float, &parsed_uint32, sizeof(float));

  return parsed_float;
}

double LsbFirstParsingStrategy::getDouble(std::vector<uint8_t>::iterator it)
{
  auto parsed_uint64 = getUint64(it);
  float parsed_double;
  std::memcpy(&parsed_double, &parsed_uint64, sizeof(float));

  return parsed_double;
}

std::string LsbFirstParsingStrategy::getString(std::vector<uint8_t>::iterator begin_it,
                                               std::vector<uint8_t>::iterator end_it)
{
  return std::string(begin_it, end_it);
}
