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
    args = parser.parse_args()

    inbag_path = args.i
    magnetometer_topic = args.t

    x_list = []
    y_list = []
    z_list = []

    with rosbag.Bag(inbag_path) as inbag:
        for topic, msg, t in inbag.read_messages(topics=[magnetometer_topic]):
            if topic == magnetometer_topic:
                x_list.append(msg.magnetic_field.x)
                y_list.append(msg.magnetic_field.y)
                z_list.append(msg.magnetic_field.z)

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1, 1, 1, projection='3d')
    ax1.plot(x_list, y_list, z_list, 'r.')
    ax1.set(xlabel='x', ylabel='y', zlabel='z', title='Magnetometer 3D plot')
    ax1.grid()

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(1, 1, 1)
    ax2.plot(x_list, y_list, 'r.')
    ax2.set(xlabel='x', ylabel='y', title='Magnetometer X-Y plot')
    ax2.grid()

    plt.show()
