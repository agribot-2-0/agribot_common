#!/usr/bin/env python2

from __future__ import print_function

# Fill these values
MIN_Z = -0.000143
MAX_Z = -2.85E-5

MAGNITUDE_Z = 4.5804E-5

OFFSET = -(MAX_Z + MIN_Z) / 2.0
SCALE = (2.0 * MAGNITUDE_Z) / (MAX_Z - MIN_Z)

print('Offset: {}'.format(OFFSET))
print('Scale: {}'.format(SCALE))
