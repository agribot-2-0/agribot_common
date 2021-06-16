/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#include <agribot_common/connection/IFrame.h>

void IFrame::parse(std::vector<uint8_t>::iterator begin_it, std::vector<uint8_t>::iterator end_it,
                   IParsingStrategy& strategy)
{
  // Suppress unused variable error
  static_cast<void>(begin_it);
  static_cast<void>(end_it);
  static_cast<void>(strategy);
}
