/*
 * Copyright (C) 2020 Agribot. All rights reserved.
 */

#include <agribot_common/CanFrame.h>

void CanFrame::setupFrame(const can_frame& frame)
{
  data_.clear();
  can_id_ = frame.can_id;
  can_dlc_ = frame.can_dlc;
  for (std::size_t i = 0; i < can_dlc_; i++)
  {
    data_.push_back(frame.data[i]);
  }
}

std::vector<uint8_t> CanFrame::getData() const
{
  return data_;
}

uint16_t CanFrame::getId() const
{
  return can_id_;
}

uint8_t CanFrame::getDlc() const
{
  return can_dlc_;
}
