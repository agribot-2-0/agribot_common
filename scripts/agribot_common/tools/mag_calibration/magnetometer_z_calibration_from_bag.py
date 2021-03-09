#!/usr/bin/env python2

import argparse

import rosbag
from mpl_toolkits.mplot3d import Axes3D  # pylint: disable=unused-import

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description='Magnetometer calibration from bag')

    PARSER.add_argument('-i',
                        metavar='INPUT_BAGFILE',
                        required=True,
                        help='input bagfile')
    PARSER.add_argument('-t',
                        metavar='MAGNETOMETER_TOPIC',
                        required=False,
                        default='/agribot/imu/raw/mag',
                        help='Magnetometer topic')
    PARSER.add_argument('-m',
                        metavar='MAGNETOMETER_MAGNITUDE_Z',
                        required=False,
                        default=4.5804e-5,
                        help='Magnetometer magnitude z')
    ARGS = PARSER.parse_args()

    INBAG_PATH = ARGS.i
    MAGNETOMETER_TOPIC = ARGS.t
    MAGNITUDE_Z = ARGS.m

    Z_LIST = []

    with rosbag.Bag(INBAG_PATH) as in_bag:
        for topic, msg, t in in_bag.read_messages(topics=[MAGNETOMETER_TOPIC]):
            if topic == MAGNETOMETER_TOPIC:
                Z_LIST.append(msg.magnetic_field.z)

    MIN_Z = min(Z_LIST)
    MAX_Z = max(Z_LIST)
    OFFSET = -(MAX_Z + MIN_Z) / 2.0
    SCALE = (2.0 * MAGNITUDE_Z) / (MAX_Z - MIN_Z)

    print('Offset: {}'.format(OFFSET))
    print('Scale: {}'.format(SCALE))
