#!/usr/bin/env python

import rosbag
import sys
import argparse

parser = argparse.ArgumentParser(
    description='Rewrites bag with header timestamps as time.')

parser.add_argument('-i', metavar='INPUT_BAGFILE', required=True, help='input bagfile')
args = parser.parse_args()

inbag_path = args.i
previous_stamp = None

try:
    # Read from inbag
    with rosbag.Bag(inbag_path) as inbag:
        print('[Progress] Reading from inbag...')
        for topic, msg, t in inbag.read_messages():
            if topic == "/tf" and msg.transforms:
                
                # First iteration - set previious_stamp
                if not previous_stamp:
                    previous_stamp = msg.transforms[0].header.stamp
                    continue
                
                for transform in msg.transforms:
                    stamp = transform.header.stamp
                    if previous_stamp > stamp:
                        print('Ascending order broke at time {} for {} => {} transform'.format(transform.header.stamp.to_sec(), transform.header.frame_id, transform.child_frame_id))

                previous_stamp = msg.transforms[0].header.stamp
        
        print('[Success] Bag checked...')

except IOError as e:
    print(e)
except rosbag.bag.ROSBagException as e:
    print('[Error] {}'.format(e))
