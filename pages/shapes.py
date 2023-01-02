#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Quentin Duchemin <qduchemin9@gmail.com>
# Licensed under the Creative Commons Attribution-ShareAlike License 4.0 (International) (CC-BY-SA 4.0) -https://creativecommons.org/licenses/by-sa/4.0/


import numpy as np
import plotly.graph_objects as go

from pages.utils import *



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

    def save_excel_file(self, worksheet, count, shape_dic):
        worksheet.write('A1', 'x initial')
        worksheet.write('A'+str(count), shape_dic['bx'])
        worksheet.write('B1', 'y initial')
        worksheet.write('B'+str(count), shape_dic['by'])
        worksheet.write('C1', 'z initial')
        worksheet.write('C'+str(count), shape_dic['bz'])
        worksheet.write('D1', 'x final')
        worksheet.write('D'+str(count), shape_dic['ex'])
        worksheet.write('E1', 'y final')
        worksheet.write('E'+str(count), shape_dic['ey'])
        worksheet.write('F1', 'z final')
        worksheet.write('F'+str(count), shape_dic['ez'])
        worksheet.write('G1', 'hauteur')
        worksheet.write('G'+str(count), shape_dic['h'])
        worksheet.write('H1', 'rayon')
        worksheet.write('H'+str(count), shape_dic['r'])


class Rectangle():
    def __init__(self):
        self.default_params = {'bx':0, 'by':10, 'bz':10, 'ex': -10, 'ey':-10, 'ez':-10, 'theta':0, 'longueur':10, 'largeur':10, 'h':10}
        for key,val in self.default_params.items():
            setattr(self,key,val)

    def dic2vars(self, input):
        return input['bx'], input['by'], input['bz'], input['ex'], input['ey'], input['ez'], input['theta'], input['longueur'], input['largeur'], input['h']
    
            
    def draw_shape(self, theta, longueur, largeur, h, a, color='blue', scale_opacity=1):
        """
        parametrize the cylinder of radius r, height h, base point a
        """
        corners = np.zeros((8, 3))
        count = 0
        for i in [-1,1]: #x
            for j in [-1,1]: #y
                for k in [0,1]: #z
                    corners[count,0] =  i*(longueur/2)
                    corners[count,1] = j*(largeur/2)
                    corners[count,2] = k*h
                    count += 1
                    
        R = np.zeros((3,3))
        R[2,2] = 1
        R[0,0] = np.cos(np.deg2rad(theta))
        R[1,0] = np.sin(np.deg2rad(theta))
        R[0,1] = -np.sin(np.deg2rad(theta))
        R[1,1] = np.cos(np.deg2rad(theta))
        
        corners = (R@corners.T).T
        for i in range(3):
            corners[:,i] += a[i]*np.ones(8)
        return [go.Mesh3d(x=corners[:,0],y=corners[:,1],z=corners[:,2], alphahull = 0, color=color, opacity=0.55*scale_opacity)]
        
    
            
    def draw_current_shapes(self, color_begin='blue', color_end='orange'):
        data_current = self.draw_shape(self.theta, self.longueur, self.largeur, self.h, np.array([self.ex, self.ey, self.ez]), color=color_end)
        data_current += self.draw_shape(self.theta, self.longueur, self.largeur, self.h, np.array([self.bx, self.by, self.bz]), color=color_begin)
        return data_current
    

    
    def draw_current_tracked_shape(self, extreme_point, P, pince=0, color_begin='blue', color_end='orange'):
        # P: matrice de changement de base de la base cartésienne à la base souhaitée
        
        extreme_point = extreme_point-self.h*P[:,2]
        data_current = self.draw_shape(self.theta, self.longueur, self.largeur, self.h, np.array([self.ex, self.ey, self.ez]), color=color_end)
        
        corners = np.zeros((8, 3))
        count = 0
        for i in [-1,1]: #x
            for j in [-1,1]: #y
                for k in [0,1]: #z
                    corners[count,0] = i*(self.longueur/2)
                    corners[count,1] =  j*(self.largeur/2)
                    corners[count,2] =  k*self.h
                    count += 1
                    
        R = np.zeros((3,3))
        R[2,2] = 1
        R[0,0] = np.cos(np.deg2rad(self.theta-pince))
        R[1,0] = np.sin(np.deg2rad(self.theta-pince))
        R[0,1] = -np.sin(np.deg2rad(self.theta-pince))
        R[1,1] = np.cos(np.deg2rad(self.theta-pince))
        cornersT = (R@corners.T)
        
        res = P @ cornersT + np.tile(extreme_point.reshape(3,1), (1,8))
        
        data_current.append(go.Mesh3d(x=res[0,:],y=res[1,:],z=res[2,:], alphahull = 0, color=color_begin))
        return data_current
        
    def save_excel_file(self, worksheet, count, shape_dic):
        worksheet.write('A1', 'x initial')
        worksheet.write('A'+str(count), shape_dic['bx'])
        worksheet.write('B1', 'y initial')
        worksheet.write('B'+str(count), shape_dic['by'])
        worksheet.write('C1', 'z initial')
        worksheet.write('C'+str(count), shape_dic['bz'])
        worksheet.write('D1', 'x final')
        worksheet.write('D'+str(count), shape_dic['ex'])
        worksheet.write('E1', 'y final')
        worksheet.write('E'+str(count), shape_dic['ey'])
        worksheet.write('F1', 'z final')
        worksheet.write('F'+str(count), shape_dic['ez'])
        worksheet.write('G1', 'hauteur')
        worksheet.write('G'+str(count), shape_dic['h'])
        worksheet.write('H1', 'theta')
        worksheet.write('H'+str(count), shape_dic['theta'])
        worksheet.write('I1', 'longueur')
        worksheet.write('I'+str(count), shape_dic['longueur'])
        worksheet.write('J1', 'largeur')
        worksheet.write('J'+str(count), shape_dic['largeur'])
        



