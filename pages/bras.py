#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Quentin Duchemin <qduchemin9@gmail.com>
# Licensed under the Creative Commons Attribution-ShareAlike License 4.0 (International) (CC-BY-SA 4.0) -https://creativecommons.org/licenses/by-sa/4.0/


import dash
from dash import dcc
from dash import html, callback, clientside_callback
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import numpy as np

from pages.robot import *
from scipy.spatial import ConvexHull, Delaunay

import time
import datetime
import dash_bootstrap_components as dbc  
import pickle

from pages.shapes import *

from pages.utils import *


dash.register_page(__name__)




# Step 2. Import the dataset

# pointsin = np.load('./static/pointsin.npy')
# pointsout = np.load('./static/pointsout.npy')
# pointsin = pointsin[np.where(pointsin[:,1]<=0)[0],:]
# pointsout = pointsout[np.where(pointsout[:,1]<=0)[0],:]
# ls_pointsin_admis = pointsin[ConvexHull(pointsin).vertices]
# ls_pointsout_admis = pointsout[ConvexHull(pointsout).vertices]
# delaunayin = Delaunay(ls_pointsin_admis)
# delaunayout = Delaunay(ls_pointsout_admis)

ls_pointsin_admis = np.load('./static/ls_pointsin_admis.npy')
ls_pointsout_admis = np.load('./static/ls_pointsout_admis.npy')
delaunayin = Delaunay(ls_pointsin_admis)
delaunayout = Delaunay(ls_pointsout_admis)


# Step 3. Create a plotly figure

fig = go.Figure(layout = { 'uirevision': 'constant'})


shape = Shapes()

shape_playing = Shapes()



try:
    from adafruit_servokit import ServoKit
    nbPCAservo = 16
    pca = ServoKit(channels=nbPCAservo)
    for key, channel in key2channel.items():
        pca.servo[channel].set_pulse_width_range(min_imp[key] , max_imp[key])
    robot = Robot(reel_actif=True)
    robot.init_robot_reel(robot.pose(), pca)
except:
    robot = Robot(reel_actif=False)
    pca = None


# if robot.reel_actif:
#     from adafruit_servokit import ServoKit
#     nbPCAservo = 16
#     pca = ServoKit(channels=nbPCAservo)
#     robot.init_robot_reel(robot.pose(), pca)
# else:
#     pca = None


Storage = dcc.Store(
        id='storage',
        data=[])
Storage_shapes = dcc.Store(
        id='storage_shapes',
        data=[])
Storage_playing = dcc.Store(
        id='storage_playing',
        data=[])
Storage_title = dcc.Store(
        id='title',
        data='')



import os
list_exos = []
for file in os.listdir("./exercices"):
    if file.endswith(".pkl"):
        list_exos.append(file[:-4])
        
        

Choice_exo = dcc.Dropdown(
   options=list_exos,
   value='mode_par_defaut',
   id="choice_exo"
)

Interval = dcc.Interval(id='graph-refresher',
                     interval=1*400,
                     n_intervals=0,
                     max_intervals=50,
                     disabled=True)
for key in min_angles.keys():
    globals()['S'+key] = dcc.Slider(min_angles[key], max_angles[key], 1, 
               marks={str(i): str(i) for i in np.arange(min_angles[key],max_angles[key],20)},
                value=getattr(robot,key), id = key, vertical=True,
                tooltip={"placement": "bottom", "always_visible": True})
