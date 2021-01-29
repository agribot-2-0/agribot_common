#!/usr/bin/env python2

import yaml
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class MagnetometerCalibration(object):
    def __init__(self, logger):
        self.logger = logger

        self.x_list = []
        self.y_list = []
        self.z_list = []

        self.hard_corrected_x_list = []
        self.hard_corrected_y_list = []
        self.hard_corrected_z_list = []

        self.hard_soft_corrected_x_list = []
        self.hard_soft_corrected_y_list = []
        self.hard_soft_corrected_z_list = []

        self.offset_x = None
        self.offset_y = None
        self.offset_z = None

        self.scale_x = None
        self.scale_y = None
        self.scale_z = None

    def compute_parameters(self):
        # Hard iron distortion filtration
        self.offset_x = (max(self.x_list) + min(self.x_list)) / 2
        self.offset_y = (max(self.y_list) + min(self.y_list)) / 2
        self.offset_z = (max(self.z_list) + min(self.z_list)) / 2

        # Soft iron distortion filtration
        avg_delta = (self.offset_x + self.offset_y + self.offset_z) / 3

        avg_delta_x = (max(self.x_list) - min(self.x_list)) / 2
        avg_delta_y = (max(self.y_list) - min(self.y_list)) / 2
        avg_delta_z = (max(self.z_list) - min(self.z_list)) / 2

        self.scale_x = avg_delta / avg_delta_x
        self.scale_y = avg_delta / avg_delta_y
        self.scale_z = avg_delta / avg_delta_z

    def print_parameters(self):
        self.logger('offset_x: {}'.format(self.offset_x))
        self.logger('offset_y: {}'.format(self.offset_y))
        self.logger('offset_z: {}'.format(self.offset_z))
        self.logger('scale_x: {}'.format(self.scale_x))
        self.logger('scale_y: {}'.format(self.scale_y))
        self.logger('scale_z: {}'.format(self.scale_z))

    def save_parameters_to_yaml(self, file_path):
        # magnetometer_offset_dict = [{'x': 'a', 'xx': 'aa'}, {'y': 'b'}]
        magnetometer_offset_dict = {
            'x': self.offset_x,
            'y': self.offset_y,
            'z': self.offset_z
        }
        magnetometer_scale_dict = {
            'x': self.scale_x,
            'y': self.scale_y,
            'z': self.scale_z
        }
        parameters_dict = {
            'hal/hydrabox/imu_bias': {
                'magnetometer_offset': magnetometer_offset_dict,
                'magnetometer_scale': magnetometer_scale_dict
            }
        }

        with open(file_path, 'w') as file:
            yaml.dump(parameters_dict, file, default_flow_style=False)

        self.logger('[MagnetometerCalibration] Parameters saved to {}'.format(
            file_path))

    def compute_corrected_data(self):
        for x in self.x_list:
            hard_corrected_x = x - self.offset_x
            hard_corrected_x = hard_corrected_x * self.scale_x
            self.hard_corrected_x_list.append(hard_corrected_x)
            self.hard_soft_corrected_x_list.append(hard_corrected_x)

        for y in self.y_list:
            hard_corrected_y = y - self.offset_y
            hard_corrected_y = hard_corrected_y * self.scale_y
            self.hard_corrected_y_list.append(hard_corrected_y)
            self.hard_soft_corrected_y_list.append(hard_corrected_y)

        for z in self.z_list:
            hard_corrected_z = z - self.offset_z
            hard_corrected_z = hard_corrected_z * self.scale_z
            self.hard_corrected_z_list.append(hard_corrected_z)
            self.hard_soft_corrected_z_list.append(hard_corrected_z)

    def plot_data(self):
        # Raw data
        fig = plt.figure()
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.plot(self.x_list, self.y_list, 'r.')
        ax1.plot(self.x_list, self.z_list, 'b.')
        ax1.plot(self.y_list, self.z_list, 'c.')
        ax1.set(xlabel='', ylabel='', title='Raw magnetometer data.')
        ax1.grid()

        ax2 = fig.add_subplot(2, 2, 2)
        ax2.plot(self.hard_corrected_x_list, self.hard_corrected_y_list, 'r.')
        ax2.plot(self.hard_corrected_x_list, self.hard_corrected_z_list, 'b.')
        ax2.plot(self.hard_corrected_y_list, self.hard_corrected_z_list, 'c.')
        ax2.set(xlabel='',
                ylabel='',
                title='After hard iron distortion filtration.')
        ax2.grid()

        ax3 = fig.add_subplot(2, 2, 3)
        ax3.plot(self.hard_soft_corrected_x_list,
                 self.hard_soft_corrected_y_list, 'r.')
        ax3.plot(self.hard_soft_corrected_x_list,
                 self.hard_soft_corrected_z_list, 'b.')
        ax3.plot(self.hard_soft_corrected_y_list,
                 self.hard_soft_corrected_z_list, 'c.')
        ax3.set(xlabel='',
                ylabel='',
                title='After soft and hard iron distortion filtration.')
        ax3.grid()

        ax4 = fig.add_subplot(2, 2, 4, projection='3d')
        ax4.plot(self.x_list, self.y_list, self.z_list, 'r.')
        ax4.set(xlabel='', ylabel='', title='3D after filtration')
        ax4.grid()

        plt.show()
