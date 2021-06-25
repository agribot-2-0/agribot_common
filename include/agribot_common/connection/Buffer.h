/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <cstdint>
#include <vector>

class Buffer
{
public:
  Buffer() = delete;
  explicit Buffer(std::size_t size);
  Buffer(std::vector<uint8_t>::iterator begin_it, std::vector<uint8_t>::iterator end_it);
  ~Buffer() = default;
  Buffer(const Buffer& other) = default;
  Buffer(Buffer&& other) = default;
  Buffer& operator=(const Buffer& other) = default;
  Buffer& operator=(Buffer&& other) = default;

  std::vector<uint8_t> buffer_;
  std::size_t read_length_;
};
