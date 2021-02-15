/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

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
  virtual void assembleValueFromFrame(const std::vector<uint8_t>& data) = 0;
  virtual std::optional<T> getAssembledValue() const = 0;
  virtual void resetParsedFlag() = 0;
};
}  // namespace hal_tool
