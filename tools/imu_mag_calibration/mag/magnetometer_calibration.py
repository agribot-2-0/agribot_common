#!/usr/bin/env python2

import yaml
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class MagnetometerCalibration(object):
    def __init__(self,
                 logger,
                 magnitude,
                 previous_offset=None,
                 previous_scale=None):
        self.logger = logger

        self.magnitude = magnitude

        self.x_list = []
        self.y_list = []
        self.z_list = []

        self.hard_corrected_x_list = []
        self.hard_corrected_y_list = []
        self.hard_corrected_z_list = []

        self.corrected_x_list = []
        self.corrected_y_list = []
        self.corrected_z_list = []

        self.previous_offset = previous_offset
        self.previous_scale = previous_scale

        self.offset = {}
        self.scale = {}

    def compute_parameters(self):
        min_dict = {
            'x': min(self.x_list),
            'y': min(self.y_list),
            'z': min(self.z_list)
        }
        max_dict = {
            'x': max(self.x_list),
            'y': max(self.y_list),
            'z': max(self.z_list)
        }

        if self.previous_offset is not None and self.previous_scale is not None:
            min_dict, max_dict = self.include_previous_parameters(
                min_dict, max_dict)

        # Hard iron distortion filtration
        self.compute_hard_iron_parameters(min_dict, max_dict)

        # Soft iron distortion filtration
        self.compute_soft_iron_parameters(min_dict, max_dict)

    def include_previous_parameters(self, min_dict, max_dict):
        self.logger(
            '\n\n[IMPORTANT!!!] Previous parameters loaded. Calculating new parameters with respect to the previous ones\n\n'
        )
        min_dict['x'] /= self.previous_scale['x']
        min_dict['x'] -= self.previous_offset['x']
        min_dict['y'] /= self.previous_scale['y']
        min_dict['y'] -= self.previous_offset['y']
        min_dict['z'] /= self.previous_scale['z']
        min_dict['z'] -= self.previous_offset['z']

        max_dict['x'] /= self.previous_scale['x']
        max_dict['x'] -= self.previous_offset['x']
        max_dict['y'] /= self.previous_scale['y']
        max_dict['y'] -= self.previous_offset['y']
        max_dict['z'] /= self.previous_scale['z']
        max_dict['z'] -= self.previous_offset['z']

        return min_dict, max_dict

    def compute_hard_iron_parameters(self, min_dict, max_dict):
        self.offset['x'] = -(max_dict['x'] + min_dict['x']) / 2
        self.offset['y'] = -(max_dict['y'] + min_dict['y']) / 2
        self.offset['z'] = -(max_dict['z'] + min_dict['z']) / 2

    def compute_soft_iron_parameters(self, min_dict, max_dict):
        delta_x = (max_dict['x'] - min_dict['x']) / 2
        delta_y = (max_dict['y'] - min_dict['y']) / 2
        delta_z = (max_dict['z'] - min_dict['z']) / 2

        self.scale['x'] = self.magnitude / delta_x
        self.scale['y'] = self.magnitude / delta_y
        self.scale['z'] = self.magnitude / delta_z

    def print_parameters(self):
        self.logger('offset_x: {}'.format(self.offset['x']))
        self.logger('offset_y: {}'.format(self.offset['y']))
        self.logger('offset_z: {}'.format(self.offset['z']))
        self.logger('scale_x: {}'.format(self.scale['x']))
        self.logger('scale_y: {}'.format(self.scale['y']))
        self.logger('scale_z: {}'.format(self.scale['z']))

    def save_parameters_to_yaml(self, file_path):
        magnetometer_offset_dict = {
            'x': self.offset['x'],
            'y': self.offset['y'],
            'z': self.offset['z']
        }
        magnetometer_scale_dict = {
            'x': self.scale['x'],
            'y': self.scale['y'],
            'z': self.scale['z']
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
            self.corrected_x_list.append(self.apply_correction(x, 'x'))

        for y in self.y_list:
            self.corrected_y_list.append(self.apply_correction(y, 'y'))

        for z in self.z_list:
            self.corrected_z_list.append(self.apply_correction(z, 'z'))

    def apply_correction(self, value, axis):
        corrected_value = value
        if self.previous_offset is not None and self.previous_scale is not None:
            corrected_value /= self.previous_scale[axis]
            corrected_value -= self.previous_offset[axis]

        corrected_value += self.offset[axis]
        corrected_value *= self.scale[axis]

        return corrected_value

    def plot_data(self):
        # Raw data
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(2, 1, 1)
        ax1.plot(self.x_list, self.y_list, 'r.')
        ax1.plot(self.x_list, self.z_list, 'b.')
        ax1.plot(self.y_list, self.z_list, 'c.')
        ax1.set(xlabel='', ylabel='', title='Raw magnetometer data.')
        ax1.grid()

        ax2 = fig1.add_subplot(2, 1, 2)
        ax2.plot(self.corrected_x_list, self.corrected_y_list, 'r.')
        ax2.plot(self.corrected_x_list, self.corrected_z_list, 'b.')
        ax2.plot(self.corrected_y_list, self.corrected_z_list, 'c.')
        ax2.set(xlabel='',
                ylabel='',
                title='After soft and hard iron distortion filtration.')
        ax2.grid()

        fig2 = plt.figure()

        ax3 = fig2.add_subplot(1, 1, 1, projection='3d')
        ax3.plot(self.x_list,
                 self.y_list,
                 self.z_list,
                 'r.',
                 label='Before filtration')
        ax3.plot(self.corrected_x_list,
                 self.corrected_y_list,
                 self.corrected_z_list,
                 'b.',
                 label='After filtration')
        ax3.set(xlabel='', ylabel='', title='3D before and after filtration')
        ax3.legend()
        ax3.grid()

        plt.show()

    @staticmethod
    def load_previous_parameters_from_file(filepath):
        with open(filepath) as file:
            parameters_dict = yaml.load(file)
            offset_dict = parameters_dict['hal/hydrabox/imu_bias'][
                'magnetometer_offset']
            scale_dict = parameters_dict['hal/hydrabox/imu_bias'][
                'magnetometer_scale']
            return offset_dict, scale_dict
