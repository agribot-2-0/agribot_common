#!/usr/bin/env python2

import argparse
import yaml
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import rosbag


class MagnetometerComparisonPlot(object):
    def __init__(self, magnetometer_topic, inbag_path_1, inbag_path_2):
        self.magnetometer_topic = magnetometer_topic
        self.x_list_1, self.y_list_1, self.z_list_1 = self.load_data(
            inbag_path_1)
        self.x_list_2, self.y_list_2, self.z_list_2 = self.load_data(
            inbag_path_2)

    def load_data(self, bag_path):
        x_list = []
        y_list = []
        z_list = []

        with rosbag.Bag(bag_path) as inbag:
            for topic, msg, t in inbag.read_messages(topics=[self.magnetometer_topic]):
                if topic == self.magnetometer_topic:
                    x_list.append(msg.magnetic_field.x)
                    y_list.append(msg.magnetic_field.y)
                    z_list.append(msg.magnetic_field.z)

        return x_list, y_list, z_list

    def plot_data(self):

        fig = plt.figure()

        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot(self.x_list_1, self.y_list_1, self.z_list_1, 'r.', label='Bag 1')
        ax.plot(self.x_list_2, self.y_list_2, self.z_list_2, 'b.', label='Bag 2')
        ax.set(xlabel='x', ylabel='y', title='3D magnetometer plot')
        ax.legend()
        ax.grid()

        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='3D comparison plot of 2 magnetometer from bags')

    parser.add_argument('-i1',
                        metavar='INPUT_BAGFILE_1',
                        required=True,
                        help='input bagfile 1')
    parser.add_argument('-i2',
                        metavar='INPUT_BAGFILE_2',
                        required=True,
                        help='input bagfile 2')

    parser.add_argument('-t',
                        metavar='MAGNETOMETER_TOPIC',
                        required=False,
                        default='/agribot/imu/raw/mag',
                        help='Magnetometer topic')
    args = parser.parse_args()

    inbag_1_path = args.i1
    inbag_2_path = args.i2
    topic = args.t

    mcp = MagnetometerComparisonPlot(topic, inbag_1_path, inbag_2_path)
    mcp.plot_data()
