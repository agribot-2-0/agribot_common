#!/usr/bin/env python

from __future__ import print_function

import sys
import yaml

FILENAME = sys.argv[1]

LATITUDES = []
LONGITUDES = []

with open(FILENAME, 'r') as file_:
    DICT = dict(yaml.safe_load(file_))
    for point in DICT.itervalues():
        LATITUDES.append(point["position"][0])
        LONGITUDES.append(point["position"][1])

for i, v in enumerate(LATITUDES):
    print('{},{}'.format(LATITUDES[i], LONGITUDES[i]))
