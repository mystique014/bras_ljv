#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 23:06:51 2022

@author: Quentin Duchemin
"""

import plotly.graph_objects as go
import numpy as np
import os
os.sys.path.append('../')
from pages.robot import *

from scipy.spatial import ConvexHull, Delaunay

size = 50
points_admissibles = []
robot = Robot()

x_ = np.linspace(0, 300, size)
z_ = np.linspace(0, 90, size)
for i, z in enumerate(z_):
    print(i)
    count = 0
    found = 0
    sol, dic = robot.compute_path(0, 0, z, step_bras1=0.1)
    while found<2 and count+1<len(x_):
        count += 1
        x = x_[count]
        sol, dic = robot.compute_path(x, 0, z, step_bras1=0.1)
        if sol:
            if found == 0:
                found += 1
            elif found == 1:
                lstheta = np.linspace(0, 2*np.pi, 100)
                print(z, x)
                points_admissibles += list([[np.cos(theta)*x, x*np.sin(theta), z] for theta in lstheta])                
        else:
            if found == 1:
                found += 1
                
    # if found != 2:
    #     assert False

points_admissibles = np.array(points_admissibles)
points_admissibles = points_admissibles[np.where(points_admissibles[:,1]<=0)[0],:]
np.save('points_admissibles.npy', points_admissibles)

ls_points_admis = points_admissibles[ConvexHull(points_admissibles).vertices]
delaunayin = Delaunay(ls_points_admis)
np.save('cvx_hull_points_admissibles.npy', ls_points_admis)
np.save('delaunay_admissibles_points.npy', delaunayin)



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


x1 = np.linspace(-200, 200, 50) 
y1 = np.linspace(-200, 200, 50) 
z1 = np.linspace(0, 90, size) 
  
X, Y, Z = np.meshgrid(x1, y1, z1)

values = np.zeros(len(X.flatten()))
for i, z in enumerate(z1):
    print(i)
    count = 0
    found = 0
    sol, dic = robot.compute_path(0, 0, z, step_bras1=0.1)
    while found<2 and count+1<len(x_):
        count += 1
        x = x_[count]
        sol, dic = robot.compute_path(x, 0, z, step_bras1=0.1)
        if sol:
            if found == 0:
                found += 1
                xmin = x
        else:
            if found == 1:
                xmax = x
                found += 1

    idx = np.where(((xmin<=X.flatten())*(X.flatten()<=xmax)*(Z.flatten()==z)))[0]
    values[idx] =  1
np.save('xgrid.npy', X.flatten())
np.save('ygrid.npy', Y.flatten())
np.save('zgrid.npy', Z.flatten())
np.save('valuesgrid.npy', np.array(values))

