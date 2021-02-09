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

inline uint16_t makeU16Lsbf(uint8_t start_byte, const std::vector<uint8_t>& data)
{
  return static_cast<uint16_t>((static_cast<uint16_t>(data[start_byte + 1]) << 8) | data[start_byte]);
}

inline uint16_t makeU16Msbf(uint8_t start_byte, const std::vector<uint8_t>& data)
{
  return static_cast<uint16_t>((static_cast<uint16_t>(data[start_byte]) << 8) | data[start_byte + 1]);
}

inline uint32_t makeU32Lsbf(uint8_t start_byte, const std::vector<uint8_t>& data)
{
  return static_cast<uint32_t>(
      (static_cast<uint32_t>(data[start_byte + 4]) << 24) | (static_cast<uint32_t>(data[start_byte + 2]) << 16) |
      (static_cast<uint32_t>(data[start_byte + 1]) << 8) | (static_cast<uint32_t>(data[start_byte])));
}

inline uint32_t makeU32Msbf(uint8_t start_byte, const std::vector<uint8_t>& data)
{
  return static_cast<uint32_t>(
      (static_cast<uint32_t>(data[start_byte]) << 24) | (static_cast<uint32_t>(data[start_byte + 1]) << 16) |
      (static_cast<uint32_t>(data[start_byte + 2]) << 8) | (static_cast<uint32_t>(data[start_byte + 3])));
}

}  // namespace CanHelperFunctions
