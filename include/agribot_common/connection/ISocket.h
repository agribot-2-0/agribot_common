/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/connection/Buffer.h>

class ISocket
{
public:
  virtual ~ISocket() = default;
  virtual void open() = 0;
  virtual void close() = 0;
  virtual void connect() = 0;
  virtual void reconnect() = 0;
  virtual void read(Buffer& buffer) = 0;  // NOLINT(runtime/references)
protected:
  ISocket() = default;
  ISocket(const ISocket& other) = default;
  ISocket(ISocket&& other) = default;
  ISocket& operator=(const ISocket& other) = default;
  ISocket& operator=(ISocket&& other) = default;
};
