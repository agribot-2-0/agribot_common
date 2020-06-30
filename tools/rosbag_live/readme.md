# rosbag_live tools
- Used to investigate bags when played live (with `rosbag play ...`)

---

#### check_tf_stamp_ascending_live.py
- Checks (by subbscribing to `/tf` topic) if all transform stamps are in ascending order (current_stamp >= previous_stamp)
- Usage: `rosrun agribot_common check_tf_stamp_ascending_live.py`
- roscore required to run

---
