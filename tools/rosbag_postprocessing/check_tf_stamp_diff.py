#!/usr/bin/env python

import rosbag
import sys
import argparse

parser = argparse.ArgumentParser(
    description='Rewrites bag with header timestamps as time.')

parser.add_argument('-i',
                    metavar='INPUT_BAGFILE',
                    required=True,
                    help='input bagfile')
args = parser.parse_args()

inbag_path = args.i

try:
    # Read from inbag
    with rosbag.Bag(inbag_path) as inbag:
        print('[Progress] Reading from inbag...')
        for topic, msg, t in inbag.read_messages():
            if topic == "/tf" and msg.transforms:
                for transform in msg.transforms:
                    if transform.header.stamp != t:
                        tdiff = transform.header.stamp - t
                        print('Stamp differs for {} => {} at time {} by {}s'.
                              format(transform.header.frame_id,
                                     transform.child_frame_id, t.to_sec(),
                                     tdiff.to_sec()))
        print('[Success] Bag checked...')

except IOError as e:
    print(e)
except rosbag.bag.ROSBagException as e:
    print('[Error] {}'.format(e))
