# rosbag_postprocessing tools
Used to investigate or modify bags with rosbag Python API (http://wiki.ros.org/rosbag/Code%20API)

---

#### check_tf_stamp_ascending.py
- Checks if all transform stamps are in ascending order (current_stamp >= previous_stamp)
- Usage: `rosrun agribot_common check_tf_stamp_ascending.py -i input.bag` 
- roscore **not** required to run

---

#### check_tf_stamp_diff.py
- Checks if bag contains transform (`/tf`) messages for which transform header timestamp differs with time logged by rosbag
- Usage: `rosrun agribot_common check_tf_stamp_diff.py -i input.bag` 
- roscore **not** required to run

---

#### rewrite_bag_with_header_timestamps.py
- Rewrites bag replacing logged rosbag time with header timestamps if possible (message contains header). Previous time is left for messages without the header. Messages are reordered according to new times.
- Usage: `rosrun agribot_common rewrite_bag_with_header_timestamps.py -i input.bag -o output.bag` 
- roscore **not** required to run
- Additional note: reordering performed in script (line 34) is **most likely** not required (as it is handled by bag.write(...)) but it is left just in case

---
