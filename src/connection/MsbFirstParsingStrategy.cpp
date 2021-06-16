/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <agribot_common/connection/MsbFirstParsingStrategy.h>

uint8_t MsbFirstParsingStrategy::getUint8(std::vector<uint8_t>::iterator it)
{
  return *it;
}

uint16_t MsbFirstParsingStrategy::getUint16(std::vector<uint8_t>::iterator it)
{
  return (static_cast<uint16_t>(*(it + 1)) | static_cast<uint16_t>(*(it)) << 8);
}

uint32_t MsbFirstParsingStrategy::getUint32(std::vector<uint8_t>::iterator it)
{
  return (static_cast<uint32_t>(*(it + 3)) | static_cast<uint32_t>(*(it + 2)) << 8 |
          static_cast<uint32_t>(*(it + 1)) << 16 | static_cast<uint32_t>(*(it)) << 24);
}

uint64_t MsbFirstParsingStrategy::getUint64(std::vector<uint8_t>::iterator it)
{
  return (static_cast<uint64_t>(*(it + 7)) | static_cast<uint64_t>(*(it + 6)) << 8 |
          static_cast<uint64_t>(*(it + 5)) << 16 | static_cast<uint64_t>(*(it + 4)) << 24 |
          static_cast<uint64_t>(*(it + 3)) << 32 | static_cast<uint64_t>(*(it + 2)) << 40 |
          static_cast<uint64_t>(*(it + 1)) << 48 | static_cast<uint64_t>(*(it)) << 56);
}

float MsbFirstParsingStrategy::getFloat(std::vector<uint8_t>::iterator it)
{
  auto parsed_uint32 = getUint32(it);
  float parsed_float;
  std::memcpy(&parsed_float, &parsed_uint32, sizeof(float));

  return parsed_float;
}

double MsbFirstParsingStrategy::getDouble(std::vector<uint8_t>::iterator it)
{
  auto parsed_uint64 = getUint64(it);
  float parsed_double;
  std::memcpy(&parsed_double, &parsed_uint64, sizeof(float));

  return parsed_double;
}

std::string MsbFirstParsingStrategy::getString(std::vector<uint8_t>::iterator begin_it,
                                               std::vector<uint8_t>::iterator end_it)
{
  std::vector<uint8_t>::reverse_iterator rbegin_it{ end_it };
  std::vector<uint8_t>::reverse_iterator rend_it{ begin_it };
  return std::string(rbegin_it, rend_it);
}
