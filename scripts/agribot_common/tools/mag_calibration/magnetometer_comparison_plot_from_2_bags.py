#!/usr/bin/env python2

import argparse
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # pylint: disable=unused-import

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
            for topic, msg, _ in inbag.read_messages(
                    topics=[self.magnetometer_topic]):
                if topic == self.magnetometer_topic:
                    x_list.append(msg.magnetic_field.x)
                    y_list.append(msg.magnetic_field.y)
                    z_list.append(msg.magnetic_field.z)

        return x_list, y_list, z_list

    def plot_data(self):

        fig = plt.figure()

        ax1 = fig.add_subplot(1, 1, 1, projection='3d')
        ax1.plot(self.x_list_1,
                 self.y_list_1,
                 self.z_list_1,
                 'r.',
                 label='Bag 1')
        ax1.plot(self.x_list_2,
                 self.y_list_2,
                 self.z_list_2,
                 'b.',
                 label='Bag 2')
        ax1.set(xlabel='x', ylabel='y', title='3D magnetometer plot')
        ax1.legend()
        ax1.grid()

        plt.show()


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description='3D comparison plot of 2 magnetometer from bags')

    PARSER.add_argument('-i1',
                        metavar='INPUT_BAGFILE_1',
                        required=True,
                        help='input bagfile 1')
    PARSER.add_argument('-i2',
                        metavar='INPUT_BAGFILE_2',
                        required=True,
                        help='input bagfile 2')

    PARSER.add_argument('-t',
                        metavar='MAGNETOMETER_TOPIC',
                        required=False,
                        default='/agribot/imu/raw/mag',
                        help='Magnetometer topic')
    ARGS = PARSER.parse_args()

    INBAG_1_PATH = ARGS.i1
    INBAG_2_PATH = ARGS.i2
    TOPIC = ARGS.t

    MCP = MagnetometerComparisonPlot(TOPIC, INBAG_1_PATH, INBAG_2_PATH)
    MCP.plot_data()
