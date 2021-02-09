#!/usr/bin/env python2

from __future__ import print_function  # Necessary to pass print as argument in Python2

import argparse
import rospy
import rosbag

from magnetometer_calibration import MagnetometerCalibration


class MagnetometerCalibrationFromBag(MagnetometerCalibration):
    def __init__(self, magnitude):
        super(MagnetometerCalibrationFromBag, self).__init__(print, magnitude)

    def collect_data(self, magnetometer_topic, bag_path):
        self.logger(
            '[MagnetometerCalibration] Data collection from bag started...')

        with rosbag.Bag(bag_path) as inbag:
            for topic, msg, t in inbag.read_messages():
                if topic == magnetometer_topic:
                    self.x_list.append(msg.magnetic_field.x)
                    self.y_list.append(msg.magnetic_field.y)
                    self.z_list.append(msg.magnetic_field.z)

        self.logger(
            '[MagnetometerCalibration] Finished collecting data from {} bag...'
            .format(bag_path))


if __name__ == '__main__':
    try:
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
                            metavar='MAGNETOMETER_MAGNITUDE',
                            required=False,
                            default=4.9714e-5,
                            help='Magnetometer topic')
        args = parser.parse_args()

        inbag_path = args.i
        topic = args.t
        magnitude = float(args.m)

        # Initialize
        mcfb = MagnetometerCalibrationFromBag(magnitude)

        # Collect data and compute parameters
        mcfb.collect_data(topic, inbag_path)
        mcfb.compute_parameters()

        # Show and save parameters
        mcfb.print_parameters()
        mcfb.save_parameters_to_yaml('./mag_bias_from_bag.yaml')

        # Compute and plot additional data
        mcfb.compute_corrected_data()
        mcfb.plot_data()
    except rospy.ROSInterruptException:
        pass
