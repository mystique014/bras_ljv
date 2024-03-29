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
    

    def draw_shape(self, r, h, a, color='blue', name=None, showlegend=None, legendgroup=None, scale_opacity=1):
        """
        parametrize the cylinder of radius r, height h, base point a
        """
        corners = np.zeros((2*20, 3))
        count = 0
        lsthetas = np.linspace(0,2*np.pi, 20)
        for theta in lsthetas:
            corners[count,0] = r*np.cos(theta)
            corners[count,1] = r*np.sin(theta)
            corners[count,2] = h
            count += 1
        for theta in lsthetas:
            corners[count,0] = r*np.cos(theta)
            corners[count,1] = r*np.sin(theta)
            corners[count,2] = 0
            count += 1

        for i in range(3):
            corners[:,i] += a[i]*np.ones(40)
        return [go.Mesh3d(x=corners[:,0],y=corners[:,1],z=corners[:,2], name=name, legendgroup=legendgroup, showlegend=showlegend,  alphahull = 0, color=color, opacity=0.55*scale_opacity)]



            
    def draw_current_shapes(self, showlegend=None, color_begin='blue', color_end='orange'):
        data_current = self.draw_shape(self.r, self.h, np.array([self.ex, self.ey, self.ez]), showlegend=showlegend, name="Positions d'arrivée", legendgroup="arrivee", color=color_end, scale_opacity=0.3)
        data_current += self.draw_shape(self.r, self.h, np.array([self.bx, self.by, self.bz]), showlegend=showlegend, name="Positions des pièces", legendgroup="depart", color=color_begin)
        return data_current
    

    def draw_current_tracked_shape(self, extreme_point, P, pince=0, showlegend=None, color_begin='blue', color_end='orange'):
        # P: matrice de changement de base de la base cartésienne à la base souhaitée

        extreme_point = extreme_point-self.h*P[:,2]
        data_current = self.draw_shape(self.r, self.h, np.array([self.ex, self.ey, self.ez]), name="Positions d'arrivée", showlegend=showlegend, legendgroup="arrivee", color=color_end)

        corners = np.zeros((2*20, 3))
        count = 0
        lsthetas = np.linspace(0, 2*np.pi, 20)
        for theta in lsthetas:
            corners[count,0] = self.r*np.cos(theta)
            corners[count,1] = self.r*np.sin(theta)
            corners[count,2] = self.h
            count += 1
        for theta in lsthetas:
            corners[count,0] = self.r*np.cos(theta)
            corners[count,1] = self.r*np.sin(theta)
            corners[count,2] = 0
            count += 1

        res = P @ corners.T + np.tile(extreme_point.reshape(3,1), (1,40))

        data_current.append(go.Mesh3d(x=res[0,:],y=res[1,:],z=res[2,:], name="Positions des pièces", legendgroup="depart", showlegend=showlegend, alphahull = 0, color=color_begin))
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
    
            
    def draw_shape(self, theta, longueur, largeur, h, a, color='blue', showlegend=None, name=None, legendgroup=None, scale_opacity=1):
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
        return [go.Mesh3d(x=corners[:,0],y=corners[:,1],z=corners[:,2], name=name, legendgroup=legendgroup, showlegend=showlegend, alphahull = 0, color=color, opacity=0.55*scale_opacity)]
        
    
            
    def draw_current_shapes(self, showlegend=None, color_begin='blue', color_end='orange'):
        data_current = self.draw_shape(self.theta, self.longueur, self.largeur, self.h, np.array([self.ex, self.ey, self.ez]), showlegend=showlegend, name="Positions d'arrivée", legendgroup="arrivee", color=color_end, scale_opacity=0.3)
        data_current += self.draw_shape(self.theta, self.longueur, self.largeur, self.h, np.array([self.bx, self.by, self.bz]), showlegend=showlegend, name="Positions des pièces", legendgroup="depart", color=color_begin)
        return data_current
    

    
    def draw_current_tracked_shape(self, extreme_point, P, pince=0, showlegend=None, color_begin='blue', color_end='orange'):
        # P: matrice de changement de base de la base cartésienne à la base souhaitée
        
        extreme_point = extreme_point-self.h*P[:,2]
        data_current = self.draw_shape(self.theta, self.longueur, self.largeur, self.h, np.array([self.ex, self.ey, self.ez]), showlegend=showlegend, name="Positions d'arrivée", legendgroup="arrivee", color=color_end)
        
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
        
        data_current.append(go.Mesh3d(x=res[0,:],y=res[1,:],z=res[2,:], name="Positions des pièces", legendgroup="depart", showlegend=showlegend, alphahull = 0, color=color_begin))
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
            
            
           
    def draw_current_shapes(self, showlegend=None, color_begin='blue', color_end='orange'):
        return self.shape.draw_current_shapes(showlegend=showlegend, color_begin=color_begin, color_end=color_end)

    
    def draw_current_tracked_shape(self, extreme_point, P, pince=0, showlegend=None, color_begin='blue', color_end='orange'):
        # P: matrice de changement de base de la base cartésienne à la base souhaitée
        if self.shape_type=='Rectangle':
            # if the shape is a rectangle, we take into account the value of the 'pince' in order to ajust the orientation of the shape
            return self.shape.draw_current_tracked_shape(extreme_point, P, pince=pince, showlegend=showlegend, color_begin=color_begin, color_end=color_end)
        else:
            return self.shape.draw_current_tracked_shape(extreme_point, P, showlegend=showlegend, color_begin=color_begin, color_end=color_end)

        
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
        