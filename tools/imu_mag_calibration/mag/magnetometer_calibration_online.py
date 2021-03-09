#!/usr/bin/env python2

import argparse
import rospy
from sensor_msgs.msg import MagneticField

from magnetometer_calibration import MagnetometerCalibration


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
                '[MagnetometerCalibration] Press Ctrl-C to stop data logging and compute parameters...'
            )
            rospy.spin()  # Data is collected in magnetometer_cb
        except KeyboardInterrupt:
            self.logger('[MagnetometerCalibration] Data collection stopped...')
            magnetometer_sub.unregister()


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(
            description='Magnetometer calibration from bag')

        parser.add_argument('-t',
                            metavar='MAGNETOMETER_TOPIC',
                            required=False,
                            default='/agribot/imu/raw/mag',
                            help='Magnetometer topic')
        parser.add_argument('-m',
                            metavar='MAGNETOMETER_MAGNITUDE',
                            required=False,
                            default=4.9714e-5,
                            help='Magnetometer magnitude')
        parser.add_argument(
            '-pp',
            metavar='PREVIOUS_PARAMETERS',
            required=False,
            default=None,
            help='Previous parameters (parameters set when bag was logged)')
        args = parser.parse_args()

        topic = args.t
        magnitude = float(args.m)
        pp_filepath = args.pp

        # Initialize
        rospy.init_node('magnetometer_calibration')

        if pp_filepath is not None:
            previous_offset, previous_scale = MagnetometerCalibration.load_previous_parameters_from_file(
                pp_filepath)
            mco = MagnetometerCalibrationOnline(magnitude, previous_offset,
                                                previous_scale)
        else:
            mco = MagnetometerCalibrationOnline(magnitude)

        # Collect data and compute parameters
        mco.collect_data(topic)
        mco.compute_parameters()

        # Show and save parameters
        mco.print_parameters()
        mco.save_parameters_to_yaml('./mag_bias_online.yaml')

        # Compute and plot additional data
        mco.compute_corrected_data()
        mco.plot_data()
    except rospy.ROSInterruptException:
        pass
