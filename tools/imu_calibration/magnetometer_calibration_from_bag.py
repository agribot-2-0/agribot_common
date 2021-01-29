#!/usr/bin/env python2

from __future__ import print_function  # Necessary to pass print as argument in Python2

import rospy
import rosbag

from magnetometer_calibration import MagnetometerCalibration


class MagnetometerCalibrationFromBag(MagnetometerCalibration):
    def __init__(self):
        super(MagnetometerCalibrationFromBag, self).__init__(print)

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
        # Provide magnetometer topic and /your/path/to/file.bag
        magnetometer_topic = '/agribot/imu/raw/mag'
        bag_path = '/your/path/to/file.bag'

        # Initialize
        mc = MagnetometerCalibrationFromBag()

        # Collect data and compute parameters
        mc.collect_data(magnetometer_topic, bag_path)
        mc.compute_parameters()

        # Show and save parameters
        mc.print_parameters()
        mc.save_parameters_to_yaml('./imu_bias_from_bag.yaml')

        # Compute and plot additional data
        mc.compute_corrected_data()
        mc.plot_data()
    except rospy.ROSInterruptException:
        pass
