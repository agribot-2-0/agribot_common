/*
 * Copyright (C) 2020 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/SocketInitCode.h>

#include <fcntl.h>
#include <linux/can.h>
#include <linux/can/error.h>
#include <linux/can/raw.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <sstream>

#include <vector>

class Can
{
private:
  int _iFileDesc;
  std::vector<can_frame> can_error_frames_;

  void monitorCanErrorFramesSize();
  void addErrorToCanErrorFrames(can_frame* frame);
public:
  Can();
  // return: if 0 - config success, below 0 - config failed
  int iInitialize(const char* pchCanChannel);

  // true - frame received, false - no new frames
  bool bReceiveFrame(can_frame* frame);
  // example can frame to send:
  // frame.can_id  = 0x123;
  // frame.can_dlc = 8;
  // frame.data[0] = 0x1;
  // ...
  // frame.data[7] = 0x8;
  int iSendFrame(can_frame* frame, bool extended_id = true);
};
