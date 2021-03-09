#!/usr/bin/env python

# Based on: http://wiki.ros.org/rosbag/Cookbook

import argparse
import rosbag

PARSER = argparse.ArgumentParser(
    description='Rewrites bag with header timestamps as time.')

PARSER.add_argument('-o',
                    metavar='OUTPUT_BAGFILE',
                    required=True,
                    help='output bagfile')
PARSER.add_argument('-i',
                    metavar='INPUT_BAGFILE',
                    required=True,
                    help='input bagfile')
ARGS = PARSER.parse_args()
INBAG_PATH = ARGS.i
OUTBAG_PATH = ARGS.o

try:
    DATA = []

    # Read from inbag
    with rosbag.Bag(INBAG_PATH) as inbag:
        print('[Progress] Reading from inbag...')
        for topic, msg, t in inbag.read_messages():
            if topic == "/tf" and msg.transforms:
                DATA.append([topic, msg, msg.transforms[0].header.stamp])
            elif msg._has_header:  # pylint: disable=protected-access
                DATA.append([topic, msg, msg.header.stamp])
            else:
                DATA.append([topic, msg, t])

    # Reorder according to timestamps
    print('[Progress] Reordering according to timestamps...')
    DATA.sort(key=lambda x: x[2])

    # Write to outbag
    print('[Progress] Writing to outbag...')
    with rosbag.Bag(OUTBAG_PATH, 'w') as outbag:
        for topic, msg, t in DATA:
            outbag.write(topic, msg, t)

    print('[Success] Bag rewritten succesfully...')
except IOError as error:
    print(error)
except rosbag.bag.ROSBagException as error:
    print('[Error] {}'.format(error))
