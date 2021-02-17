/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

#include <agribot_common/CanFrame.h>
#include <vector>
#include <optional>
#include <cstdint>

namespace hal_tool
{
template <class T>
class ICanReceivedData
{
  virtual void setParsedValue(const T val) = 0;

 public:
  virtual ~ICanReceivedData(){}
  virtual void assembleValueFromFrame(const CanFrame& can_frame) = 0;
  virtual std::optional<T> getAssembledValue() const = 0;
  virtual void resetParsedValue() = 0;
};
}  // namespace hal_tool
