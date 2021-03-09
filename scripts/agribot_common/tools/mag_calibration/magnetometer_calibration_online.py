#!/usr/bin/env python2

import argparse
import rospy
from sensor_msgs.msg import MagneticField

from agribot_common.tools.mag_calibration.magnetometer_calibration import MagnetometerCalibration


class MagnetometerCalibrationOnline(MagnetometerCalibration):
    def __init__(self, magnitude, previous_offset=None, previous_scale=None):
        super(MagnetometerCalibrationOnline,
              self).__init__(rospy.loginfo, magnitude, previous_offset,
                             previous_scale)

    def magnetometer_cb(self, mag_msg):
        self.x_list.append(mag_msg.magnetic_field.x)
        self.y_list.append(mag_msg.magnetic_field.y)
        self.z_list.append(mag_msg.magnetic_field.z)

    def collect_data(self, magnetometer_topic):
        # Collect data until Ctrl-C is pressed
        # Ctrl-C is catched with try-except, so it doesn't stop the program
        try:
            magnetometer_sub = rospy.Subscriber(magnetometer_topic,
                                                MagneticField,
                                                self.magnetometer_cb,
                                                queue_size=100)
            self.logger(
                '[MagnetometerCalibration] Data collection online started...')
            self.logger(
                '[MagnetometerCalibration] Press Ctrl-C to stop logging and compute parameters...'
            )
            rospy.spin()  # Data is collected in magnetometer_cb
        except KeyboardInterrupt:
            self.logger('[MagnetometerCalibration] Data collection stopped...')
            magnetometer_sub.unregister()


if __name__ == '__main__':
    try:
        PARSER = argparse.ArgumentParser(
            description='Magnetometer calibration from bag')

        PARSER.add_argument('-t',
                            metavar='MAGNETOMETER_TOPIC',
                            required=False,
                            default='/agribot/imu/raw/mag',
                            help='Magnetometer topic')
        PARSER.add_argument('-m',
                            metavar='MAGNETOMETER_MAGNITUDE',
                            required=False,
                            default=4.9714e-5,
                            help='Magnetometer magnitude')
        PARSER.add_argument(
            '-pp',
            metavar='PREVIOUS_PARAMETERS',
            required=False,
            default=None,
            help='Previous parameters (parameters set when bag was logged)')
        ARGS = PARSER.parse_args()

        TOPIC = ARGS.t
        MAGNITUDE = float(ARGS.m)
        PP_FILEPATH = ARGS.pp

        # Initialize
        rospy.init_node('magnetometer_calibration')

        if PP_FILEPATH is not None:
            PREV_OFFSET, PREV_SCALE = MagnetometerCalibration.load_previous_parameters_from_file(
                PP_FILEPATH)
            MCO = MagnetometerCalibrationOnline(MAGNITUDE, PREV_OFFSET,
                                                PREV_SCALE)
        else:
            MCO = MagnetometerCalibrationOnline(MAGNITUDE)

        # Collect data and compute parameters
        MCO.collect_data(TOPIC)
        MCO.compute_parameters()

        # Show and save parameters
        MCO.print_parameters()
        MCO.save_parameters_to_yaml('./mag_bias_online.yaml')

        # Compute and plot additional data
        MCO.compute_corrected_data()
        MCO.plot_data()
    except rospy.ROSInterruptException:
        pass
