#!/usr/bin/env python2

from __future__ import print_function  # Necessary to pass print as argument in Python2

import rospy
import rosbag

from imu_calibration import ImuCalibration


class ImuCalibrationFromBag(ImuCalibration):
    def __init__(self):
        super(ImuCalibrationFromBag, self).__init__(print)

    def collect_data(self, imu_topic, bag_path):
        self.logger(
            '[ImuCalibration] Data collection from bag started...')

        with rosbag.Bag(bag_path) as inbag:
            for topic, msg, t in inbag.read_messages():
                if topic == imu_topic:
                    self.x_gyro_list.append(msg.angular_velocity.x)
                    self.y_gyro_list.append(msg.angular_velocity.y)
                    self.z_gyro_list.append(msg.angular_velocity.z)
                    self.x_acc_list.append(msg.linear_acceleration.x)
                    self.y_acc_list.append(msg.linear_acceleration.y)
                    self.z_acc_list.append(msg.linear_acceleration.z)

        self.logger(
            '[ImuCalibration] Finished collecting data from {} bag...'
            .format(bag_path))


if __name__ == '__main__':
    try:
        # Provide imu topic and /your/path/to/file.bag
        imu_topic = '/agribot/imu/raw/data'
        # bag_path = '/your/path/to/file.bag'
        bag_path = '/home/olek/agribot/logs/2_02_2021/imu_calib_only_imu.bag'

        # Initialize
        ic = ImuCalibrationFromBag()

        # Collect data and compute parameters
        ic.collect_data(imu_topic, bag_path)
        ic.compute_offsets()

        # Show and save parameters
        ic.print_offsets()
        ic.save_offsets_to_yaml('./imu_bias_from_bag.yaml')

    except rospy.ROSInterruptException:
        pass
