import numpy as np
import plotly.graph_objects as go


colors = ['blue', 'red', 'brown', 'pink', 'purple', 'black']

def dcos(a):
    return np.cos(np.deg2rad(a))

def dsin(a):
    return np.sin(np.deg2rad(a))

class Robot:
    def __init__(self, input=None, scale=1, recording=False):
        self.scale = scale
        self.color_arrivee = 'red'
        self.default_extreme_point = [100, -60, 30]
        sol, self.DEFAULT_PARAMS = self.compute_path(self.default_extreme_point[0], self.default_extreme_point[1], self.default_extreme_point[2])
        self.extreme_point = self.default_extreme_point
        if input is None:
            for key, value in self.DEFAULT_PARAMS.items():
                setattr(self, key, value)
        else:
            for key, value in input.items():
                setattr(self, key, value)
        self.frame = 0
        self.maxframe = 10
        self.fig = go.Figure({'data': []})
        self.trace = []
        self.save = []    
        self.is_playing = False
        self.idx_playing = 0
        self.ghost_pose = {}
        self.sx, self.sy, self.sz = 0, 0, 0
        self.sauve_auto = True
        
        
        
    def show_points_admissibles(self, ls, color='blue'):
        return go.Mesh3d(x=ls[:, 0], 
                                y=ls[:, 1], 
                                z=ls[:, 2], 
                                color="blue", 
                                opacity=0.1,
                                alphahull=0)
   
    def show_point_end(self, sx, sy, sz, color='blue'):
        return go.Scatter3d(x=[sx], y=[sy], z=[sz], name="Point de d'arrivée", mode='markers',
                marker=dict(
                    color=color,  # set color to an array/list of desired values
                    opacity=0.8
                ), showlegend=True)
                              
    def dic2vars(self, input):
        return input['pivot'], input['bras1'], input['bras2'], input['bras3'], input['pince']
    
    def vars2dic(self, piv, b1, b2, b3, pince):
        return {'pivot':piv, 'bras1':b1, 'bras2':b2, 'bras3':b3, 'pince':pince} 
    
    def pose(self):
        return self.vars2dic(self.pivot, self.bras1, self.bras2, self.bras3, self.pince)
    
    def mean_pose(self, input1, input2):
        piv, b1, b2, b3, pince = self.dic2vars(input1)
        pivb, b1b, b2b, b3b, pinceb = self.dic2vars(input2)
        b = self.frame / self.maxframe
        a = 1-b
        return self.vars2dic( (a*piv+b*pivb), (a*b1+b*b1b), (a*b2+b*b2b), (a*b3+b*b3b), (a*pince+b*pinceb))
    

    def update_structure(self, input):
        # update the structure of the robot
        self.pivot = input.get("pivot") if input.get("pivot") else self.pivot
        self.bras1 = input.get("bras1") if input.get("bras1") else self.bras1
        self.bras2 = input.get("bras2") if input.get("bras2") else self.bras2
        self.bras3 = input.get("bras3") if input.get("bras3") else self.bras3
        self.pince = input.get("pince") if input.get("pince") else self.pince


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
                
        start, end = np.array([0,0,0]), np.array([0,0,61])
        maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=0, name='Socle', showlegend=True)
        start, end = end, np.array([dcos(self.pivot)*45.5, dsin(self.pivot)*45.5, 61])
        maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=0)
        start, end = end, end + np.array([dcos(self.pivot-90)*25.8, dsin(self.pivot-90)*25.8, 0])
        maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=0)
        if self.bras1<90:
            start, end = end, end + np.array([dsin(-self.bras1+90)*dcos(self.pivot)*104.3, dsin(-self.bras1+90)*dsin(self.pivot)*104.3, dcos(-self.bras1+90)*104.3])
            maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=1, name='Bras 1', showlegend=True)
        else:
            start, end = end, end + np.array([dsin(self.bras1-90)*dcos(self.pivot-180)*104.3, dsin(self.bras1-90)*dsin(self.pivot-180)*104.3, dcos(self.bras1-90)*104.3])
            maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=1, name='Bras 1', showlegend=True)
        start, end = end, end + np.array([dcos(self.pivot+90)*16.65, dsin(self.pivot+90)*16.65, 0])
        maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=2, name='Bras 2', showlegend=True)
        start, end = end, end + np.array([dsin(90+self.bras1-self.bras2)*dcos(180+self.pivot)*135.75, dsin(90+self.bras1-self.bras2)*dsin(180+self.pivot)*135.75, dcos(90+self.bras1-self.bras2)*135.75])
        maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=2)
        start, end = end, end + np.array([dsin(90+self.bras1-self.bras2-self.bras3)*dcos(180+self.pivot)*28.45, dsin(90+self.bras1-self.bras2-self.bras3)*dsin(180+self.pivot)*28.45, dcos(90+self.bras1-self.bras2-self.bras3)*28.45])
        maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=3, name='Bras 3', showlegend=True)
        start, end = end, end + np.array([dsin(180+self.bras1-self.bras2-self.bras3)*dcos(180+self.pivot)*(27.5+48.15), dsin(180+self.bras1-self.bras2-self.bras3)*dsin(180+self.pivot)*(27.5+48.15), dcos(180+self.bras1-self.bras2-self.bras3)*(27.5+48.15)])
        maxx, maxy, maxz = self.add(start, end, maxx, maxy, maxz, idxcolor=3)
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
    
    def add_2_list(self, start, end, idxcolor=0, name = None, showlegend=False, opacity=1):
        return  go.Scatter3d(
                x=[start[0],end[0]],
                y=[start[1],end[1]],
                z=[start[2],end[2]],
                mode="lines",
                line={"width": 4, "color": colors[idxcolor]},
                name = name,
                opacity=opacity,
                showlegend = showlegend
            )
    
    def update_max(self, maxx, maxy, maxz, start, end):
        return np.max([maxx,np.abs(start[0]),np.abs(end[0])]),np.max([maxy,np.abs(start[1]),np.abs(end[1])]), np.max([maxz,np.abs(start[2]),np.abs(end[2])])

    def data_list(self, input, opacity=1, showlegend=True):
        maxx, maxy, maxz = 0,0,0
        # note order does matter
        data_liste = []
        start, end = np.array([0,0,0]), np.array([0,0,61])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
        data_liste.append(self.add_2_list(start, end, idxcolor=0, name="Socle", showlegend=showlegend, opacity=opacity))
        start, end = end, np.array([dcos(input['pivot'])*45.5, dsin(input['pivot'])*45.5, 61])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
        data_liste.append(self.add_2_list(start, end, idxcolor=0, opacity=opacity))
        start, end = end, end + np.array([dcos(input['pivot']-90)*25.8, dsin(input['pivot']-90)*25.8, 0])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
        data_liste.append(self.add_2_list(start, end, idxcolor=0, opacity=opacity))
        if input['bras1']<90:
            start, end = end, end + np.array([dsin(-input['bras1']+90)*dcos(input['pivot'])*104.3, dsin(-input['bras1']+90)*dsin(input['pivot'])*104.3, dcos(-input['bras1']+90)*104.3])
            maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
            data_liste.append(self.add_2_list(start, end, idxcolor=1, name='Bras 1', showlegend=showlegend, opacity=opacity))
        else:
            start, end = end, end + np.array([dsin(input['bras1']-90)*dcos(input['pivot']-180)*104.3, dsin(input['bras1']-90)*dsin(input['pivot']-180)*104.3, dcos(input['bras1']-90)*104.3])
            maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
            data_liste.append(self.add_2_list(start, end, idxcolor=1, name='Bras 1', showlegend=showlegend, opacity=opacity))
        start, end = end, end + np.array([dcos(input['pivot']+90)*16.65, dsin(input['pivot']+90)*16.65, 0])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
        
        data_liste.append(self.add_2_list(start, end, idxcolor=2, name='Bras 2', showlegend=showlegend, opacity=opacity))
        start, end = end, end + np.array([dsin(90+input['bras1']-input['bras2'])*dcos(180+input['pivot'])*135.75, dsin(90+input['bras1']-input['bras2'])*dsin(180+input['pivot'])*135.75, dcos(90+input['bras1']-input['bras2'])*135.75])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)        
        data_liste.append(self.add_2_list(start, end, idxcolor=2, opacity=opacity))
        start, end = end, end + np.array([dsin(90+input['bras1']-input['bras2']-input['bras3'])*dcos(180+input['pivot'])*28.45, dsin(90+input['bras1']-input['bras2']-input['bras3'])*dsin(180+input['pivot'])*28.45, dcos(90+input['bras1']-input['bras2']-input['bras3'])*28.45])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
        data_liste.append(self.add_2_list(start, end, idxcolor=3, name='Bras 3', showlegend=showlegend, opacity=opacity))
        start, end = end, end + np.array([dsin(180+input['bras1']-input['bras2']-input['bras3'])*dcos(180+input['pivot'])*(27.5+48.15), dsin(180+input['bras1']-input['bras2']-input['bras3'])*dsin(180+input['pivot'])*(27.5+48.15), dcos(180+input['bras1']-input['bras2']-input['bras3'])*(27.5+48.15)])
        maxx, maxy, maxz = self.update_max(maxx, maxy, maxz, start, end)
        data_liste.append(self.add_2_list(start, end, idxcolor=3, opacity=opacity))
        return data_liste, end # end is the extreme point
    
    
    def compute_path(self, sx, sy, sz, step_bras1=0.001):
        # pivi, bras1i, bras2i, bras3i, pincei = self.dic2vars(pose)        
        bras1,bras2,bras3 = 0,0,0
        norm = np.linalg.norm([sx,sy])
        phi = np.rad2deg(np.arccos(-sx/norm))
        theta = np.rad2deg(np.arcsin((25.8-16.65)/norm))
        if sy>0 and sx>0:
            pive = -(phi+theta)
        elif sy<0 and sx<0:
            pive = (phi-theta)    
        elif sy>0 and sx<0:
            pive = -(phi+theta)    
        else:
            pive = (phi-theta) 
                
        point_end = np.array([sx,sy,sz])
        point_b2_b3 = point_end+np.array([dcos(pive)*28.45,dsin(pive)*28.45,(27.5+48.15)])
        
        point_b1_b2 = np.array([dcos(pive)*45.5, dsin(pive)*45.5, 61])
        point_b1_b2 += np.array([dcos(pive-90)*25.8, dsin(pive-90)*25.8, 0])
        
        test_bras1 = 60
        solution_found = False
        while (not(solution_found) and test_bras1<=150):
            if test_bras1<90:
                point_after_bras1 = point_b1_b2 + np.array([dsin(-test_bras1+90)*dcos(pive)*104.3, dsin(-test_bras1+90)*dsin(pive)*104.3, dcos(-test_bras1+90)*104.3])
            else:
                point_after_bras1 = point_b1_b2 + np.array([dsin(test_bras1-90)*dcos(pive-180)*104.3, dsin(test_bras1-90)*dsin(pive-180)*104.3, dcos(test_bras1-90)*104.3])
            point_after_bras1_deep = point_after_bras1 + np.array([dcos(pive+90)*16.65, dsin(pive+90)*16.65, 0])
            v1 = point_b1_b2-point_after_bras1
            v1 /= np.linalg.norm(v1)
            v2 = point_b2_b3-point_after_bras1_deep
            norm2 = np.linalg.norm(v2)
            v2 /= np.linalg.norm(v2)
            test_bras2 = np.rad2deg(np.arccos(np.vdot(v1,v2)))
            test_bras3 = test_bras1 - test_bras2
            # if test_bras1 % 10==0:
            #     print(norm2, test_bras3, test_bras2)
            if 135<=norm2<=136.5 and 0<=test_bras3<=110 and 70<=test_bras2<=110:
                print('sol found')
                solution_found = True
                bras1 = test_bras1
                bras2 = test_bras2
                bras3 = test_bras3
            else:
                test_bras1 += step_bras1
        return solution_found, self.vars2dic(pive, bras1, bras2, bras3, 0)
    
    def compute_frames(self, pose, sx, sy, sz):
        print(pose)
        self.save = [pose.copy()]
        solution_found, end = self.compute_path(sx, sy, sz)
        poseb = pose.copy()
        for key, val in end.items():
            poseb = poseb.copy()
            poseb[key] = val
            self.save.append(poseb)
        self.save.append(poseb)
        