class Shapes():
    def __init__(self, shape_type='Cylindre'):
        self.save = []
        self.available_shapes = {'Cylindre':['r'], 'Rectangle':['longueur', 'largeur']}#, 'Obstacle':['longueur', 'largeur']}
        self.update_shape_type(shape_type)
        
    def vars2dic(self,  bx, by, bz, ex, ey, ez, rayon, hauteur, theta, longueur, largeur):
        return {'bx':bx, 'by':by, 'bz':bz, 'ex': ex, 'ey':ey, 'ez':ez, 'r':rayon, 'h':hauteur,  'theta': theta, 'largeur':largeur, 'longueur':longueur}
    

    def update_shape_type(self, shape_type):
        self.shape_type = shape_type
        if shape_type == 'Cylindre':
            self.shape = Cylindre()
        else:
            self.shape = Rectangle()
        
    def save_pose(self):
        dic =  {'shape_type': self.shape_type}
        dic.update({key:getattr(self.shape,key) for key in list(self.shape.default_params.keys())})
        self.save.append(dic)

    def show_point(self, sx, sy, sz, label, color='blue', symbol_marker='circle'):
        return go.Scatter3d(x=[sx], y=[sy], z=[sz], name=label, mode='markers',
                marker=dict(
                    color=color,  # set color to an array/list of desired values
                    opacity=0.8,
                    symbol=symbol_marker
                ), showlegend=True)
    
    def shape_catched(self, point, dir_bras, tol=10, tol_vertical=0.1):
        current_point = np.array([self.shape.bx, self.shape.by, self.shape.bz+self.shape.h])
        dir_bras /= np.linalg.norm(dir_bras)
        if np.linalg.norm(current_point-point)<=tol and dir_bras[2]>1-tol_vertical:
            return True
        else:
            return False

    def show_points_admissibles(self, ls, color='blue'):
        return go.Mesh3d(x=ls[:, 0], 
                                y=ls[:, 1], 
                                z=ls[:, 2], 
                                color="blue", 
                                opacity=0.1,
                                alphahull=0)
    def update_shape(self, input):
        try:
            if input['shape_type']!=self.shape_type:
                self.update_shape_type(input['shape_type'])
        except:
            pass
        for key in list(self.shape.default_params.keys()):
            setattr(self.shape,key,input[key])
            
            
           
    def draw_current_shapes(self, color_begin='blue', color_end='orange'):
        return self.shape.draw_current_shapes(color_begin=color_begin, color_end=color_end)

    
    def draw_current_tracked_shape(self, extreme_point, P, pince=0, color_begin='blue', color_end='orange'):
        # P: matrice de changement de base de la base cartésienne à la base souhaitée
        if self.shape_type=='Rectangle':
            return self.shape.draw_current_tracked_shape(extreme_point, P, pince=pince, color_begin=color_begin, color_end=color_end)
        else:
            return self.shape.draw_current_tracked_shape(extreme_point, P, color_begin=color_begin, color_end=color_end)

        
    def save_excel_file(self, name_exo, admis_carte, admis_exo, admis_coord):
        import xlsxwriter
         
        # Workbook() takes one, non-optional, argument
        # which is the filename that we want to create.
        workbook = xlsxwriter.Workbook('./exercices/'+name_exo+'.xlsx')
         
        # The workbook object is then used to add new
        # worksheet via the add_worksheet() method.
        worksheet = workbook.add_worksheet('Parametres')
        
        worksheet.write('A1', 'Utilisation des coordonnées cartésiennes autorisée')
        worksheet.write('A2', str(admis_carte==['show']))

        worksheet.write('C1', "Possibilité d'afficher les points admissibles dans l'exercice")
        worksheet.write('C2', str(admis_exo==['show']))
        
        worksheet.write('B1', 'Lecture possible des coordonnées cartésiennes sur la figure 3D')
        worksheet.write('B2', str(admis_coord==['show']))
        
        worksheet_cylindres = workbook.add_worksheet('Cylindres')
        worksheet_rectangles = workbook.add_worksheet('Rectangles')
        
        count_cylindres = 2
        count_rectangles = 2
        for shape_dic in self.save:
            self.update_shape(shape_dic)
            if shape_dic['shape_type'] == 'Cylindre':
                self.shape.save_excel_file(worksheet_cylindres, count_cylindres, shape_dic)
                count_cylindres += 1
            elif shape_dic['shape_type'] == 'Rectangle':
                self.shape.save_excel_file(worksheet_rectangles, count_rectangles, shape_dic)
                count_rectangles += 1
         
        # Finally, close the Excel file
        # via the close() method.
        workbook.close()