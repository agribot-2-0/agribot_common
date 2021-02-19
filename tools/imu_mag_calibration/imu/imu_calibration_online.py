#!/usr/bin/env python2

import argparse
import rospy
from sensor_msgs.msg import Imu

from imu_calibration import ImuCalibration


class ImuCalibrationOnline(ImuCalibration):
    def __init__(self):
        super(ImuCalibrationOnline, self).__init__(rospy.loginfo)

    def imu_cb(self, imu_msg):
        self.x_gyro_list.append(imu_msg.angular_velocity.x)
        self.y_gyro_list.append(imu_msg.angular_velocity.y)
        self.z_gyro_list.append(imu_msg.angular_velocity.z)
        self.x_acc_list.append(imu_msg.linear_acceleration.x)
        self.y_acc_list.append(imu_msg.linear_acceleration.y)
        self.z_acc_list.append(imu_msg.linear_acceleration.z)

    def collect_data(self, imu_topic):
        # Collect data until Ctrl-C is pressed
        # Ctrl-C is catched with try-except, so it doesn't stop the program
        try:
            self.imu_sub = rospy.Subscriber(imu_topic,
                                            Imu,
                                            self.imu_cb,
                                            queue_size=100)
            self.logger('[ImuCalibration] Data collection online started...')
            self.logger(
                '[ImuCalibration] Press Ctrl-C to stop data logging and compute parameters...'
            )
            rospy.spin()  # Data is collected in imu_cb
        except KeyboardInterrupt:
            self.logger('[ImuCalibration] Data collection stopped...')
            self.imu_sub.unregister()


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='IMU calibration online')

        parser.add_argument('-t',
                            metavar='IMU_TOPIC',
                            required=False,
                            default='/agribot/imu/raw/data',
                            help='IMU topic')
        args = parser.parse_args()

        topic = args.t

        # Initialize
        rospy.init_node('imu_calibration')
        ico = ImuCalibrationOnline()

        # Collect data and compute parameters
        ico.collect_data(topic)
        ico.compute_offsets()

        # Show and save parameters
        ico.print_offsets()
        ico.save_offsets_to_yaml('./imu_bias_online.yaml')

    except rospy.ROSInterruptException:
        pass
