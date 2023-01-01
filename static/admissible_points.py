#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 23:06:51 2022

@author: Quentin Duchemin
"""

import plotly.graph_objects as go
import numpy as np
from robot import *

from scipy.spatial import ConvexHull


size = 50
pointsin = []
pointsout = []
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
                lstheta = np.linspace(0, 2*np.pi, 100)
                pointsin += list([[np.cos(theta)*x, x*np.sin(theta), z] for theta in lstheta])
        else:
            if found == 1:
                found += 1
                lstheta = np.linspace(0, 2*np.pi, 100)
                pointsout += list([[np.cos(theta)*x, x*np.sin(theta), z] for theta in lstheta])
    # if found != 2:
    #     assert False

pointsin = np.array(pointsin)
pointsout = np.array(pointsout)
np.save('pointsin.npy', pointsin)
np.save('pointsout.npy', pointsout)


xc = pointsin[ConvexHull(pointsin).vertices]


xcout = pointsout[ConvexHull(pointsout).vertices]
fig = go.Figure(data=[go.Mesh3d(x=xc[:, 0], 
                        y=xc[:, 1], 
                        z=xc[:, 2], 
                        color="blue", 
                        opacity=0.1,
                        alphahull=0), 
                      go.Mesh3d(x=xcout[:, 0], 
                                              y=xcout[:, 1], 
                                              z=xcout[:, 2], 
                                              color="orange", 
                                              opacity=0.1,
                                              alphahull=0)
                      ])
fig.show()


# size=50
# x_ = np.linspace(-120, 120, size)
# z_ = np.linspace(0, 220, size)

# x, z = np.meshgrid(x_, z_, indexing='ij')

# mesh = np.zeros(x.shape)

# robot = Robot()

# X,Y,Z = [],[],[]

# for i in range(x.shape[0]):
#     print(i)
#     for k in range(x.shape[1]):
#         sol, dic = robot.compute_path(x[i,k], 0, z[i,k], step_bras1=0.1)
#         if sol:
            
#             X += list(x[i,k]*np.cos(np.linspace(0,2*np.pi,100)))
#             Y += list(x[i,k]*np.sin(np.linspace(0,2*np.pi,100)))
#             Z += list(z[i,k]*np.ones(100))


# points = np.array([[X[i],Y[i],Z[i]] for i in range(len(X))])
# xc = points[ConvexHull(points).vertices]
# fig = go.Figure(data=go.Mesh3d(x=xc[:, 0], 
#                         y=xc[:, 1], 
#                         z=xc[:, 2], 
#                         color="blue", 
#                         opacity=0.1,
#                         alphahull=0))
# fig.show()

