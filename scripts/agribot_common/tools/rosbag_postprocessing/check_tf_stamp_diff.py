#!/usr/bin/env python

from __future__ import print_function

import argparse
import rosbag

PARSER = argparse.ArgumentParser(
    description='Rewrites bag with header timestamps as time.')

PARSER.add_argument('-i',
                    metavar='INPUT_BAGFILE',
                    required=True,
                    help='input bagfile')
ARGS = PARSER.parse_args()

INBAG_PATH = ARGS.i

try:
    # Read from inbag
    with rosbag.Bag(INBAG_PATH) as inbag:
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

except IOError as error:
    print(error)
except rosbag.bag.ROSBagException as error:
    print('[Error] {}'.format(error))
