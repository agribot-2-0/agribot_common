/*
 * Copyright (C) 2020 Agribot. All rights reserved.
 */

#pragma once

#include <cstdint>
#include <vector>

namespace CanHelperFunctions
{
inline uint16_t getNodeSource(uint32_t extendedId)
{
  return static_cast<uint16_t>(extendedId);
}

inline int8_t getI8(uint8_t start_byte, const std::vector<uint8_t>& data)
{
  return data[start_byte];
}

inline int16_t getI16Lsbf(uint8_t start_byte, const std::vector<uint8_t>& data)
{
  return static_cast<int16_t>((static_cast<int16_t>(data[start_byte + 1]) << 8) |
                              static_cast<int16_t>(data[start_byte]));
}

inline int16_t getI16Msbf(uint8_t start_byte, const std::vector<uint8_t>& data)
{
  return static_cast<int16_t>((static_cast<int32_t>(data[start_byte]) << 8) |
                              static_cast<int32_t>(data[start_byte + 1]));
}

inline int32_t getI32Lsbf(uint8_t start_byte, const std::vector<uint8_t>& data)
{
  return static_cast<int32_t>(
      (static_cast<int32_t>(data[start_byte + 3]) << 24) | (static_cast<int32_t>(data[start_byte + 2]) << 16) |
      (static_cast<int32_t>(data[start_byte + 1]) << 8) | (static_cast<int32_t>(data[start_byte])));
}

inline int32_t getI32Msbf(uint8_t start_byte, const std::vector<uint8_t>& data)
{
  return static_cast<int32_t>(
      (static_cast<int32_t>(data[start_byte]) << 24) | (static_cast<int32_t>(data[start_byte + 1]) << 16) |
      (static_cast<int32_t>(data[start_byte + 2]) << 8) | (static_cast<int32_t>(data[start_byte + 3])));
}

}  // namespace CanHelperFunctions
