#!/usr/bin/env python2

from __future__ import print_function  # Necessary to pass print as argument in Python2

import argparse
import rospy
import rosbag

from agribot_common.tools.mag_calibration.magnetometer_calibration import MagnetometerCalibration


class MagnetometerCalibrationFromBag(MagnetometerCalibration):
    def __init__(self, magnitude, previous_offset=None, previous_scale=None):
        super(MagnetometerCalibrationFromBag,
              self).__init__(print, magnitude, previous_offset, previous_scale)

    def collect_data(self, magnetometer_topic, bag_path):
        self.logger(
            '[MagnetometerCalibration] Data collection from bag started...')

        with rosbag.Bag(bag_path) as inbag:
            for topic, msg, _ in inbag.read_messages(
                    topics=[magnetometer_topic]):
                if topic == magnetometer_topic:
                    self.x_list.append(msg.magnetic_field.x)
                    self.y_list.append(msg.magnetic_field.y)
                    self.z_list.append(msg.magnetic_field.z)

        self.logger(
            '[MagnetometerCalibration] Finished collecting data from {} bag...'
            .format(bag_path))


if __name__ == '__main__':
    try:
        PARSER = argparse.ArgumentParser(
            description='Magnetometer calibration from bag')

        PARSER.add_argument('-i',
                            metavar='INPUT_BAGFILE',
                            required=True,
                            help='input bagfile')
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

        INBAG_PATH = ARGS.i
        TOPIC = ARGS.t
        MAGNITUDE = float(ARGS.m)
        PP_FILEPATH = ARGS.pp

        if PP_FILEPATH is not None:
            PREV_OFFSET, PREV_SCALE = MagnetometerCalibration.load_previous_parameters_from_file(
                PP_FILEPATH)
            MCFB = MagnetometerCalibrationFromBag(MAGNITUDE, PREV_OFFSET,
                                                  PREV_SCALE)
        else:
            MCFB = MagnetometerCalibrationFromBag(MAGNITUDE)

        # Collect data and compute parameters
        MCFB.collect_data(TOPIC, INBAG_PATH)
        MCFB.compute_parameters()

        # Show and save parameters
        MCFB.print_parameters()
        MCFB.save_parameters_to_yaml('./mag_bias_from_bag.yaml')

        # Compute and plot additional data
        MCFB.compute_corrected_data()
        MCFB.plot_data()
    except rospy.ROSInterruptException:
        pass
