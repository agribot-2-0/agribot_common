/*
 * Copyright (C) 2020 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/CanBus/ICan.h>
#include <gmock/gmock.h>

class CanMock : public ICan
{
public:
  MOCK_METHOD1(iInitialize, int(const char* pchCanChannel));
  MOCK_METHOD0(bReceiveFrame, bool());
  MOCK_METHOD1(bReceiveFrame, bool(can_frame * frame));
  MOCK_METHOD2(iSendFrame, int(can_frame * frame, bool extended_id));
  MOCK_CONST_METHOD0(getMostRecentCanFrame, CanFrame());
};
