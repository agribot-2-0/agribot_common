#!/usr/bin/env python

# Based on: http://wiki.ros.org/rosbag/Cookbook

import rosbag
import sys
import argparse

parser = argparse.ArgumentParser(
    description='Rewrites bag with header timestamps as time.')

parser.add_argument('-o', metavar='OUTPUT_BAGFILE', required=True, help='output bagfile')
parser.add_argument('-i', metavar='INPUT_BAGFILE', required=True, help='input bagfile')
args = parser.parse_args()
inbag_path = args.i
outbag_path = args.o

try:
    data = []

    # Read from inbag
    with rosbag.Bag(inbag_path) as inbag:
        print('[Progress] Reading from inbag...')
        for topic, msg, t in inbag.read_messages():
            if topic == "/tf" and msg.transforms:
                data.append([topic, msg, msg.transforms[0].header.stamp])
            elif msg._has_header:
                data.append([topic, msg, msg.header.stamp])
            else:
                data.append([topic, msg, t])
    
    # Reorder according to timestamps
    print('[Progress] Reordering according to timestamps...')
    data.sort(key=lambda x: x[2])

    # Write to outbag
    print('[Progress] Writing to outbag...')
    with rosbag.Bag(outbag_path, 'w') as outbag:
        for topic, msg, t in data:
            outbag.write(topic, msg, t)

    print('[Success] Bag rewritten succesfully...')
except IOError as e:
    print(e)
except rosbag.bag.ROSBagException as e:
    print('[Error] {}'.format(e))
