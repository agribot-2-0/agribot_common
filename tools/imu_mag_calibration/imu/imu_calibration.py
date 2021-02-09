#!/usr/bin/env python2

import yaml
from statistics import mean


class ImuCalibration(object):

    GRAVITY_OFFSET_Z = 9.807

    def __init__(self, logger):
        self.logger = logger

        self.x_acc_list = []
        self.y_acc_list = []
        self.z_acc_list = []

        self.x_gyro_list = []
        self.y_gyro_list = []
        self.z_gyro_list = []

        self.acc_offset_x = None
        self.acc_offset_y = None
        self.acc_offset_z = None

        self.gyro_offset_x = None
        self.gyro_offset_y = None
        self.gyro_offset_z = None

    def compute_offsets(self):
        self.acc_offset_x = -mean(self.x_acc_list)
        self.acc_offset_y = -mean(self.y_acc_list)
        self.acc_offset_z = -mean(self.z_acc_list) + self.GRAVITY_OFFSET_Z

        self.gyro_offset_x = -mean(self.x_gyro_list)
        self.gyro_offset_y = -mean(self.y_gyro_list)
        self.gyro_offset_z = -mean(self.z_gyro_list)

    def print_offsets(self):
        self.logger('Accelerometer offset_x: {}'.format(self.acc_offset_x))
        self.logger('Accelerometer offset_y: {}'.format(self.acc_offset_y))
        self.logger('Accelerometer offset_z: {}'.format(self.acc_offset_z))
        self.logger('Gyro offset_x: {}'.format(self.gyro_offset_x))
        self.logger('Gyro offset_y: {}'.format(self.gyro_offset_y))
        self.logger('Gyro offset_z: {}'.format(self.gyro_offset_z))

    def save_offsets_to_yaml(self, file_path):
        accelerometer_offset_dict = {
            'x': self.acc_offset_x,
            'y': self.acc_offset_y,
            'z': self.acc_offset_z
        }
        gyroscope_scale_dict = {
            'x': self.gyro_offset_x,
            'y': self.gyro_offset_y,
            'z': self.gyro_offset_z
        }
        parameters_dict = {
            'hal/hydrabox/imu_bias': {
                'accelerometer_offset': accelerometer_offset_dict,
                'gyroscope_offset': gyroscope_scale_dict
            }
        }

        with open(file_path, 'w') as outfile:
            yaml.dump(parameters_dict, outfile, default_flow_style=False)

        self.logger(
            '[ImuCalibration] Parameters saved to {}'.format(file_path))
