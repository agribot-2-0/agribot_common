/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/connection/Buffer.h>

class ISocket
{
public:
  ISocket() = default;
  virtual ~ISocket() = default;
  virtual void open() = 0;
  virtual void close() = 0;
  virtual void connect() = 0;
  virtual void reconnect() = 0;
  virtual void read(Buffer& buffer) = 0;  // NOLINT(runtime/references)
};
