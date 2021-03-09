#!/usr/bin/env python2

### IMPORTANT NOTE ###
# When analizing order of messages it is recommended to record rosbag using explicitly stated topics
# e.g. "rosbag record /agribot/odom/global /agribot/odom/raw /agribot/imu/filtered"
# instead of recording all frames with "rosbag record -a",
# as the latter option may drop/miss couple of frames at the beginning

# Also pay attention to the possible differences between time recorded in the bag
# (time when the message was received by bag recorder)
# and time in the message timestamp (stamped by publisher)

from math import degrees

import rosbag
from tf.transformations import euler_from_quaternion

from termcolor import colored
from tabulate import tabulate

INPUT_BAG_PATH = '/TODO/put/path/to/bag/here'

# Time up to which the angles are printed
TIME_THRESHOLD = 1.0
# TIME_THRESHOLD = None

print(colored('\n\n[BAG] {}'.format(INPUT_BAG_PATH), 'red'))
RECORDS = []
with rosbag.Bag(INPUT_BAG_PATH) as inbag:
    for topic, msg, t in inbag.read_messages():
        if hasattr(msg, 'header'):
            time_header_sec = msg.header.stamp.to_sec()
        else:
            continue

        if TIME_THRESHOLD is not None:
            if time_header_sec > TIME_THRESHOLD:
                break

        if 'agribot/odom/global' in topic:
            quat = [
                msg.pose.pose.orientation.x, msg.pose.pose.orientation.y,
                msg.pose.pose.orientation.z, msg.pose.pose.orientation.w
            ]
            roll, pitch, yaw = euler_from_quaternion(quat)
            RECORDS.append([t.to_sec(), time_header_sec, topic, degrees(yaw)])
        elif 'agribot/odom/raw' in topic:
            quat = [
                msg.pose.pose.orientation.x, msg.pose.pose.orientation.y,
                msg.pose.pose.orientation.z, msg.pose.pose.orientation.w
            ]
            roll, pitch, yaw = euler_from_quaternion(quat)
            RECORDS.append([t.to_sec(), time_header_sec, topic, degrees(yaw)])
        elif 'agribot/imu/prefiltered' in topic:
            quat = [
                msg.orientation.x, msg.orientation.y, msg.orientation.z,
                msg.orientation.w
            ]
            roll, pitch, yaw = euler_from_quaternion(quat)
            RECORDS.append([t.to_sec(), time_header_sec, topic, degrees(yaw)])
        elif 'agribot/imu/filtered' in topic:
            quat = [
                msg.orientation.x, msg.orientation.y, msg.orientation.z,
                msg.orientation.w
            ]
            roll, pitch, yaw = euler_from_quaternion(quat)
            RECORDS.append([t.to_sec(), time_header_sec, topic, degrees(yaw)])

print(tabulate(
    RECORDS,
    headers=['Time recorded [s]', 'Time header [s]', 'Topic', 'Yaw [deg]']))
