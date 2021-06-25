/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <agribot_common/connection/MsbFirstParsingStrategy.h>

uint8_t MsbFirstParsingStrategy::getUint8(std::vector<uint8_t>::const_iterator it)
{
  return *it;
}

uint16_t MsbFirstParsingStrategy::getUint16(std::vector<uint8_t>::const_iterator it)
{
  return (static_cast<uint16_t>(*(it + 1)) | static_cast<uint16_t>(*(it)) << 8);
}

uint32_t MsbFirstParsingStrategy::getUint32(std::vector<uint8_t>::const_iterator it)
{
  return (static_cast<uint32_t>(*(it + 3)) | static_cast<uint32_t>(*(it + 2)) << 8 |
          static_cast<uint32_t>(*(it + 1)) << 16 | static_cast<uint32_t>(*(it)) << 24);
}

uint64_t MsbFirstParsingStrategy::getUint64(std::vector<uint8_t>::const_iterator it)
{
  return (static_cast<uint64_t>(*(it + 7)) | static_cast<uint64_t>(*(it + 6)) << 8 |
          static_cast<uint64_t>(*(it + 5)) << 16 | static_cast<uint64_t>(*(it + 4)) << 24 |
          static_cast<uint64_t>(*(it + 3)) << 32 | static_cast<uint64_t>(*(it + 2)) << 40 |
          static_cast<uint64_t>(*(it + 1)) << 48 | static_cast<uint64_t>(*(it)) << 56);
}

float MsbFirstParsingStrategy::getFloat(std::vector<uint8_t>::const_iterator it)
{
  auto parsed_uint32 = getUint32(it);
  float parsed_float;
  std::memcpy(&parsed_float, &parsed_uint32, sizeof(float));

  return parsed_float;
}

// NOTE: memcpy should work properly on systems with Most Significant Byte First and Least Significant Byte First. It
// assumes that float/double has the same byte order as uint32/uint64. An uint32/uint64 are parsed using
// platform-independent binary operators and shifts
double MsbFirstParsingStrategy::getDouble(std::vector<uint8_t>::const_iterator it)
{
  auto parsed_uint64 = getUint64(it);
  double parsed_double;
  std::memcpy(&parsed_double, &parsed_uint64, sizeof(double));

  return parsed_double;
}

std::string MsbFirstParsingStrategy::getString(std::vector<uint8_t>::const_iterator begin_it,
                                               std::vector<uint8_t>::const_iterator end_it)
{
  std::vector<uint8_t>::const_reverse_iterator crbegin_it{ end_it };
  std::vector<uint8_t>::const_reverse_iterator crend_it{ begin_it };
  return std::string(crbegin_it, crend_it);
}
