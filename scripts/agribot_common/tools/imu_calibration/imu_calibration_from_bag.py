#!/usr/bin/env python2

from __future__ import print_function  # Necessary to pass print as argument in Python2

import argparse
import rospy
import rosbag

from agribot_common.tools.imu_calibration.imu_calibration import ImuCalibration


class ImuCalibrationFromBag(ImuCalibration):
    def __init__(self):
        super(ImuCalibrationFromBag, self).__init__(print)

    def collect_data(self, imu_topic, bag_path):
        self.logger('[ImuCalibration] Data collection from bag started...')

        with rosbag.Bag(bag_path) as inbag:
            for topic, msg, _ in inbag.read_messages(topics=[imu_topic]):
                if topic == imu_topic:
                    self.x_gyro_list.append(msg.angular_velocity.x)
                    self.y_gyro_list.append(msg.angular_velocity.y)
                    self.z_gyro_list.append(msg.angular_velocity.z)
                    self.x_acc_list.append(msg.linear_acceleration.x)
                    self.y_acc_list.append(msg.linear_acceleration.y)
                    self.z_acc_list.append(msg.linear_acceleration.z)

        self.logger(
            '[ImuCalibration] Finished collecting data from {} bag...'.format(
                bag_path))


if __name__ == '__main__':
    try:
        PARSER = argparse.ArgumentParser(
            description='IMU calibration from bag')

        PARSER.add_argument('-i',
                            metavar='INPUT_BAGFILE',
                            required=True,
                            help='input bagfile')
        PARSER.add_argument('-t',
                            metavar='IMU_TOPIC',
                            required=False,
                            default='/agribot/imu/raw/data',
                            help='IMU topic')
        ARGS = PARSER.parse_args()

        INBAG_PATH = ARGS.i
        TOPIC = ARGS.t

        # Initialize
        ICFB = ImuCalibrationFromBag()

        # Collect data and compute parameters
        ICFB.collect_data(TOPIC, INBAG_PATH)
        ICFB.compute_offsets()

        # Show and save parameters
        ICFB.print_offsets()
        ICFB.save_offsets_to_yaml('./imu_bias_from_bag.yaml')

    except rospy.ROSInterruptException:
        pass
