#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Quentin Duchemin <qduchemin9@gmail.com>
# Licensed under the Creative Commons Attribution-ShareAlike License 4.0 (International) (CC-BY-SA 4.0) -https://creativecommons.org/licenses/by-sa/4.0/


import numpy as np
import plotly.graph_objects as go
import time

from pages.utils import *
from pulp import *



class Robot:
    def __init__(self, input=None, scale=1, reel_actif=True):
        self.scale = scale
        self.color_arrivee = 'green'
        self.default_extreme_point = [100, -80, 30]
        sol, self.DEFAULT_PARAMS = self.compute_path(self.default_extreme_point[0], self.default_extreme_point[1], self.default_extreme_point[2])
        self.extreme_point = self.default_extreme_point
        if input is None:
            for key, value in self.DEFAULT_PARAMS.items():
                setattr(self, key, value)
        else:
            for key, value in input.items():
                setattr(self, key, value)
        self.frame = 0
        self.maxframe = 5
        self.fig = go.Figure({'data': []})
        self.trace = []
        self.save = []    
        self.is_playing = False
        self.idx_playing = 0
        self.ghost_pose = {}
        self.sx, self.sy, self.sz = 0, 0, 0
        self.sauve_auto = True
        self.reel_actif = reel_actif
        self.first_callback = True
        self.show_point = True
        self.id_tracked_shape = None
        self.ls_shapes_playing = []
        

    def show_points_admissibles(self, ls, opacity=0.1, color='blue'):
        return go.Mesh3d(x=ls[:, 0], 
                                y=ls[:, 1], 
                                z=ls[:, 2], 
                                color=color, 
                                opacity=opacity,
                                alphahull=0)
   
    def show_point_end(self, sx, sy, sz, color='blue'):
        return go.Scatter3d(x=[sx], y=[sy], z=[sz], name="Point d'arrivée", mode='markers',
                marker=dict(
                    color=color,  # set color to an array/list of desired values
                    opacity=0.8
                ), showlegend=True)
                              
    def dic2vars(self, input):
        return input['pivot'], input['bras1'], input['bras2'], input['bras3'], input['pince'], input['pompe']
    
    def vars2dic(self, piv, b1, b2, b3, pince, pompe):
        return {'pivot':piv, 'bras1':b1, 'bras2':b2, 'bras3':b3, 'pince':pince, 'pompe':pompe} 
    
    def pose(self):
        return self.vars2dic(self.pivot, self.bras1, self.bras2, self.bras3, self.pince, self.pompe)
    
    def mean_pose(self, input1, input2):
        piv, b1, b2, b3, pince, pompe_val = self.dic2vars(input1)
        pivb, b1b, b2b, b3b, pinceb, pompe_valb = self.dic2vars(input2)
        b = self.frame / self.maxframe
        a = 1-b
        return self.vars2dic( (a*piv+b*pivb), (a*b1+b*b1b), (a*b2+b*b2b), (a*b3+b*b3b), (a*pince+b*pinceb), pompe_val)
    

    def update_structure(self, input):
        # update the structure of the robot
        self.pivot = input.get("pivot")
        self.bras1 = input.get("bras1")
        self.bras2 = input.get("bras2")
        self.bras3 = input.get("bras3")
        self.pince = input.get("pince")
        self.pompe = input.get("pompe")
        
    def pompe_is_changed(self):
        if self.save[self.idx_playing]['pompe'] != self.save[self.idx_playing+1]['pompe']:
            return True
        else:
            return False

    def add(self, start, end, maxx, maxy, maxz, idxcolor=0, name = None, showlegend=False):
        start = self.scale * np.array(start)
        end = self.scale * np.array(end)
        self.fig.add_trace(
            go.Scatter3d(
                x=[start[0],end[0]],
                y=[start[1],end[1]],
                z=[start[2],end[2]],
                mode="lines",
                line={"width": 4, "color": colors[idxcolor]},
                name = name,
                showlegend = showlegend
            )
        )
        return np.max([maxx,np.abs(start[0]),np.abs(end[0])]),np.max([maxy,np.abs(start[1]),np.abs(end[1])]), np.max([maxz,np.abs(start[2]),np.abs(end[2])])
    
    def draw(self):
        self.fig.data = []
        maxx, maxy, maxz = 0,0,0
        # note order does matter
                
        start, end = np.array([0,0,0]), np.array([0,0,lengths[0]])
        maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=0, name='Socle', showlegend=True)
        start, end = end, np.array([dcos(self.pivot)*lengths[1], dsin(self.pivot)*lengths[1], lengths[0]])
        maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=0)
        start, end = end, end + np.array([dcos(self.pivot-90)*lengths[2], dsin(self.pivot-90)*lengths[2], 0])
        maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=0)
        if self.bras1<90:
            start, end = end, end + np.array([dsin(-self.bras1+90)*dcos(self.pivot)*lengths[3], dsin(-self.bras1+90)*dsin(self.pivot)*lengths[3], dcos(-self.bras1+90)*lengths[3]])
            maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=1, name='Bras 1', showlegend=True)
        else:
            start, end = end, end + np.array([dsin(self.bras1-90)*dcos(self.pivot-180)*lengths[3], dsin(self.bras1-90)*dsin(self.pivot-180)*lengths[3], dcos(self.bras1-90)*lengths[3]])
            maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=1, name='Bras 1', showlegend=True)
        start, end = end, end + np.array([dcos(self.pivot+90)*lengths[4], dsin(self.pivot+90)*lengths[4], 0])
        maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=2, name='Bras 2', showlegend=True)
        start, end = end, end + np.array([dsin(90+self.bras1-self.bras2)*dcos(180+self.pivot)*lengths[5], dsin(90+self.bras1-self.bras2)*dsin(180+self.pivot)*lengths[5], dcos(90+self.bras1-self.bras2)*lengths[5]])
        maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=2)
        start, end = end, end + np.array([dsin(90+self.bras1-self.bras2-self.bras3)*dcos(180+self.pivot)*lengths[6], dsin(90+self.bras1-self.bras2-self.bras3)*dsin(180+self.pivot)*lengths[6], dcos(90+self.bras1-self.bras2-self.bras3)*lengths[6]])
        maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=3, name='Bras 3', showlegend=True)
        start, end = end, end + np.array([dsin(180+self.bras1-self.bras2-self.bras3)*dcos(180+self.pivot)*(lengths[7]+lengths[8]), dsin(180+self.bras1-self.bras2-self.bras3)*dsin(180+self.pivot)*(lengths[7]+lengths[8]), dcos(180+self.bras1-self.bras2-self.bras3)*(lengths[7]+lengths[8])])
        maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=3, name='Bras 3', showlegend=False)
        d = max(maxx,maxy)
        self.fig.update_layout(
            scene=dict(
                xaxis=dict(
                    nticks=4,
                    range=[-d-10, d+10],
                ),
                yaxis=dict(
                    nticks=4,
                    range=[-d-10, d+10],
                ),
                zaxis=dict(
                    nticks=4,
                    range=[-30, maxz+10],
                ),
            ),
            margin=dict(r=10, l=10, b=10, t=10),
        )
        self.fig.update_layout(scene_aspectmode="cube")
        return self.fig
    
    def add_2_list(self, start, end, idxcolor=0, name = None, showlegend=False, legendgroup=None, opacity=1, linewidth=10):
        return  go.Scatter3d(
                x=[start[0],end[0]],
                y=[start[1],end[1]],
                z=[start[2],end[2]],
                mode="lines",
                line={"width": linewidth, "color": colors[idxcolor]},
                name = name,
                legendgroup = legendgroup,
                opacity=opacity,
                showlegend = showlegend
            )
    
    def update_max(self, maxx, maxy, maxz, start, end):
        return np.max([maxx,np.abs(start[0]),np.abs(end[0])]),np.max([maxy,np.abs(start[1]),np.abs(end[1])]), np.max([maxz,np.abs(start[2]),np.abs(end[2])])

    def data_list(self, input, opacity=1, showlegend=True, get_final_coord=False):
        maxx, maxy, maxz = 0,0,0
        # note order does matter
        data_liste = []
        start, end = np.array([0,0,0]), np.array([0,0,lengths[0]])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
        data_liste.append(self.add_2_list(start, end, idxcolor=0, legendgroup="0", name="Socle", showlegend=showlegend, opacity=opacity))
        start, end = end, np.array([dcos(input['pivot'])*lengths[1], dsin(input['pivot'])*lengths[1], lengths[0]])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
        data_liste.append(self.add_2_list(start, end, idxcolor=0, legendgroup="0", name="Socle", showlegend=False, opacity=opacity))
        start, end = end, end + np.array([dcos(input['pivot']-90)*lengths[2], dsin(input['pivot']-90)*lengths[2], 0])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
        data_liste.append(self.add_2_list(start, end, idxcolor=0, legendgroup="0", name="Socle", showlegend=False, opacity=opacity))
        if input['bras1']<90:
            start, end = end, end + np.array([dsin(-input['bras1']+90)*dcos(input['pivot'])*lengths[3], dsin(-input['bras1']+90)*dsin(input['pivot'])*lengths[3], dcos(-input['bras1']+90)*lengths[3]])
            maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
            data_liste.append(self.add_2_list(start, end, idxcolor=1, legendgroup="1", name='Bras 1', showlegend=showlegend, opacity=opacity))
        else:
            start, end = end, end + np.array([dsin(input['bras1']-90)*dcos(input['pivot']-180)*lengths[3], dsin(input['bras1']-90)*dsin(input['pivot']-180)*lengths[3], dcos(input['bras1']-90)*lengths[3]])
            maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
            data_liste.append(self.add_2_list(start, end, idxcolor=1, legendgroup="1", name='Bras 1', showlegend=showlegend, opacity=opacity))
        start, end = end, end + np.array([dcos(input['pivot']+90)*lengths[4], dsin(input['pivot']+90)*lengths[4], 0])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
        
        data_liste.append(self.add_2_list(start, end, idxcolor=2, legendgroup="2", name='Bras 2', showlegend=showlegend, opacity=opacity))
        start, end = end, end + np.array([dsin(90+input['bras1']-input['bras2'])*dcos(180+input['pivot'])*lengths[5], dsin(90+input['bras1']-input['bras2'])*dsin(180+input['pivot'])*lengths[5], dcos(90+input['bras1']-input['bras2'])*lengths[5]])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)        
        data_liste.append(self.add_2_list(start, end, idxcolor=2, legendgroup="2", name='Bras 2', showlegend=False, opacity=opacity))
        start, end = end, end + np.array([dsin(90+input['bras1']-input['bras2']-input['bras3'])*dcos(180+input['pivot'])*lengths[6], dsin(90+input['bras1']-input['bras2']-input['bras3'])*dsin(180+input['pivot'])*lengths[6], dcos(90+input['bras1']-input['bras2']-input['bras3'])*lengths[6]])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
        data_liste.append(self.add_2_list(start, end, idxcolor=3, legendgroup="3", name='Bras 3', showlegend=showlegend, opacity=opacity))
        start, extreme_point = end, end + np.array([dsin(180+input['bras1']-input['bras2']-input['bras3'])*dcos(180+input['pivot'])*(lengths[7]+lengths[8]), dsin(180+input['bras1']-input['bras2']-input['bras3'])*dsin(180+input['pivot'])*(lengths[7]+lengths[8]), dcos(180+input['bras1']-input['bras2']-input['bras3'])*(lengths[7]+lengths[8])])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, extreme_point)
        data_liste.append(self.add_2_list(start, extreme_point, idxcolor=3, legendgroup="3", name='Bras 3', showlegend=False, opacity=opacity))
        
        start_arrow = np.copy(start)

        # pince
        # matrice de changement de base
        P = np.ones((3,3))
        P[:,2] = start_arrow-extreme_point
        vec = np.array([dsin(90-(180+input['bras1']-input['bras2']-input['bras3']))*dcos(input['pivot']), dsin(90-(180+input['bras1']-input['bras2']-input['bras3']))*dsin(input['pivot']), dcos(90-(180+input['bras1']-input['bras2']-input['bras3']))])
        P[:,1] = vec
        vec = np.array([dcos(90+input['pivot']), dsin(90+input['pivot']), 0])
        P[:,0] = vec
        P /= np.tile(np.linalg.norm(P, axis=0), (3,1))
        
        
        
        start, end = extreme_point, extreme_point + P @ np.array([dsin(input['pince'])*lengths[9], dcos(input['pince'])*lengths[9],0])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
        data_liste.append(self.add_2_list(start, end, idxcolor=4, legendgroup="4", name="pince", showlegend=showlegend, opacity=opacity, linewidth=4))
        start, end = extreme_point, extreme_point + P @ np.array([-dsin(input['pince'])*lengths[9], -dcos(input['pince'])*lengths[9],0])

        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
        data_liste.append(self.add_2_list(start, end, idxcolor=4, legendgroup="4", showlegend=False, opacity=opacity, linewidth=4))
        
        # pompe
        if input['pompe']:
            vec = start_arrow-extreme_point
            vec /= np.linalg.norm(vec)
            arrow_starting_ratio = (lengths[7]+lengths[8])/2
            arrow_tip_ratio = (lengths[7]+lengths[8])
            data_liste.append(go.Cone(
                x=[extreme_point[0] + arrow_starting_ratio*vec[0]],
                y=[extreme_point[1] + arrow_starting_ratio*vec[1]],
                z=[extreme_point[2] + arrow_starting_ratio*vec[2]],
                u=[arrow_tip_ratio*vec[0]],
                v=[arrow_tip_ratio*vec[1]],
                w=[arrow_tip_ratio*vec[2]],
                name='pompe',
                showlegend=showlegend,
                showscale=False,
                colorscale=[[0, colors[3]], [1, colors[3]]]
            ))
        
        if get_final_coord:
            return data_liste, extreme_point, P
        else:
            return data_liste, extreme_point # end is the extreme point
    
    
    def compute_path(self, sx, sy, sz, step_bras1=0.001):
        # pivi, bras1i, bras2i, bras3i, pincei = self.dic2vars(pose)        
        bras1,bras2,bras3 = 0,0,0
        norm = np.linalg.norm([sx,sy])
        phi = np.rad2deg(np.arccos(-sx/norm))
        theta = np.rad2deg(np.arcsin((lengths[2]-lengths[4])/norm))
        if sy>0 and sx>0:
            pive = -(phi+theta)
        elif sy<0 and sx<0:
            pive = (phi-theta)    
        elif sy>0 and sx<0:
            pive = -(phi+theta)    
        else:
            pive = (phi-theta) 
                
        point_end = np.array([sx,sy,sz])
        point_b2_b3 = point_end+np.array([dcos(pive)*lengths[6],dsin(pive)*lengths[6],(lengths[7]+lengths[8])])
        
        point_b1_b2 = np.array([dcos(pive)*lengths[1], dsin(pive)*lengths[1], lengths[0]])
        point_b1_b2 += np.array([dcos(pive-90)*lengths[2], dsin(pive-90)*lengths[2], 0])
        
        test_bras1 = min_angles['bras1']
        solution_found = False
        while (not(solution_found) and test_bras1<=max_angles['bras1']):
            if test_bras1<90:
                point_after_bras1 = point_b1_b2 + np.array([dsin(-test_bras1+90)*dcos(pive)*lengths[3], dsin(-test_bras1+90)*dsin(pive)*lengths[3], dcos(-test_bras1+90)*lengths[3]])
            else:
                point_after_bras1 = point_b1_b2 + np.array([dsin(test_bras1-90)*dcos(pive-180)*lengths[3], dsin(test_bras1-90)*dsin(pive-180)*lengths[3], dcos(test_bras1-90)*lengths[3]])
            point_after_bras1_deep = point_after_bras1 + np.array([dcos(pive+90)*lengths[4], dsin(pive+90)*lengths[4], 0])
            v1 = point_b1_b2-point_after_bras1
            v1 /= np.linalg.norm(v1)
            v2 = point_b2_b3-point_after_bras1_deep
            norm2 = np.linalg.norm(v2)
            v2 /= np.linalg.norm(v2)
            test_bras2 = np.rad2deg(np.arccos(np.vdot(v1,v2)))
            test_bras3 = test_bras1 - test_bras2
            if lengths[5]-0.75<=norm2<=lengths[5]+0.75 and min_angles['bras3']<=test_bras3<=max_angles['bras3'] and min_angles['bras2']<=test_bras2<=max_angles['bras2']:
                solution_found = True
                bras1 = test_bras1
                bras2 = test_bras2
                bras3 = test_bras3
            else:
                test_bras1 += step_bras1
        return solution_found, self.vars2dic(pive, bras1, bras2, bras3, 0, 0)
    
    def compute_frames(self, pose, sx, sy, sz):
        solution_found, end = self.compute_path(sx, sy, sz)
        poseb = pose.copy()
        for key, val in end.items():
            poseb = poseb.copy()
            poseb[key] = val
            self.save.append(poseb)
        self.save.append(poseb)
        
        
    def init_robot_reel(self, input, pca):
        if self.reel_actif:
            piv, b1, b2, b3, pince, pompe = self.dic2vars(input)
            pca.servo[0].angle = piv
            pca.servo[1].angle = b1
            pca.servo[3].angle = b2
            pca.servo[4].angle = b3
            pca.servo[5].angle = pince
            self.reel_pose = input     
        
    def update_structure_reel(self, input, pca):
        if self.reel_actif:
            try:
                for key in input.keys():
                    if input[key]!=self.reel_pose[key] and key!='pompe':
                        pca.servo[key2channel[key]].angle = input[key]
                self.reel_pose = input.copy()
            except:
                self.init_robot_reel(input, pca)

    def correct_release(self, direction):
        if corr(direction, np.array([0,0,1]))>=0.95:
            return True
        else:
            return False

    def conflict(self, extreme_point, P, pince):
        
        conflict = False
        eltracked = self.ls_shapes_playing[self.id_tracked_shape]
        if 'theta' in eltracked.keys():
            theta = eltracked['theta']

            L = eltracked['longueur']
            l = eltracked['largeur']

        else:
            theta = 0
            L = 2*eltracked['r']
            l = 2*eltracked['r']

        Rinv = np.zeros((3,3))
        Rinv[2,2] = 1
        Rinv[0,0] = np.cos(np.deg2rad(theta-pince))
        Rinv[1,0] = -np.sin(np.deg2rad(theta-pince))
        Rinv[0,1] = np.sin(np.deg2rad(theta-pince))
        Rinv[1,1] = np.cos(np.deg2rad(theta-pince))
        Q = Rinv @ np.linalg.inv(P)
        Abase = -Q
        bbase = -Q @ extreme_point + np.array([L/2, l/2, eltracked['h']])
        Abase = np.vstack((Abase,Q))
        bbase = np.hstack((bbase,Q @ extreme_point + np.array([L/2, l/2, 0])))
        for id_shape, el in enumerate(self.ls_shapes_playing):
            if id_shape != self.id_tracked_shape:
                A = np.copy(Abase)
                b = np.copy(bbase)
                if not('P' in el.keys()):
                    if el['shape_type'] =='Cylindre':
                        theta=0
                        L = 2*el['r']
                        l = 2*el['r']
                    elif not('P' in el.keys()):
                        theta = el['theta']
                        L = el['longueur']
                        l = el['largeur']
                    center = np.array([el['bx'], el['by'], el['bz']])
                    Q = np.array([[dcos(theta), dsin(theta), 0],[-dsin(theta),dcos(theta), 0], [0,0,1]])
                    A = np.vstack((A,Q,-Q))
                    b = np.hstack((b, Q @ center + np.array([L/2,  l/2, el['h']]),-Q @ center + np.array([L/2, l/2, 0])))
                else:
                    Q = np.linalg.inv(el['P'])
                    center = el['extreme_point']
                    A = np.vstack((A,Q,-Q))
                    b = np.hstack((b,Q @ center + np.array([L/2, l/2, 0]),-Q @ center + np.array([L/2, l/2, el['h']])))

                set_D = range(0, A.shape[0])
                set_I = range(0, A.shape[1])
    
                prob = LpProblem("intersection", LpMinimize)
                V = pulp.LpVariable.dicts("V", [0,1,2], cat='Continuous')

                # Make up an objective, let's say sum of V_i
                prob += lpSum([V[i] for i in set_I])
                prob += V[0] >= -200
                prob += V[1] >= -200
                prob += V[2] >= -30
                prob += 200 >= V[0]
                prob += 200 >= V[1]
                prob += 200 >= V[2]
                # Apply constraints
                for d in set_D:
                        prob += b[d] - lpSum([A[d][i]*V[i] for i in set_I]) >= 0

                # Solve problem
                prob.solve()

                conflict = conflict or (LpStatus[prob.status]=='Optimal')
        return conflict


