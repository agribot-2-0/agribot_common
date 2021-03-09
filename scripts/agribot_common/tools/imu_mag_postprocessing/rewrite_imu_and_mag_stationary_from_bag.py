#!/usr/bin/env python

import argparse
from distutils.util import strtobool
from statistics import mean
import rosbag


class ImuMagRewriter(object):

    GRAVITY_OFFSET_Z = 9.807

    def __init__(self, rewrite_imu, rewrite_mag, imu_topic, mag_topic):
        self.rewrite_imu = rewrite_imu
        self.rewrite_mag = rewrite_mag
        self.imu_topic = imu_topic
        self.mag_topic = mag_topic

    def rewrite(self, inbag_path, outbag_path):
        # Calculate mean magnetic field vector if necessary
        if self.rewrite_mag:
            mean_mag_field = self.calculate_mean_magnetic_field_from_bag(
                inbag_path)

        try:
            with rosbag.Bag(inbag_path) as inbag:
                with rosbag.Bag(outbag_path, 'w') as outbag:
                    for topic, msg, time in inbag.read_messages():
                        if topic == self.imu_topic and self.rewrite_imu:
                            msg.angular_velocity.x = 0.0
                            msg.angular_velocity.y = 0.0
                            msg.angular_velocity.z = 0.0
                            msg.linear_acceleration.x = 0.0
                            msg.linear_acceleration.y = 0.0
                            msg.linear_acceleration.z = self.GRAVITY_OFFSET_Z
                        elif topic == self.mag_topic and self.rewrite_mag:
                            msg.magnetic_field.x = mean_mag_field['x']
                            msg.magnetic_field.y = mean_mag_field['y']
                            msg.magnetic_field.z = mean_mag_field['z']

                        outbag.write(topic, msg, time)

            print('[Success] Bag rewritten succesfully...')
        except IOError as error:
            print(error)
        except rosbag.bag.ROSBagException as error:
            print('[Error] {}'.format(error))

    def calculate_mean_magnetic_field_from_bag(self, bag_path):
        mean_mag_field = {}
        mag_field_list_x = []
        mag_field_list_y = []
        mag_field_list_z = []

        with rosbag.Bag(bag_path) as bag:
            for topic, msg, _ in bag.read_messages():
                if topic == self.mag_topic:
                    mag_field_list_x.append(msg.magnetic_field.x)
                    mag_field_list_y.append(msg.magnetic_field.y)
                    mag_field_list_z.append(msg.magnetic_field.z)

        mean_mag_field['x'] = mean(mag_field_list_x)
        mean_mag_field['y'] = mean(mag_field_list_y)
        mean_mag_field['z'] = mean(mag_field_list_z)

        return mean_mag_field


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description='Rewrites bag with IMU and/or magnetometer stationary')

    PARSER.add_argument('-o',
                        metavar='OUTPUT_BAGFILE',
                        required=True,
                        help='Output bagfile')
    PARSER.add_argument('-i',
                        metavar='INPUT_BAGFILE',
                        required=True,
                        help='Input bagfile')
    PARSER.add_argument('-imu_topic',
                        metavar='IMU_TOPIC',
                        required=False,
                        default='/agribot/imu/raw/data',
                        help='IMU topic')
    PARSER.add_argument('-mag_topic',
                        metavar='MAGNETOMETER_TOPIC',
                        required=False,
                        default='/agribot/imu/raw/mag',
                        help='Magnetometer topic')
    PARSER.add_argument('-rewrite_imu',
                        metavar='REWRITE_IMU',
                        required=False,
                        default='True',
                        help='Rewrite IMU')
    PARSER.add_argument('-rewrite_mag',
                        metavar='REWRITE_MAG',
                        required=False,
                        default='True',
                        help='Rewrite magnetometer')
    ARGS = PARSER.parse_args()

    INBAG_PATH = ARGS.i
    OUTBAG_PATH = ARGS.o
    IMU_TOPIC = ARGS.imu_topic
    MAG_TOPIC = ARGS.mag_topic
    REWRITE_IMU = strtobool(ARGS.rewrite_imu)
    REWRITE_MAG = strtobool(ARGS.rewrite_mag)

    IMR = ImuMagRewriter(REWRITE_IMU, REWRITE_MAG, IMU_TOPIC, MAG_TOPIC)
    IMR.rewrite(INBAG_PATH, OUTBAG_PATH)
