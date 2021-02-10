#!/usr/bin/env python2

min_z = -1.2e-05
max_z = 0.000167
magnitude_z = 4.5804e-5

offset = (max_z + min_z) / 2.0
scale = (2 * magnitude_z) / (max_z - min_z)

print('Offset: {}'.format(offset))
print('Scale: {}'.format(scale))
