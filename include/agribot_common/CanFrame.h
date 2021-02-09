/*
 * Copyright (C) 2020 Agribot. All rights reserved.
 */

#pragma once

#include <linux/can.h>

#include <cstdint>
#include <vector>


class CanFrame
{
 private:
  uint32_t can_id_;
  uint8_t can_dlc_;
  std::vector<uint8_t> data_;

 public:
  CanFrame(): can_id_(0), can_dlc_(0) {}
  void setupFrame(const can_frame& frame);
  std::vector<uint8_t> getData() const;
  uint32_t getId() const;
  uint8_t getDlc() const;
};
