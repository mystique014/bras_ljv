#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 23:19:52 2022

@author: duchemin
"""

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import numpy as np

from robot import *
from scipy.spatial import ConvexHull, Delaunay

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


# Step 1. Launch the application
app = dash.Dash()
server = app.server
import dash_bootstrap_components as dbc  

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc_css])

# Step 2. Import the dataset

pointsin = np.load('pointsin.npy')
pointsout = np.load('pointsout.npy')
pointsin = pointsin[np.where(pointsin[:,1]<=0)[0],:]
pointsout = pointsout[np.where(pointsout[:,1]<=0)[0],:]
ls_pointsin_admis = pointsin[ConvexHull(pointsin).vertices]
ls_pointsout_admis = pointsout[ConvexHull(pointsout).vertices]
delaunayin = Delaunay(ls_pointsin_admis)
delaunayout = Delaunay(ls_pointsout_admis)
ls_points_admis = np.concatenate((ls_pointsin_admis,ls_pointsout_admis), axis=0)


# Step 3. Create a plotly figure

fig = go.Figure()
robot = Robot()


Storage = dcc.Store(
        id='storage',
        data=[])
Storage_point_end = dcc.Store(
        id='storage_point_end',
        data=[])
Interval = dcc.Interval(id='graph-refresher',
                     interval=1*200,
                     n_intervals=0,
                     max_intervals=50,
                     disabled=True)
Spiv = dcc.Slider(0, 180, 1, 
           marks={str(i): str(i) for i in np.arange(0,180,45)},
            value=robot.pivot, id = 'pivot', vertical=True,
            tooltip={"placement": "bottom", "always_visible": True})
Spince = dcc.Slider(0, 360, 1, 
           marks={str(i): str(i) for i in np.arange(0,360,45)},
           value=robot.pince, id = 'pince',  vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Sbras1 = dcc.Slider(60, 150, 1, 
           marks={str(i): str(i) for i in np.arange(60,150,20)},
           value=robot.bras1, id = 'bras1', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Sbras2 = dcc.Slider(70, 110, 1, 
           marks={str(i): str(i) for i in np.arange(70,110,10)},
           value=robot.bras2, id = 'bras2', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Sbras3 = dcc.Slider(0, 100, 1, 
           marks={str(i): str(i) for i in np.arange(0,100,20)},
           value=robot.bras3, id = 'bras3', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Sx = dcc.Slider(-200, 200, 1, 
           marks={str(i): str(i) for i in np.arange(-200,200,100)},
           value=0, id = 'Sx', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Sy = dcc.Slider(-200, 200, 1, 
           marks={str(i): str(i) for i in np.arange(-200,200,100)},
           value=0, id = 'Sy', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Sz = dcc.Slider(0, 100, 1, 
           marks={str(i): str(i) for i in np.arange(0,200,50)},
           value=0, id = 'Sz', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Rx = dcc.Slider(-200, 200, 1, 
           marks={str(i): str(i) for i in np.arange(-200,200,100)},
           value=robot.extreme_point[0], id = 'Rx', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Ry = dcc.Slider(-200, 200, 1, 
           marks={str(i): str(i) for i in np.arange(-200,200,100)},
           value=robot.extreme_point[1], id = 'Ry', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Rz = dcc.Slider(-200, 200, 1, 
           marks={str(i): str(i) for i in np.arange(0,200,50)},
           value=robot.extreme_point[2], id = 'Rz', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
admis = dcc.Checklist(
    [{"label": "Montrer les points admissibles", "value": 'show'}], value=['show'], id='admis'
)
ghost = dcc.Checklist(
    [{"label": "Montrer la position initiale du mouvement", "value": 'show'}], value=['show'], id='ghost'
)

Sauve_auto = dcc.Checklist(
    [{"label": "Sauvegarde automatique des positions", "value": 'show'}], value=['show'], id='sauve_auto'
)


app.layout = dbc.Container(
    [html.Button(id="compute_path", n_clicks=0, children="Film parcours", style={"background-color": "#41924B", "color": "#EFF3EF", "width": "120px"}),
     html.Button(id="compute_path_end", n_clicks=0, children="Film point d'arrivée", style={"background-color": "#41924B", "color": "#EFF3EF", "width": "120px"}),
     html.Button(id="reset", n_clicks=0, children="Reset ",style={"background-color": "#41924B", "color": "#EFF3EF", "width": "120px"}),
     html.Button(id="init", n_clicks=0, children="Initialisation ",style={"background-color": "#41924B", "color": "#EFF3EF", "width": "120px"}),
     html.Button(id="sauve", n_clicks=0, hidden=True, children="Sauvegarde position",style={"background-color": "#41924B", "color": "#EFF3EF", "width": "120px"}),
     admis, ghost, Sauve_auto,
     Storage_point_end,Storage,Interval,
     dbc.Row([dbc.Col(dcc.Graph(id = 'plot', figure = fig)),
              dbc.Col([dbc.Row([dbc.Col(html.P([html.Label("Pivot"),Spiv])), 
                                dbc.Col(html.P([html.Label("Bras 1"),Sbras1])),
                                dbc.Col(html.P([html.Label("Bras 2"), Sbras2])), 
                                dbc.Col(html.P([html.Label("Bras 3"),Sbras3])), 
                                dbc.Col(html.P([html.Label("Pince"),Spince])),
                                dbc.Col(html.P([html.Label("Robot x"),Rx])), 
                                dbc.Col(html.P([html.Label("Robot y"),Ry])),
                                dbc.Col(html.P([html.Label("Robot z"),Rz]))]), 
                       dbc.Row([dbc.Col(html.P([html.Label("x"),Sx])), 
                                dbc.Col(html.P([html.Label("y"),Sy])),
                                dbc.Col(html.P([html.Label("z"),Sz]))
                                ])
                      ]),
              ]),
     ], fluid=True, className="dbc"
)                   


# Step 5. Add callback functions


@app.callback(
    Output("graph-refresher", "disabled"),
    Output("graph-refresher", "max_intervals"),
    Output('graph-refresher','n_intervals'),
    Input('compute_path', 'n_clicks'),
    Input('compute_path_end', 'n_clicks')
)
def update_store_interval(b_path, b_path_end):
    ctx = dash.callback_context
    if (not ctx.triggered):
        button_id = "not pressed yet"
        return True, 50, 50        
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
    
    if button_id == 'compute_path_end':
        robot.compute_frames(robot.pose(), robot.sx, robot.sy, robot.sz)
        
    if len(robot.save)>=2:
        robot.is_playing = True
        return False, (len(robot.save)-1)*robot.maxframe-1, 0
    else:
        return True, 50, 50
                


               

    
    
                                        
@app.callback(
    Output('storage', 'data'),
    Output('sauve', 'hidden'),
    Output('pivot', 'value'),
    Output('bras1', 'value'),
    Output('bras2', 'value'),
    Output('bras3', 'value'),
    Output('pince', 'value'),
    Output('Rx', 'value'),
    Output('Ry', 'value'),
    Output('Rz', 'value'),
    Input('graph-refresher','n_intervals'),
    Input('reset', 'n_clicks'),
    Input('init', 'n_clicks'),
    Input('sauve', 'n_clicks'),
    Input('pivot', 'value'),
    Input('bras1', 'value'),
    Input('bras2', 'value'),
    Input('bras3', 'value'),
    Input('pince', 'value'),
    Input('Rx', 'value'),
    Input('Ry', 'value'),
    Input('Rz', 'value'),
    Input('ghost', 'value'),
    Input('sauve_auto', 'value')
)
def update_store_button(n_interval, b_reset, b_init, b_sauve, input_piv, input1, input2, input3, input_pince, rx, ry, rz, check_ghost, check_sauve_auto):
    ctx = dash.callback_context
    if check_sauve_auto==['show']:
        robot.sauve_auto = True
        hidden_sauve= True
    else:
        robot.sauve_auto = False
        hidden_sauve = False
    if (robot.extreme_point != np.array([rx,ry,rz])).any():
        sol, dic = robot.compute_path(rx, ry, rz)
        if sol:
            input_piv, input1, input2, input3, input_pince = robot.dic2vars(dic)     
        else:
            [rx, ry, rz] = robot.extreme_point
            data, extreme_point = robot.data_list(robot.pose().copy())
            return data, hidden_sauve, input_piv, input1, input2, input3, input_pince, rx, ry, rz
    pose = {'pivot': input_piv, 'bras1': input1, 'bras2': input2, 'bras3': input3, 'pince': input_pince}
    if robot.is_playing:
        data, extreme_point = robot.data_list(robot.mean_pose(robot.save[robot.idx_playing],robot.save[robot.idx_playing+1]))
        robot.frame += 1
        if robot.frame == robot.maxframe:
            robot.idx_playing += 1
            robot.frame = 0
            if robot.idx_playing == len(robot.save)-1:
                robot.is_playing = False
                robot.idx_playing = 0
    else:
        if not ctx.triggered:
            button_id = "not pressed yet"
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "reset":
            robot.save = []
            robot.ghost_pose = {}
            robot.update_structure(pose)
        elif button_id == 'init':
            robot.update_structure(robot.DEFAULT_PARAMS)
            robot.extreme_point = robot.default_extreme_point
            input_piv, input1, input2, input3, input_pince = robot.dic2vars(robot.pose())
        else:
            robot.update_structure(pose)
        if robot.save == [] or robot.save[-1] != pose:
                # le dernier état du robot enregistré correspond-il à l'état courant?
                if robot.save==[] and (robot.sauve_auto or button_id == 'sauve'):
                    robot.ghost_pose = robot.pose().copy()
                if robot.sauve_auto or button_id == 'sauve':
                    robot.save.append(robot.pose().copy())
        data, extreme_point = robot.data_list(robot.pose().copy())
        robot.extreme_point = extreme_point
    if check_ghost==['show'] and robot.ghost_pose != {}:
        data_g, end = robot.data_list(robot.ghost_pose.copy(), opacity = 0.3, showlegend=False) 
        data = data + data_g
    [rx, ry, rz] = robot.extreme_point
    return data, hidden_sauve, input_piv, input1, input2, input3, input_pince, rx, ry, rz




      
                                        
# @app.callback(
#     Output('storage', 'data'),
#     Output('sauve', 'hidden'),
#     Input('graph-refresher','n_intervals'),
#     Input('reset', 'n_clicks'),
#     Input('init', 'n_clicks'),
#     Input('sauve', 'n_clicks'),
#     Input('pivot', 'value'),
#     Input('bras1', 'value'),
#     Input('bras2', 'value'),
#     Input('bras3', 'value'),
#     Input('pince', 'value'),
#     Input('ghost', 'value'),
#     Input('sauve_auto', 'value')
# )
# def update_store_button(n_interval, b_reset, b_init, b_sauve, input_piv, input1, input2, input3, input_pince, check_ghost, check_sauve_auto):
#     ctx = dash.callback_context
#     pose = {'pivot': input_piv, 'bras1': input1, 'bras2': input2, 'bras3': input3, 'pince': input_pince}
#     if check_sauve_auto==['show']:
#         robot.sauve_auto = True
#         hidden_sauve= True
#     else:
#         robot.sauve_auto = False
#         hidden_sauve = False
#     if robot.is_playing:
#         data, extreme_point = robot.data_list(robot.mean_pose(robot.save[robot.idx_playing],robot.save[robot.idx_playing+1]))
#         robot.extreme_point = extreme_point
#         robot.frame += 1
#         if robot.frame == robot.maxframe:
#             robot.idx_playing += 1
#             robot.frame = 0
#             if robot.idx_playing == len(robot.save)-1:
#                 robot.is_playing = False
#                 robot.idx_playing = 0
#     else:
#         if not ctx.triggered:
#             button_id = "not pressed yet"
#         else:
#             button_id = ctx.triggered[0]["prop_id"].split(".")[0]
#         if button_id == "reset":
#             robot.save = []
#             robot.ghost_pose = {}
#             robot.update_structure(pose)
#         elif button_id == 'init':
#             robot.update_structure(robot.DEFAULT_PARAMS)
#         else:
#             robot.update_structure(pose)
#         if robot.save == [] or robot.save[-1] != pose:
#                 # le dernier état du robot enregistré correspond-il à l'état courant?
#                 if robot.save==[] and (robot.sauve_auto or button_id == 'sauve'):
#                     robot.ghost_pose = robot.pose().copy()
#                 if robot.sauve_auto or button_id == 'sauve':
#                     robot.save.append(robot.pose().copy())
#         data, extreme_point = robot.data_list(robot.pose().copy())
#         robot.extreme_point = extreme_point
#     if check_ghost==['show'] and robot.ghost_pose != {}:
#         data_g, end = robot.data_list(robot.ghost_pose.copy(), opacity = 0.3, showlegend=False) 
#         data = data + data_g
#     return data, hidden_sauve




                                        
# @app.callback(
#     Output('pivot', 'value'),
#     Output('bras1', 'value'),
#     Output('bras2', 'value'),
#     Output('bras3', 'value'),
#     Output('pince', 'value'),
#     Output('Rx', 'value'),
#     Output('Ry', 'value'),
#     Output('Rz', 'value'),
#     Input('pivot', 'value'),
#     Input('bras1', 'value'),
#     Input('bras2', 'value'),
#     Input('bras3', 'value'),
#     Input('pince', 'value'),
#     Input('Rx', 'value'),
#     Input('Ry', 'value'),
#     Input('Rz', 'value')
# )
# def update_param_carte(input_piv, input1, input2, input3, input_pince, rx, ry, rz):
#     if robot.extreme_point != [rx,ry,rz]:
#         sol, dic = robot.compute_path(rx, ry, rz)
#         return robot.dic2vars(dic), rx, ry, rz
#     else:
        
        
#         return 


# @app.callback(
#     Output('pivot', 'value'),
#     Output('bras1', 'value'),
#     Output('bras2', 'value'),
#     Output('bras3', 'value'),
#     Output('pince', 'value'),
#     Input('Rx', 'value'),
#     Input('Ry', 'value'),
#     Input('Rz', 'value')
# )
# def update_carte2param(rx, ry, rz):
#     return robot.dic2vars(dic)


  
@app.callback(
    Output('storage_point_end', 'data'),
    Input('Sx', 'value'),
    Input('Sy', 'value'),
    Input('Sz', 'value'),
    Input('admis', 'value')
)
def update_store_point_end(sx, sy, sz, check_admis):
    robot.sx, robot.sy, robot.sz = sx, sy, sz
    if in_hull([sx, sy, sz], delaunayout) and not(in_hull([sx, sy, sz], delaunayin)):
        robot.color_arrivee = 'green'
    else:
        robot.color_arrivee = 'red'
    data = [robot.show_point_end(sx, sy, sz, color=robot.color_arrivee)]
    if check_admis==['show']:
        data = data + [robot.show_points_admissibles(ls_pointsout_admis)]
        data = data + [robot.show_points_admissibles(ls_pointsin_admis, color='orange')]
    return data



app.clientside_callback(
    """
    function(n_interval, data, data_point_end) {
        return {
            'data': data.concat(data_point_end),
            'layout' : {'scene_aspectmode': 'cube',
                        'width': 1000,
                        'height': 700,
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
                             }
                        }
            }
    }
    """,
    Output('plot', 'figure'),
    Input('graph-refresher','n_intervals'),
    Input('storage', 'data'),
    Input('storage_point_end', 'data')
    )


            
# Step 6. Add the server clause
if __name__ == '__main__':
    app.run_server(debug = True)
