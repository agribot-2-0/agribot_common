#!/usr/bin/env python2

import argparse

import rosbag
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Magnetometer calibration from bag')

    parser.add_argument('-i',
                        metavar='INPUT_BAGFILE',
                        required=True,
                        help='input bagfile')
    parser.add_argument('-t',
                        metavar='MAGNETOMETER_TOPIC',
                        required=False,
                        default='/agribot/imu/raw/mag',
                        help='Magnetometer topic')
    parser.add_argument('-m',
                        metavar='MAGNETOMETER_MAGNITUDE_Z',
                        required=False,
                        default=4.5804e-5,
                        help='Magnetometer magnitude z')
    args = parser.parse_args()

    inbag_path = args.i
    magnetometer_topic = args.t
    magnitude_z = args.m

    z_list = []

    with rosbag.Bag(inbag_path) as inbag:
        for topic, msg, t in inbag.read_messages(topics=[magnetometer_topic]):
            if topic == magnetometer_topic:
                z_list.append(msg.magnetic_field.z)

    min_z = min(z_list)
    max_z = max(z_list)
    offset = -(max_z + min_z) / 2.0
    scale = (2.0 * magnitude_z) / (max_z - min_z)

    print('Offset: {}'.format(offset))
    print('Scale: {}'.format(scale))
