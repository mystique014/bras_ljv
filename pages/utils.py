#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Quentin Duchemin <qduchemin9@gmail.com>
# Licensed under the Creative Commons Attribution-ShareAlike License 4.0 (International) (CC-BY-SA 4.0) -https://creativecommons.org/licenses/by-sa/4.0/

import numpy as np
colors = ['blue', 'red', 'brown', 'black', 'purple']
key2channel = {'pivot':0, 'bras1':1, 'bras2':3, 'bras3':4, 'pince':5, 'pompe':6}
lengths = [84.3, 45.5, 25.8, 104.3, 16.65, 135.75, 28.45, 27.5, 48.15, 10]
min_angles = {'pivot': 0, 'bras1':30, 'bras2':70, 'bras3':0, 'pince':0}
max_angles = {'pivot': 180, 'bras1':120, 'bras2':110, 'bras3':110, 'pince':180}
etalonnage = {'pivot': -7, 'bras1': 0, 'bras2': 0, 'bras3': 45, 'pince':0}

min_imp = {'pivot': 500, 'bras1': 500, 'bras2': 500, 'bras3': 500, 'pince': 500, 'pompe': 500}
max_imp = {'pivot': 2500, 'bras1': 2500, 'bras2': 2500, 'bras3': 2500, 'pince': 2500, 'pompe': 2500}



def dcos(a):
    return np.cos(np.deg2rad(a))

def dsin(a):
    return np.sin(np.deg2rad(a))

def corr(a,b):
    """Computes the correlation between two 1D-vectors"""
    return np.vdot(a,b)/ (np.linalg.norm(a)*np.linalg.norm(b))

def in_hull(p, hull):
    """
    Test if points in `p` are in `hull`

    `p` should be a `NxK` coordinates of `N` points in `K` dimensions
    `hull` is either a scipy.spatial.Delaunay object or the `MxK` array of the 
    coordinates of `M` points in `K`dimensions for which Delaunay triangulation
    will be computed
    """
    from scipy.spatial import Delaunay
    if not isinstance(hull,Delaunay):
        hull = Delaunay(hull)

    return hull.find_simplex(p)>=0