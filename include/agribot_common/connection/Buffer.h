/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <cstdint>
#include <vector>

class Buffer
{
public:
  std::vector<uint8_t> buffer_;
  std::size_t read_length_;

  Buffer() = default;
  explicit Buffer(std::size_t size);
  ~Buffer() = default;
};