Rx = dcc.Slider(-250, 250, 1, 
           marks={str(i): str(i) for i in np.arange(-200,200,100)},
           value=robot.extreme_point[0], id = 'Rx', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Ry = dcc.Slider(-300, 0, 1, 
           marks={str(i): str(i) for i in np.arange(-200,200,100)},
           value=robot.extreme_point[1], id = 'Ry', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Rz = dcc.Slider(0, 300, 1, 
           marks={str(i): str(i) for i in np.arange(0,200,50)},
           value=robot.extreme_point[2], id = 'Rz', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
admis = dcc.Checklist(
    [{"label": "Montrer les points admissibles", "value": 'show'}], value=['show'], id='admis'
)
ghost = dcc.Checklist(
    [{"label": "Montrer la position initiale du mouvement", "value": 'show'}], value=['show'], id='ghost'
)

Robot_reel = dcc.Checklist(
    [{"label": "Activer le mouvement synchronisé avec le robot réel", "value": 'show'}], value=['show'], id='robot_reel'
)

Sauve_auto = dcc.Checklist(
    [{"label": "Sauvegarde automatique des positions", "value": 'show'}], value=['show'], id='sauve_auto'
)
pompe_switch = dbc.Checklist(
            options=[
                {"value": 1}
            ],
            value=0,
            id="pompe",
            switch=True,
        )


layout = dbc.Container(
    [
     dbc.Row([dbc.Col(html.Button(id="compute_path", n_clicks=0, children="Film parcours", style={"background-color": "#41924B", "color": "#EFF3EF", "width": "200px"})),
              dbc.Col(html.Button(id="reset", n_clicks=0, children="Supprimer sauvegarde",style={"background-color": "#41924B", "color": "#EFF3EF", "width": "200px"})),
              dbc.Col(html.Button(id="init", n_clicks=0, children="Retour à la position initiale",style={"background-color": "#41924B", "color": "#EFF3EF", "width": "200px"})),
              dbc.Col(html.Button(id="sauve", n_clicks=0, hidden=True, children="Sauvegarde position",style={"background-color": "#41924B", "color": "#EFF3EF", "width": "200px"})),
              dbc.Col(html.P([html.Label("Choix d'un exercice: "), Choice_exo]))
              ]),
     html.Div([admis], style= {'display': 'block'}), ghost, Sauve_auto, Robot_reel,
     Storage_shapes,Storage,Interval,Storage_playing,Storage_title,
     dbc.Row([dbc.Col(dcc.Graph(id = 'plot', figure = fig)),
              dbc.Col([dbc.Row([
                                dbc.Col(html.P([html.Label("Pompe"), pompe_switch])),
                                dbc.Col(html.P([html.Label("Pivot"),Spivot])), 
                                dbc.Col(html.P([html.Label("Bras 1"),Sbras1])),
                                dbc.Col(html.P([html.Label("Bras 2"), Sbras2])), 
                                dbc.Col(html.P([html.Label("Bras 3"),Sbras3])), 
                                dbc.Col(html.P([html.Label("Pince"),Spince]))
                                ]),
                        dbc.Row([
                            html.Button(id="valide_carte", hidden=False, n_clicks=0, children="Valider position cartésienne", style={"background-color": "#f4a261", "color": "#EFF3EF", "width": "120px", 'font-size':'18px'}),
                            dbc.Col(html.P([html.Label("Robot x"),Rx])), 
                            dbc.Col(html.P([html.Label("Robot y"),Ry])),
                            dbc.Col(html.P([html.Label("Robot z"),Rz]))
                            ]),
                      ]),
              ]),
     ], fluid=True, className="dbc"
)    


@callback(
    Output('page_refresh', 'data'),
    Input('page_refresh', 'data')
)
def update_after_refresh(page_refresh):
    global robot
    global pca
    try:
        from adafruit_servokit import ServoKit
        robot = Robot(reel_actif=True)
        nbPCAservo = 16
        pca = ServoKit(channels=nbPCAservo)
        for key, channel in key2channel.items():
            pca.servo[channel].set_pulse_width_range(min_imp[key] , max_imp[key])
        robot.init_robot_reel(robot.pose(), pca)
        return False, list_exos
    except:
        robot = Robot(reel_actif=False)
        pca = None
        return False, list_exos




@callback(
    Output('robot_reel', 'value'),
    Input('robot_reel', 'value')
)
def update_robot_reel(robot_reel):
    print('actif', robot.reel_actif)

    if pca is None or robot_reel != ['show']:
        robot.reel_actif = False
        return []
    else:
        robot.reel_actif = True
        return ['show']




@callback(
    Output('storage_shapes', 'data'),
    Output('admis', 'style'),
    Output('admis', 'value'),
    Output('valide_carte', 'hidden'),
    Output('Rx', 'disabled'),
    Output('Ry', 'disabled'),
    Output('Rz', 'disabled'),
    Output('choice_exo', 'options'),
    Input('choice_exo', 'value')
)

def update_param_exo(name_exo):
    list_exos = []
    for file in os.listdir("./exercices"):
        if file.endswith(".pkl"):
            list_exos.append(file[:-4])
            
    data = []
    exo = pickle.load(open('./exercices/'+name_exo+'.pkl', "rb"))
    for id_shape, el in enumerate(exo['shapes']):
        shape.update_shape(el)
        data += shape.draw_current_shapes(showlegend=(id_shape==0))
    if exo['admis_exo']:
        disp = {'display': 'block'}
        val_admis = ['show']
    else:
        disp = {'display': 'none'}
        val_admis= ['']
    if exo['admis_carte']==['show']:
        carte = True
        robot.show_point = True
    else:
        carte = False
        robot.show_point = False
    return data, disp, val_admis, not(carte), not(carte), not(carte), not(carte), list_exos



@callback(
    Output("graph-refresher", "disabled"),
    Output("graph-refresher", "max_intervals"),
    Output('graph-refresher','n_intervals'),
    Input('compute_path', 'n_clicks'),
    State('choice_exo', 'value')
)
def update_store_interval(b_path, nom_exo):
    ctx = dash.callback_context
    if (not ctx.triggered):
        button_id = "not pressed yet"
        return True, 50, 50        
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        exo = pickle.load(open('./exercices/'+nom_exo+'.pkl', "rb"))
        for el in exo['shapes']:
            shape_playing.update_shape(el)
            robot.ls_shapes_playing.append(el)
       
        
    if len(robot.save)>=2:
        robot.is_playing = True
        robot.update_structure_reel(robot.save[0], pca)
        return False, (len(robot.save)-1)*(robot.maxframe+1)-1, 0
    else:
        return True, 50, 50
    
    
                                        
@callback(
    Output('storage', 'data'),
    Output('storage_playing', 'data'),
    Output('sauve', 'hidden'),
    Output('pivot', 'value'),
    Output('bras1', 'value'),
    Output('bras2', 'value'),
    Output('bras3', 'value'),
    Output('pince', 'value'),
    Output('pompe', 'value'),
    Output('Rx', 'value'),
    Output('Ry', 'value'),
    Output('Rz', 'value'),
    Output('title', 'data'),
    Input('graph-refresher','n_intervals'),
    Input('reset', 'n_clicks'),
    Input('init', 'n_clicks'),
    Input('sauve', 'n_clicks'),
    Input('valide_carte', 'n_clicks'),
    Input('pivot', 'value'),
    Input('bras1', 'value'),
    Input('bras2', 'value'),
    Input('bras3', 'value'),
    Input('pince', 'value'),
    Input('Rx', 'value'),
    Input('Ry', 'value'),
    Input('Rz', 'value'),
    Input('ghost', 'value'),
    Input('sauve_auto', 'value'),
    Input('admis', 'value'),
    Input('pompe', 'value'),
    Input('page_refresh', 'data'),
    State('choice_exo', 'value'),
    State('title', 'data')
)
def update_store_button(n_interval, b_reset, b_init, b_sauve, b_carte, input_piv, comple_input1, input2, input3, input_pince, rx, ry, rz, check_ghost, check_sauve_auto, check_admis, pompe_val, page_refresh, nom_exo, title):
    input1 = 180-comple_input1
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = "not pressed yet"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    data = []
    data_playing = []
    if check_sauve_auto==['show']:
        robot.sauve_auto = True
        hidden_sauve = True
    else:
        robot.sauve_auto = False
        hidden_sauve = False
    slider_carte_moved = (robot.extreme_point != np.array([rx,ry,rz])).any()
    
    
    pose = {'pivot': input_piv, 'bras1': input1, 'bras2': input2, 'bras3': input3, 'pince': input_pince, 'pompe':pompe_val}
    if robot.is_playing:
            
        mean_pose = robot.mean_pose(robot.save[robot.idx_playing],robot.save[robot.idx_playing+1])
        data, extreme_point, P = robot.data_list(mean_pose.copy(), get_final_coord=True)
        if robot.frame == 0:
            robot.update_structure_reel(robot.save[robot.idx_playing+1].copy(), pca)
        robot.frame += 1
        
        if not(robot.id_tracked_shape is None):
            if robot.conflict(extreme_point, P, mean_pose['pince']):
                title = 'Scénario incorrect: des pièces se percutent'

        if robot.pompe_is_changed():
            robot.frame = robot.maxframe+1
            if (robot.id_tracked_shape is None) and robot.save[robot.idx_playing+1]['pompe']:
                for id_shape, el in enumerate(robot.ls_shapes_playing):
                    shape_playing.update_shape(el)
                    if shape_playing.shape_catched(extreme_point, P[:,2]):
                        robot.id_tracked_shape = id_shape
                        if shape_playing.shape_type == 'Rectangle':
                            robot.ls_shapes_playing[id_shape]['theta'] -= (90+mean_pose['pivot'])-mean_pose['pince']
            elif not(robot.save[robot.idx_playing+1]['pompe']):
                if not(robot.id_tracked_shape is None):
                    if robot.correct_release(P[:,2]):
                        robot.ls_shapes_playing[robot.id_tracked_shape]['bx'] = extreme_point[0]
                        robot.ls_shapes_playing[robot.id_tracked_shape]['by'] = extreme_point[1]
                        robot.ls_shapes_playing[robot.id_tracked_shape]['bz'] = extreme_point[2]-robot.ls_shapes_playing[robot.id_tracked_shape]['h']
                        
                        if robot.ls_shapes_playing[robot.id_tracked_shape]['shape_type'] == 'Rectangle':
                            robot.ls_shapes_playing[robot.id_tracked_shape]['theta'] += (90+mean_pose['pivot'])-mean_pose['pince']
                    else:
                        robot.ls_shapes_playing[robot.id_tracked_shape]['bx'] = extreme_point[0]
                        robot.ls_shapes_playing[robot.id_tracked_shape]['by'] = extreme_point[1]
                        robot.ls_shapes_playing[robot.id_tracked_shape]['bz'] = extreme_point[2]-robot.ls_shapes_playing[robot.id_tracked_shape]['h']
                        robot.ls_shapes_playing[robot.id_tracked_shape]['pince'] = mean_pose['pince']
                        robot.ls_shapes_playing[robot.id_tracked_shape]['P'] = P
                        robot.ls_shapes_playing[robot.id_tracked_shape]['extreme_point'] = extreme_point
                        title = 'Scénario incorrect: pièce lachée non verticalement'
                robot.id_tracked_shape = None
            
        for id_shape, el in enumerate(robot.ls_shapes_playing):
            shape_playing.update_shape(el)            
            if id_shape != robot.id_tracked_shape:
                if 'P' in list(el.keys()):
                    data_playing += shape_playing.draw_current_tracked_shape(el['extreme_point'], el['P'], pince=el['pince'], showlegend=(id_shape==0))
                else:
                    data_playing += shape_playing.draw_current_shapes(showlegend=(id_shape==0))
            else:
                shape_playing.update_shape(el)
                data_playing += shape_playing.draw_current_tracked_shape(extreme_point, P, pince=mean_pose['pince'], showlegend=(id_shape==0))

        if robot.frame == robot.maxframe+1:
            robot.idx_playing += 1
            robot.frame = 0
            if robot.idx_playing == len(robot.save)-1:
                robot.is_playing = False
                robot.idx_playing = 0
                robot.id_tracked_shape = None
                robot.ls_shapes_playing = []
    else:
        if button_id == "reset":
            robot.save = []
            robot.ghost_pose = {}
            robot.update_structure(pose)
            robot.update_structure_reel(pose, pca)
            title = ''
        elif button_id == 'init' or robot.first_callback:
            robot.first_callback = False
            robot.update_structure(robot.DEFAULT_PARAMS.copy())
            robot.update_structure_reel(robot.pose(), pca)
            pose = robot.pose().copy()
            robot.extreme_point = robot.default_extreme_point
            input_piv, input1, input2, input3, input_pince, pompe_val = robot.dic2vars(robot.pose())
        elif button_id == "valide_carte":
            sol, dic = robot.compute_path(rx, ry, rz)
            if sol:
                input_piv, input1, input2, input3, input_pince_fake, pompe_fake = robot.dic2vars(dic)
                pose = {'pivot': input_piv, 'bras1': input1, 'bras2': input2, 'bras3': input3, 'pince': input_pince, 'pompe':pompe_val}
                robot.update_structure(pose)
                robot.update_structure_reel(pose, pca)                
        else:
            robot.update_structure(pose)
            robot.update_structure_reel(pose, pca)
        if robot.save == [] or robot.save[-1] != pose:
                # le dernier état du robot enregistré correspond-il à l'état courant?
                if robot.save==[] and (robot.sauve_auto or button_id == 'sauve'):
                    robot.ghost_pose = robot.pose().copy()
                if robot.sauve_auto or button_id == 'sauve':
                    robot.save.append(robot.pose().copy())
        data_pose, extreme_point = robot.data_list(robot.pose().copy())
        data += data_pose
        robot.extreme_point = extreme_point
    if check_ghost==['show'] and robot.ghost_pose != {}:
        data_g, end = robot.data_list(robot.ghost_pose.copy(), opacity = 0.3, showlegend=False) 
        data = data + data_g
    if not(slider_carte_moved) or button_id=="valide_carte":
        [rx, ry, rz] = robot.extreme_point
        
    if robot.show_point:
        if in_hull([rx, ry, rz], delaunayout) and not(in_hull([rx, ry, rz], delaunayin)):
            robot.color_arrivee = 'green'
        else:
            robot.color_arrivee = 'red'
        data += [robot.show_point_end(rx, ry, rz, color=robot.color_arrivee)]
        if check_admis==['show']:
            data = data + [robot.show_points_admissibles(ls_pointsout_admis)]
            data = data + [robot.show_points_admissibles(ls_pointsin_admis, opacity= 0.1, color='red')]

    return data, data_playing, hidden_sauve, input_piv, 180-input1, input2, input3, input_pince, pompe_val, rx, ry, rz, title







clientside_callback(
    """
    function(n_interval, data, data_shapes, data_playing, title) {
        if (data_playing.length == 0) {
               data_plot = data.concat(data_shapes)
        }
        else {
            data_plot = data.concat(data_playing)
        }
        
        layout = { 'uirevision': 'constant',
                    'title': {'text': title, 'font': {'size': 40, 'color': 'red'}},
                    'width': 1000,
                    'height': 1000,
                    'scene': {
                             'xaxis': {
                                 'nticks': 4,
                                 'range': [-200, 200],
                             },
                             'yaxis':{ 'nticks': 4,
                                 'range': [-200, 200],
                             },
                             'zaxis': {
                                 'nticks': 4,
                                 'range': [-30, 220],
                             },
                             'aspectratio': {'x':1, 'y':1, 'z':0.95},
                         }
                    }
        
        return  {'data': data_plot,
                    'layout' : layout
                    };
    }
    """,
    Output('plot', 'figure'),
    Input('graph-refresher','n_intervals'),
    Input('storage', 'data'),
    Input('storage_shapes', 'data'),
    Input('storage_playing', 'data'),
    Input('title', 'data')
    )

