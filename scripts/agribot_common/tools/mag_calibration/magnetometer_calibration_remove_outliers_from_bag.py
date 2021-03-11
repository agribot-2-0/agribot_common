#!/usr/bin/env python

from __future__ import print_function

import argparse
import rosbag

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # pylint: disable=unused-import
from scipy.spatial import KDTree


class MagnetometerCalibrationRemoveOutliers(object):
    def __init__(self):
        self.magnetic_field_msgs = []
        self.processed_magnetic_field_msgs = []

    def load_from_bag(self, bag_path, magnetometer_topic):
        try:
            with rosbag.Bag(bag_path) as inbag:
                for topic, msg, time in inbag.read_messages(
                        topics=[magnetometer_topic]):
                    if topic == magnetometer_topic:
                        mag_d = {'topic': topic, 't': time, 'msg': msg}
                        self.magnetic_field_msgs.append(mag_d)
        except IOError as error:
            print(error)
        except rosbag.bag.ROSBagException as error:
            print('[Error] {}'.format(error))

    def save_to_bag(self, bag_path):
        try:
            with rosbag.Bag(bag_path, 'w') as outbag:
                for mag_d in self.processed_magnetic_field_msgs:
                    outbag.write(mag_d['topic'], mag_d['msg'], mag_d['t'])
        except IOError as error:
            print(error)
        except rosbag.bag.ROSBagException as error:
            print('[Error] {}'.format(error))

    def remove_outliers(self, radius, min_neighbors_number):
        # Create KDTree object
        buf = [[
            d['msg'].magnetic_field.x, d['msg'].magnetic_field.y,
            d['msg'].magnetic_field.z
        ] for d in self.magnetic_field_msgs]
        tree = KDTree(np.array(buf))
        outliers_removed_cnt = 0

        for mag_d in self.magnetic_field_msgs:
            point = [
                mag_d['msg'].magnetic_field.x, mag_d['msg'].magnetic_field.y,
                mag_d['msg'].magnetic_field.z
            ]
            neighbors = tree.query_ball_point(x=point, r=radius)

            if len(neighbors) >= min_neighbors_number:
                self.processed_magnetic_field_msgs.append(mag_d)
            else:
                outliers_removed_cnt += 1

        print('Removed {} outliers'.format(outliers_removed_cnt))

    def plot_results(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(111, projection='3d')

        raw_x_list = [
            d['msg'].magnetic_field.x for d in self.magnetic_field_msgs
        ]
        raw_y_list = [
            d['msg'].magnetic_field.y for d in self.magnetic_field_msgs
        ]
        raw_z_list = [
            d['msg'].magnetic_field.z for d in self.magnetic_field_msgs
        ]

        processed_x_list = [
            d['msg'].magnetic_field.x
            for d in self.processed_magnetic_field_msgs
        ]
        processed_y_list = [
            d['msg'].magnetic_field.y
            for d in self.processed_magnetic_field_msgs
        ]
        processed_z_list = [
            d['msg'].magnetic_field.z
            for d in self.processed_magnetic_field_msgs
        ]

        ax1.plot(raw_x_list, raw_y_list, raw_z_list, 'r.', label='Raw')
        ax1.plot(processed_x_list,
                 processed_y_list,
                 processed_z_list,
                 'b.',
                 label='Outliers removed')
        ax1.grid()
        ax1.legend()
        plt.show()


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description='Rewrites bag with header timestamps as time.')

    PARSER.add_argument('-o',
                        metavar='OUTPUT_BAGFILE',
                        required=True,
                        help='output bagfile')
    PARSER.add_argument('-i',
                        metavar='INPUT_BAGFILE',
                        required=True,
                        help='input bagfile')
    PARSER.add_argument('-r',
                        metavar='RADIUS',
                        required=False,
                        default=1.0e-6,
                        help='neighbor search distance')
    PARSER.add_argument('-n',
                        metavar='MIN_NEIGHBORS_NUMBER',
                        required=False,
                        default=10,
                        help='Mininaml number of neighbors in radius')
    PARSER.add_argument('-t',
                        metavar='MAGNETOMETER_TOPIC',
                        required=False,
                        default='/agribot/imu/raw/mag',
                        help='Magnetometer topic')
    ARGS = PARSER.parse_args()

    INBAG_PATH = ARGS.i
    OUTBAG_PATH = ARGS.o
    RADIUS = float(ARGS.r)
    MIN_NEIGHBORS_NUMBER = int(ARGS.n)
    TOPIC = ARGS.t

    print(
        'Performing outliers removal with radius = {} and min_neighbors_number = {}'
        .format(RADIUS, MIN_NEIGHBORS_NUMBER))

    MCRO = MagnetometerCalibrationRemoveOutliers()
    MCRO.load_from_bag(INBAG_PATH, TOPIC)
    MCRO.remove_outliers(RADIUS, MIN_NEIGHBORS_NUMBER)
    MCRO.save_to_bag(OUTBAG_PATH)
    MCRO.plot_results()
