#!/usr/bin/env python

import sys
import argparse
import rosbag

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import KDTree


class MagnetometerCalibrationRemoveOutliers(object):
    def __init__(self):
        self.magnetic_field_msgs = []
        self.processed_magnetic_field_msgs = []

    def load_from_bag(self, bag_path):
        try:
            with rosbag.Bag(bag_path) as inbag:
                for topic, msg, t in inbag.read_messages():
                    if topic == '/agribot/imu/raw/mag':
                        d = {'topic': topic, 't': t, 'msg': msg}
                        self.magnetic_field_msgs.append(d)
        except IOError as e:
            print(e)
        except rosbag.bag.ROSBagException as e:
            print('[Error] {}'.format(e))

    def save_to_bag(self, bag_path):
        try:
            with rosbag.Bag(bag_path, 'w') as outbag:
                for d in self.processed_magnetic_field_msgs:
                    outbag.write(d['topic'], d['msg'], d['t'])
        except IOError as e:
            print(e)
        except rosbag.bag.ROSBagException as e:
            print('[Error] {}'.format(e))

    def remove_outliers(self, radius, min_neighbors_number):
        # Create KDTree object
        buf = [[
            d['msg'].magnetic_field.x, d['msg'].magnetic_field.y,
            d['msg'].magnetic_field.z
        ] for d in self.magnetic_field_msgs]
        tree = KDTree(np.array(buf))
        outliers_removed_cnt = 0

        for d in self.magnetic_field_msgs:
            point = [
                d['msg'].magnetic_field.x, d['msg'].magnetic_field.y,
                d['msg'].magnetic_field.z
            ]
            neighbors = tree.query_ball_point(x=point, r=radius)

            if len(neighbors) >= min_neighbors_number:
                self.processed_magnetic_field_msgs.append(d)
            else:
                outliers_removed_cnt += 1

        print('Removed {} outliers'.format(outliers_removed_cnt))

    def plot_results(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

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

        ax.plot(raw_x_list, raw_y_list, raw_z_list, 'r.', label='Raw')
        ax.plot(processed_x_list,
                processed_y_list,
                processed_z_list,
                'b.',
                label='Outliers removed')
        ax.grid()
        ax.legend()
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Rewrites bag with header timestamps as time.')

    parser.add_argument('-o',
                        metavar='OUTPUT_BAGFILE',
                        required=True,
                        help='output bagfile')
    parser.add_argument('-i',
                        metavar='INPUT_BAGFILE',
                        required=True,
                        help='input bagfile')
    parser.add_argument('-r',
                        metavar='RADIUS',
                        required=False,
                        default=1.0e-6,
                        help='neighbor search distance')
    parser.add_argument('-n',
                        metavar='MIN_NEIGHBORS_NUMBER',
                        required=False,
                        default=10,
                        help='Mininaml number of neighbors in radius')
    args = parser.parse_args()

    inbag_path = args.i
    outbag_path = args.o
    radius = float(args.r)
    min_neighbors_number = int(args.n)

    print(
        'Performing outliers removal with radius = {} and min_neighbors_number = {}'
        .format(radius, min_neighbors_number))

    mcro = MagnetometerCalibrationRemoveOutliers()
    mcro.load_from_bag(inbag_path)
    mcro.remove_outliers(radius, min_neighbors_number)
    mcro.save_to_bag(outbag_path)
    mcro.plot_results()