# # Generate proble, & Create variables


#     def conflict(self, extreme_point, P, pince):

#         conflict = False
#         eltracked = self.ls_shapes_playing[self.id_tracked_shape]
#         if 'theta' in eltracked.keys():
#             theta = eltracked['theta']

#             L = eltracked['longueur']
#             l = eltracked['largeur']

#         else:
#             theta = 0
#             L = 2*eltracked['r']
#             l = 2*eltracked['r']

#         Rinv = np.zeros((3,3))
#         Rinv[2,2] = 1
#         Rinv[0,0] = np.cos(np.deg2rad(theta-pince))
#         Rinv[1,0] = -np.sin(np.deg2rad(theta-pince))
#         Rinv[0,1] = np.sin(np.deg2rad(theta-pince))
#         Rinv[1,1] = np.cos(np.deg2rad(theta-pince))
#         Q = Rinv @ np.linalg.inv(P)
#         Abase = -Q
#         bbase = -Q @ extreme_point + np.array([L/2, l/2, eltracked['h']])
#         Abase = np.vstack((Abase,Q))
#         bbase = np.hstack((bbase,Q @ extreme_point + np.array([L/2, l/2, 0])))
#         for id_shape, el in enumerate(self.ls_shapes_playing):
#             if id_shape != self.id_tracked_shape:
#                 A = np.copy(Abase)
#                 b = np.copy(bbase)
#                 if not('P' in el.keys()):
#                     if el['shape_type'] =='Cylindre':
#                         theta=0
#                         L = 2*el['r']
#                         l = 2*el['r']
#                     elif not('P' in el.keys()):
#                         theta = el['theta']
#                         L = el['longueur']
#                         l = el['largeur']
#                     center = np.array([el['bx'], el['by'], el['bz']])
#                     Q = np.array([[dcos(theta), dsin(theta), 0],[-dsin(theta),dcos(theta), 0], [0,0,1]])
#                     A = np.vstack((A,Q,-Q))
#                     b = np.hstack((b, Q @ center + np.array([L/2,  l/2, el['h']]),-Q @ center + np.array([L/2, l/2, 0])))
#                 else:
#                     Q = np.linalg.inv(el['P'])
#                     center = el['extreme_point']
#                     A = np.vstack((A,Q,-Q))
#                     b = np.hstack((b,Q @ center + np.array([L/2, l/2, 0]),-Q @ center + np.array([L/2, l/2, el['h']])))

#                 res = linprog(np.zeros(3), A_ub=A, b_ub=b, bounds = [(-200,200), (-200,200), (-30, 200)], method='interior-point')
#                 conflict = conflict or res['success']
#         return conflict
