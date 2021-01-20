/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

enum SocketInitCode
{
  SUCCESS = 0,
  ERROR_WHILE_OPENING_SOCKET = -1,
  ERROR_IN_SOCKET_BIND = -2,
  FCNTL_FAIL = -3,
  SETSOCKOPT_FAIL = -4
};
