#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Quentin Duchemin <qduchemin9@gmail.com>
# Licensed under the Creative Commons Attribution-ShareAlike License 4.0 (International) (CC-BY-SA 4.0) -https://creativecommons.org/licenses/by-sa/4.0/

import numpy as np
colors = ['blue', 'red', 'brown', 'black', 'purple']
key2channel = {'pivot':0, 'bras1':1, 'bras2':3, 'bras3':4, 'pince':5}
lengths = [61, 45.5, 25.8, 104.3, 16.65, 135.75, 28.45, 27.5, 48.15, 10]
min_angles = {'pivot': 0, 'bras1':60, 'bras2':70, 'bras3':0, 'pince':0}
max_angles = {'pivot': 180, 'bras1':150, 'bras2':110, 'bras3':110, 'pince':180}

def dcos(a):
    return np.cos(np.deg2rad(a))

def dsin(a):
    return np.sin(np.deg2rad(a))