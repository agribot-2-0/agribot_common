#!/usr/bin/env python2

### IMPORTANT NOTE ###
# When analizing order of messages it is recommended to record rosbag using explicitly stated topics
# e.g. "rosbag record /agribot/odom/global /agribot/odom/raw /agribot/imu/filtered /agribot/imu/prefiltered"
# instead of recording all frames with "rosbag record -a", as the latter option may drop/miss couple of frames at the beginning

# Also pay attention to the possible differences between time recorded in the bag (time when the message was received by bag recorder)
# and time in the message timestamp (stamped by publisher)

import rosbag
from termcolor import colored
from tabulate import tabulate
from tf.transformations import euler_from_quaternion
from math import degrees

# input_bag_path = '/TODO/put/path/to/bag/here'

# Time up to which the angles are printed
time_threshold = 1.0
# time_threshold = None

print(colored('\n\n[BAG] {}'.format(input_bag_path), 'red'))
records = []
with rosbag.Bag(input_bag_path) as inbag:
    for topic, msg, t in inbag.read_messages():
        if hasattr(msg, 'header'):
            time_header_sec = msg.header.stamp.to_sec()
        else:
            continue

        if time_threshold is not None:
            if time_header_sec > time_threshold:
                break

        if 'agribot/odom/global' in topic:
            quat = [
                msg.pose.pose.orientation.x, msg.pose.pose.orientation.y,
                msg.pose.pose.orientation.z, msg.pose.pose.orientation.w
            ]
            roll, pitch, yaw = euler_from_quaternion(quat)
            records.append([t.to_sec(), time_header_sec, topic, degrees(yaw)])
        elif 'agribot/odom/raw' in topic:
            quat = [
                msg.pose.pose.orientation.x, msg.pose.pose.orientation.y,
                msg.pose.pose.orientation.z, msg.pose.pose.orientation.w
            ]
            roll, pitch, yaw = euler_from_quaternion(quat)
            records.append([t.to_sec(), time_header_sec, topic, degrees(yaw)])
        elif 'agribot/imu/prefiltered' in topic:
            quat = [
                msg.orientation.x, msg.orientation.y, msg.orientation.z,
                msg.orientation.w
            ]
            roll, pitch, yaw = euler_from_quaternion(quat)
            records.append([t.to_sec(), time_header_sec, topic, degrees(yaw)])
        elif 'agribot/imu/filtered' in topic:
            quat = [
                msg.orientation.x, msg.orientation.y, msg.orientation.z,
                msg.orientation.w
            ]
            roll, pitch, yaw = euler_from_quaternion(quat)
            records.append([t.to_sec(), time_header_sec, topic, degrees(yaw)])

print(tabulate(
    records,
    headers=['Time recorded [s]', 'Time header [s]', 'Topic', 'Yaw [deg]']))
