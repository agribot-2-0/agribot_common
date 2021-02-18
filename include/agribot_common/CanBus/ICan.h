/*
 * Copyright (C) 2020 Agribot. All rights reserved.
 */

#pragma once

#include <linux/can.h>
#include <agribot_common/CanFrame.h>
#include <iostream>
#include <memory>

class ICan
{
public:
  virtual ~ICan() = default;
  ICan() = default;
  ICan(const ICan&) = delete;
  ICan& operator=(const ICan&) = delete;
  ICan(ICan&&) = delete;
  ICan& operator=(ICan&&) = delete;
  virtual int iInitialize(const char* pchCanChannel) = 0;
  virtual bool bReceiveFrame() = 0;
  virtual bool bReceiveFrame(can_frame* frame) = 0;
  virtual int iSendFrame(can_frame* frame, bool extended_id = true) = 0;
  virtual CanFrame getMostRecentCanFrame() const = 0;
};
