#!/usr/bin/env python2

# Fill these values
min_z = -0.000143
max_z = -2.85e-5

magnitude_z = 4.5804e-5

offset = -(max_z + min_z) / 2.0
scale = (2.0 * magnitude_z) / (max_z - min_z)

print('Offset: {}'.format(offset))
print('Scale: {}'.format(scale))
