/*
 * Copyright (C) 2020 Agribot. All rights reserved.
 */

#include <agribot_common/Can.h>

Can::Can()
{
  _iFileDesc = 0;
}

int Can::iInitialize(const char* pchCanChannel)
{
  struct sockaddr_can Addr;
  int iRet = 0;
  // Capture all errors described in:
  // https://github.com/linux-can/can-utils/blob/master/include/linux/can/error.h
  can_err_mask_t ErrMask = 0x1ff;
  struct ifreq _ifr;

  _iFileDesc = socket(PF_CAN, SOCK_RAW, CAN_RAW);

  if (_iFileDesc < 0)
  {
    return SocketInitCode::ERROR_WHILE_OPENING_SOCKET;
  }

  snprintf(_ifr.ifr_name, sizeof(&pchCanChannel), "%s", pchCanChannel);
  ioctl(_iFileDesc, SIOCGIFINDEX, &_ifr);

  Addr.can_family = AF_CAN;
  Addr.can_ifindex = _ifr.ifr_ifindex;

  if (bind(_iFileDesc, (struct sockaddr*)&Addr, sizeof(Addr)) < 0)
  {
    return SocketInitCode::ERROR_IN_SOCKET_BIND;
  }

  iRet = fcntl(_iFileDesc, F_SETFL, O_NONBLOCK);
  if (iRet != 0)
  {
    return SocketInitCode::FCNTL_FAIL;
  }

  iRet = setsockopt(_iFileDesc, SOL_CAN_RAW, CAN_RAW_ERR_FILTER, &ErrMask, sizeof(ErrMask));
  if (iRet != 0)
  {
    return SocketInitCode::SETSOCKOPT_FAIL;
  }
  return SocketInitCode::SUCCESS;
}

bool Can::bReceiveFrame(can_frame* frame)
{
  if (read(_iFileDesc, frame, sizeof((*frame))) > 0)
  {
    if (frame->can_id & CAN_ERR_FLAG)
    {
      std::cerr << "[CAN] Error frame received with id: 0x" << std::hex << frame->can_id << std::endl;
    }
    else
    {
      return true;
    }
  }
  return false;
}

// IF we use extended frames
// then we need to do (*frame).can_id = (*frame).can_id | CAN_EFF_FLAG;;
int Can::iSendFrame(can_frame* frame, bool extended_id)
{
  if (extended_id)
  {
    frame->can_id = frame->can_id | CAN_EFF_FLAG;
  }
  return write(_iFileDesc, frame, sizeof(struct can_frame));
}
