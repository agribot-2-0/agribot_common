#!/usr/bin/env python2

import rospy
from sensor_msgs.msg import MagneticField

from magnetometer_calibration import MagnetometerCalibration


class MagnetometerCalibrationOnline(MagnetometerCalibration):
    def __init__(self):
        super(MagnetometerCalibrationOnline, self).__init__(rospy.loginfo)

    def magnetometer_cb(self, mag_msg):
        self.x_list.append(mag_msg.magnetic_field.x)
        self.y_list.append(mag_msg.magnetic_field.y)
        self.z_list.append(mag_msg.magnetic_field.z)

    def collect_data(self, magnetometer_topic):
        # Collect data until Ctrl-C is pressed
        # Ctrl-C is catched with try-except, so it doesn't stop the program
        try:
            self.magnetometer_sub = rospy.Subscriber(magnetometer_topic,
                                                     MagneticField,
                                                     self.magnetometer_cb,
                                                     queue_size=100)
            self.logger(
                '[MagnetometerCalibration] Data collection online started...')
            self.logger(
                '[MagnetometerCalibration] Press Ctrl-C to stop data logging and compute parameters...'
            )
            rospy.spin()  # Data is collected in magnetometer_cb
        except KeyboardInterrupt:
            self.logger(
                '[MagnetometerCalibration] Data collection stopped...')
            self.magnetometer_sub.unregister()


if __name__ == '__main__':
    try:
        # Provide magnetometer topic
        magnetometer_topic = '/agribot/imu/raw/mag'

        # Initialize
        rospy.init_node('magnetometer_calibration')
        mc = MagnetometerCalibrationOnline()

        # Collect data and compute parameters
        mc.collect_data(magnetometer_topic)
        mc.compute_parameters()

        # Show and save parameters
        mc.print_parameters()
        mc.save_parameters_to_yaml('./mag_bias_online.yaml')

        # Compute and plot additional data
        mc.compute_corrected_data()
        mc.plot_data()
    except rospy.ROSInterruptException:
        pass
