/*
 * Copyright (C) 2021 Agribot. All rights reserved.
 */

#pragma once

namespace tool_manager
{

struct TplConfig
{
  double tpl_angle = 0.0;
  double tpl_height = 0.0;
  double red_valve_flow = 0.0;
  double yellow_valve_flow = 0.0;
  double blue_valve_flow = 0.0;
  double pto_rpm = 0.0;

  void operator=(const TplConfig& cfg)
  {
    tpl_angle = cfg.tpl_angle;
    tpl_height = cfg.tpl_height;
    red_valve_flow = cfg.red_valve_flow;
    yellow_valve_flow = cfg.yellow_valve_flow;
    blue_valve_flow = cfg.blue_valve_flow;
    pto_rpm = cfg.pto_rpm;
  }
};
}  // namespace tool_manager
