#!/usr/bin/env python2

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
        # Provide imu topic
        imu_topic = '/agribot/imu/raw/data'

        # Initialize
        rospy.init_node('imu_calibration')
        ic = ImuCalibrationOnline()

        # Collect data and compute parameters
        ic.collect_data(imu_topic)
        ic.compute_offsets()

        # Show and save parameters
        ic.print_offsets()
        ic.save_offsets_to_yaml('./imu_bias_online.yaml')

    except rospy.ROSInterruptException:
        pass
