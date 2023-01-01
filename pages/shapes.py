#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Quentin Duchemin <qduchemin9@gmail.com>
# Licensed under the Creative Commons Attribution-ShareAlike License 4.0 (International) (CC-BY-SA 4.0) -https://creativecommons.org/licenses/by-sa/4.0/


import numpy as np
import plotly.graph_objects as go


class Cylindre():
    def __init__(self):
        self.default_params = {'bx':0, 'by':10, 'bz':10, 'ex': -10, 'ey':-10, 'ez':-10, 'r':10, 'h':10}
        for key,val in self.default_params.items():
            setattr(self,key,val)

    def vars2dic(self, bx, by, bz, ex, ey, ez, rayon, hauteur):
        return {'bx':bx, 'by':by, 'bz':bz, 'ex': ex, 'ey':ey, 'ez':ez, 'r':rayon, 'h':hauteur}
    
    def dic2vars(self, input):
        return input['bx'], input['by'], input['bz'], input['ex'], input['ey'], input['ez'], input['r'], input['h']
    
    def cylinder(self, r, h, a, nt=100, nv =50):
        """
        parametrize the cylinder of radius r, height h, base point a
        """
        theta = np.linspace(0, 2*np.pi, nt)
        v = np.linspace(a[2], a[2] +h, nv )
        theta, v = np.meshgrid(theta, v)
        x = r*np.cos(theta) + a[0]
        y = r*np.sin(theta) + a[1]
        z = v
        return x, y, z
    
    def boundary_circle(self, r, h, a, nt=100):
        """
        r - boundary circle radius
        h - height above xOy-plane where the circle is included
        returns the circle parameterization
        """
        theta = np.linspace(0, 2*np.pi, nt)
        x = r*np.cos(theta) + a[0]
        y = r*np.sin(theta) + a[1]
        z = (a[2]+ h)*np.ones(theta.shape)
        return x, y, z
            
    def draw_shape(self, r, h, a, color='blue', scale_opacity=1):
        """
        parametrize the cylinder of radius r, height h, base point a
        """
        x, y, z = self.cylinder(r, h, a)
        
        colorscale = [[0, color],
                     [1, color]]
        
        cyl = go.Surface(x=x, y=y, z=z,
                         showscale=False,
                         colorscale=colorscale,
                         opacity=0.5*scale_opacity)
        xb_low, yb_low, zb_low = self.boundary_circle(r, h, a)
        xb_up, yb_up, zb_up = self.boundary_circle(r, h, a)
        
        bcircles = go.Scatter3d(x = xb_low.tolist()+[None]+xb_up.tolist(),
                                y = yb_low.tolist()+[None]+yb_up.tolist(),
                                z = zb_low.tolist()+[None]+zb_up.tolist(),
                                mode ='lines',
                                line = dict(color=color, width=2),
                                opacity =0.55*scale_opacity, showlegend=False)
        
        return [cyl, bcircles]
    
    def update_shape(self, input):
        for key,val in input.items():
            setattr(self,key,val)
            
    def draw_current_shapes(self, color_begin='blue', color_end='orange'):
        data_current = self.draw_shape(self.r, self.h, np.array([self.ex, self.ey, self.ez]), color=color_end)
        data_current += self.draw_shape(self.r, self.h, np.array([self.bx, self.by, self.bz]), color=color_begin)
        return data_current
    
    
    def draw_current_shapes(self, color_begin='blue', color_end='orange'):
        data_current = self.draw_shape(self.r, self.h, np.array([self.ex, self.ey, self.ez]), color=color_end)
        data_current += self.draw_shape(self.r, self.h, np.array([self.bx, self.by, self.bz]), color=color_begin)
        return data_current    
    
    def draw_current_tracked_shape(self, extreme_point, P, color_begin='blue', color_end='orange'):
        # P: matrice de changement de base de la base cartésienne à la base souhaitée
        
        extreme_point = extreme_point-self.h*P[:,2]
        data_current = self.draw_shape(self.r, self.h, np.array([self.ex, self.ey, self.ez]), color=color_end)
        
        x, y, z = self.cylinder(self.r, self.h, np.zeros(3))
        
        n,m = x.shape
        res = P @ np.vstack((x.reshape(-1),y.reshape(-1),z.reshape(-1))) + np.tile(extreme_point.reshape(3,1), (1,n*m))
        
        
        colorscale = [[0, color_begin],
                     [1, color_begin]]
        
        cyl = go.Surface(x=res[0,:].reshape(n,m), y=res[1,:].reshape(n,m), z=res[2,:].reshape(n,m),
                         showscale=False,
                         colorscale=colorscale,
                         opacity=0.5)
    
        xb_low, yb_low, zb_low = self.boundary_circle(self.r, self.h, np.zeros(3))
        reslow = P @ np.vstack((xb_low,yb_low,zb_low)) + np.tile(extreme_point.reshape(3,1), (1,len(xb_low)))
        xb_up, yb_up, zb_up = self.boundary_circle(self.r, self.h, np.array([0,0,self.h]))
        resup = P @ np.vstack((xb_up,yb_up,zb_up)) + np.tile(extreme_point.reshape(3,1), (1,len(xb_up)))

        bcircles = go.Scatter3d(x = reslow[0,:].tolist()+[None]+resup[0,:].tolist(),
                                y = reslow[1,:].tolist()+[None]+resup[1,:].tolist(),
                                z = reslow[2,:].tolist()+[None]+resup[2,:].tolist(),
                                mode ='lines',
                                line = dict(color=color_begin, width=2),
                                opacity =0.55, showlegend=False)
           
        data_current += [cyl, bcircles]
        return data_current


    def shape_catched(self, point, dir_bras, tol=10, tol_vertical=0.1):
        current_point = np.array([self.bx, self.by, self.bz+self.h])
        dir_bras /= np.linalg.norm(dir_bras)
        if np.linalg.norm(current_point-point)<=tol and dir_bras[2]>1-tol_vertical:
            return True
        else:
            return False
        
#class Rectangle():

class Shapes(Cylindre):
    def __init__(self):
        super().__init__()
        self.save = []
        
    def save_pose(self):
        self.save.append({'bx': self.bx, 'by': self.by, 'bz': self.bz,
                          'ex': self.ex, 'ey': self.ey, 'ez': self.ez,
                          'r': self.r, 'h': self.h })
        
        
    def show_point(self, sx, sy, sz, label, color='blue', symbol_marker='circle'):
        return go.Scatter3d(x=[sx], y=[sy], z=[sz], name=label, mode='markers',
                marker=dict(
                    color=color,  # set color to an array/list of desired values
                    opacity=0.8,
                    symbol=symbol_marker
                ), showlegend=True)
    
    
    def show_points_admissibles(self, ls, color='blue'):
        return go.Mesh3d(x=ls[:, 0], 
                                y=ls[:, 1], 
                                z=ls[:, 2], 
                                color="blue", 
                                opacity=0.1,
                                alphahull=0)
    