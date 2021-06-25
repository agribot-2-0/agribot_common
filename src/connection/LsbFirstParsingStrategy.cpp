/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <agribot_common/connection/LsbFirstParsingStrategy.h>

uint8_t LsbFirstParsingStrategy::getUint8(std::vector<uint8_t>::const_iterator it)
{
  return *it;
}

uint16_t LsbFirstParsingStrategy::getUint16(std::vector<uint8_t>::const_iterator it)
{
  return (static_cast<uint16_t>(*it) | static_cast<uint16_t>(*(it + 1)) << 8);
}

uint32_t LsbFirstParsingStrategy::getUint32(std::vector<uint8_t>::const_iterator it)
{
  return (static_cast<uint32_t>(*it) | static_cast<uint32_t>(*(it + 1)) << 8 | static_cast<uint32_t>(*(it + 2)) << 16 |
          static_cast<uint32_t>(*(it + 3)) << 24);
}

uint64_t LsbFirstParsingStrategy::getUint64(std::vector<uint8_t>::const_iterator it)
{
  return (static_cast<uint64_t>(*it) | static_cast<uint64_t>(*(it + 1)) << 8 | static_cast<uint64_t>(*(it + 2)) << 16 |
          static_cast<uint64_t>(*(it + 3)) << 24 | static_cast<uint64_t>(*(it + 4)) << 32 |
          static_cast<uint64_t>(*(it + 5)) << 40 | static_cast<uint64_t>(*(it + 6)) << 48 |
          static_cast<uint64_t>(*(it + 7)) << 56);
}

// NOTE: memcpy should work properly on systems with Most Significant Byte First and Least Significant Byte First. It
// assumes that float/double has the same byte order as uint32/uint64. An uint32/uint64 are parsed using
// platform-independent binary operators and shifts
float LsbFirstParsingStrategy::getFloat(std::vector<uint8_t>::const_iterator it)
{
  auto parsed_uint32 = getUint32(it);
  float parsed_float;
  std::memcpy(&parsed_float, &parsed_uint32, sizeof(float));

  return parsed_float;
}

double LsbFirstParsingStrategy::getDouble(std::vector<uint8_t>::const_iterator it)
{
  auto parsed_uint64 = getUint64(it);
  double parsed_double;
  std::memcpy(&parsed_double, &parsed_uint64, sizeof(double));

  return parsed_double;
}

std::string LsbFirstParsingStrategy::getString(std::vector<uint8_t>::const_iterator begin_it,
                                               std::vector<uint8_t>::const_iterator end_it)
{
  return std::string(begin_it, end_it);
}
