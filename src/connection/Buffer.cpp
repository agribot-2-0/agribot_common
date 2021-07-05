/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <agribot_common/connection/Buffer.h>

Buffer::Buffer(std::size_t size) : read_length_(0)
{
  buffer_.resize(size);
}

Buffer::Buffer(std::vector<uint8_t>::iterator begin_it, std::vector<uint8_t>::iterator end_it)
  : buffer_{ begin_it, end_it }, read_length_{ static_cast<std::size_t>(std::distance(begin_it, end_it)) }
{
}

void Buffer::clear()
{
  read_length_ = 0;
}
