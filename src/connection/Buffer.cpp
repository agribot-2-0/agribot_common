/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <agribot_common/connection/Buffer.h>

Buffer::Buffer(std::size_t size)
{
  buffer_.reserve(size);
}
