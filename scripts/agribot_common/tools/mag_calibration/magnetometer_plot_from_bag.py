#!/usr/bin/env python2

import argparse

import rosbag
import matplotlib.pyplot as plt
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
    ARGS = PARSER.parse_args()

    INBAG_PATH = ARGS.i
    MAGNETOMETER_TOPIC = ARGS.t

    X_LIST = []
    Y_LIST = []
    Z_LIST = []

    with rosbag.Bag(INBAG_PATH) as inbag:
        for topic, msg, t in inbag.read_messages(topics=[MAGNETOMETER_TOPIC]):
            if topic == MAGNETOMETER_TOPIC:
                X_LIST.append(msg.magnetic_field.x)
                Y_LIST.append(msg.magnetic_field.y)
                Z_LIST.append(msg.magnetic_field.z)

    FIG1 = plt.figure()
    AX1 = FIG1.add_subplot(1, 1, 1, projection='3d')
    AX1.plot(X_LIST, Y_LIST, Z_LIST, 'r.')
    AX1.set(xlabel='x', ylabel='y', zlabel='z', title='Magnetometer 3D plot')
    AX1.grid()

    FIG2 = plt.figure()
    AX2 = FIG2.add_subplot(1, 1, 1)
    AX2.plot(X_LIST, Y_LIST, 'r.')
    AX2.set(xlabel='x', ylabel='y', title='Magnetometer X-Y plot')
    AX2.grid()

    plt.show()
