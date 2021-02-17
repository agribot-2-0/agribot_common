/*
 * Copyright (C) 2020 Agribot. All rights reserved.
 */

#pragma once

#include <cstdint>
#include <vector>

namespace CanHelperFunctions
{
constexpr std::uint32_t pgn_and_sa_mask = 0xFFFFFF;

inline std::uint32_t getJ1939PgnAndSa(std::uint32_t extendedId)
{
  return extendedId & pgn_and_sa_mask;
}

inline std::int8_t getI8(std::uint8_t start_byte, const std::vector<std::uint8_t>& data)
{
  return static_cast<std::int8_t>(data[start_byte]);
}

inline std::uint8_t getU8(std::uint8_t start_byte, const std::vector<std::uint8_t>& data)
{
  return data[start_byte];
}

inline std::int16_t getI16Lsbf(std::uint8_t start_byte, const std::vector<std::uint8_t>& data)
{
  return (static_cast<std::int16_t>(data[start_byte + 1]) << 8) | static_cast<std::int16_t>(data[start_byte]);
}

inline std::int16_t getI16Msbf(std::uint8_t start_byte, const std::vector<std::uint8_t>& data)
{
  return (static_cast<std::int16_t>(data[start_byte]) << 8) | static_cast<std::int32_t>(data[start_byte + 1]);
}

inline std::int32_t getI32Lsbf(std::uint8_t start_byte, const std::vector<std::uint8_t>& data)
{
  return (static_cast<std::int32_t>(data[start_byte + 3]) << 24) |
         (static_cast<std::int32_t>(data[start_byte + 2]) << 16) |
         (static_cast<std::int32_t>(data[start_byte + 1]) << 8) | (static_cast<std::int32_t>(data[start_byte]));
}

inline std::int32_t getI32Msbf(std::uint8_t start_byte, const std::vector<std::uint8_t>& data)
{
  return (static_cast<std::int32_t>(data[start_byte]) << 24) | (static_cast<std::int32_t>(data[start_byte + 1]) << 16) |
         (static_cast<std::int32_t>(data[start_byte + 2]) << 8) | (static_cast<std::int32_t>(data[start_byte + 3]));
}

}  // namespace CanHelperFunctions
