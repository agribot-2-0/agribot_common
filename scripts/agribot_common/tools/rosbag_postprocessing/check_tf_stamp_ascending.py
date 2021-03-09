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
PREVIOUS_STAMP = None

try:
    # Read from inbag
    with rosbag.Bag(INBAG_PATH) as inbag:
        print('[Progress] Reading from inbag...')
        for topic, msg, t in inbag.read_messages():
            if topic == "/tf" and msg.transforms:

                # First iteration - set previious_stamp
                if not PREVIOUS_STAMP:
                    PREVIOUS_STAMP = msg.transforms[0].header.stamp
                    continue

                for transform in msg.transforms:
                    stamp = transform.header.stamp
                    if PREVIOUS_STAMP > stamp:
                        print(
                            'Ascending order broke at time {} for {} => {} transform'
                            .format(transform.header.stamp.to_sec(),
                                    transform.header.frame_id,
                                    transform.child_frame_id))

                PREVIOUS_STAMP = msg.transforms[0].header.stamp

        print('[Success] Bag checked...')

except IOError as error:
    print(error)
except rosbag.bag.ROSBagException as error:
    print('[Error] {}'.format(error))
