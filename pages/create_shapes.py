#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Quentin Duchemin <qduchemin9@gmail.com>
# Licensed under the Creative Commons Attribution-ShareAlike License 4.0 (International) (CC-BY-SA 4.0) -https://creativecommons.org/licenses/by-sa/4.0/


import dash
from dash import html, dcc, Output, Input, callback, State, clientside_callback
import numpy as np
from scipy.spatial import ConvexHull, Delaunay
import plotly.graph_objs as go

from pages.utils import *

from pages.shapes import *
import dash_bootstrap_components as dbc  
import pickle

shapes = Shapes()

dash.register_page(__name__, path='/create_shapes')


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

# Step 2. Import the dataset

pointsin = np.load('./static/pointsin.npy')
pointsout = np.load('./static/pointsout.npy')
pointsin = pointsin[np.where(pointsin[:,1]<=0)[0],:]
pointsout = pointsout[np.where(pointsout[:,1]<=0)[0],:]
ls_pointsin_admis = pointsin[ConvexHull(pointsin).vertices]
ls_pointsout_admis = pointsout[ConvexHull(pointsout).vertices]
delaunayin = Delaunay(ls_pointsin_admis)
delaunayout = Delaunay(ls_pointsout_admis)
ls_points_admis = np.concatenate((ls_pointsin_admis,ls_pointsout_admis), axis=0)


# Step 3. Create a plotly figure

fig = go.Figure()


Storage = dcc.Store(
        id='storage_exo',
        data=[])

Storage_current = dcc.Store(
        id='storage_exo_current',
        data=[])
Bx = dcc.Slider(-200, 200, 1, 
           marks={str(i): str(i) for i in np.arange(-200,200,100)},
           value=shapes.bx, id = 'Bx', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
By = dcc.Slider(-200, 200, 1, 
           marks={str(i): str(i) for i in np.arange(-200,200,100)},
           value=shapes.by, id = 'By', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Bz = dcc.Slider(0, 100, 1, 
           marks={str(i): str(i) for i in np.arange(0,200,50)},
           value=shapes.bz, id = 'Bz', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Ex = dcc.Slider(-200, 200, 1, 
           marks={str(i): str(i) for i in np.arange(-200,200,100)},
           value=shapes.ex, id = 'Ex', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Ey = dcc.Slider(-200, 200, 1, 
           marks={str(i): str(i) for i in np.arange(-200,200,100)},
           value=shapes.ey, id = 'Ey', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
Ez = dcc.Slider(0, 200, 1, 
           marks={str(i): str(i) for i in np.arange(0,200,50)},
           value=shapes.ez, id = 'Ez', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
R = dcc.Slider(1, 40, 1, 
           marks={str(i): str(i) for i in np.arange(0,40,5)},
           value=10, id = 'R', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
H = dcc.Slider(1, 40, 1, 
           marks={str(i): str(i) for i in np.arange(0,40,5)},
           value=10, id = 'H', vertical=True,
           tooltip={"placement": "bottom", "always_visible": True})
admis = dcc.Checklist(
    [{"label": "Montrer les points admissibles", "value": 'show'}], value=['show'], id='admis'
)

admis_exo = dcc.Checklist(
    [{"label": "Montrer les points admissibles dans l'exercice", "value": 'show'}], value=['show'], id='admis_exo'
)

admis_carte = dcc.Checklist(
    [{"label": "Autoriser les mouvements en coordonnées cartésiennes dans l'exercice", "value": 'show'}], value=['show'], id='admis_carte'
)

admis_coord = dcc.Checklist(
    [{"label": "Lecture possible des coordonnées cartésiennes sur la figure 3D", "value": 'show'}], value=['show'], id='admis_coord'
)

sauve_exo = dbc.Modal(
            [
                dbc.ModalHeader("Sauvegarder l'exercice"),
                dbc.ModalBody(
                    [
                        dbc.Label("Nom:"),
                        dbc.Input(id="nom_exo", type="text", debounce=True),
                    ]
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button("Valider", color="primary", id="valider_form_exo"),
                        dbc.Button("Annuler", id="annuler_form_exo"),
                    ]
                ),
            ],
            is_open=False,
            id="form_exo",
        )


layout = dbc.Container(
    [html.Button(id="reset", n_clicks=0, children="Supprimer la sauvegarde",style={"background-color": "#41924B", "color": "#EFF3EF", "width": "200px"}),
     html.Button(id="sauve_piece", n_clicks=0, children="Sauvegarder la pièce",style={"background-color": "#41924B", "color": "#EFF3EF", "width": "200px"}),
     html.Button(id="b_form_exo", n_clicks=0, children="Sauvegarder l'exercice",style={"background-color": "#48494B", "color": "#EFF3EF", "width": "200px"}),
     sauve_exo, 
     admis, 
     html.Label("Paramètres de l'exercice"),
     admis_exo, admis_carte, admis_coord, 
     Storage,Storage_current,
     dbc.Row([dbc.Col(dcc.Graph(id = 'plot_exo', figure = fig)),
              dbc.Col([dbc.Row([
                                  html.Label("Position initiale"),
                                  dbc.Col(html.P([html.Label("x initial"),Bx])), 
                                  dbc.Col(html.P([html.Label("y initial"),By])),
                                  dbc.Col(html.P([html.Label("z initial"),Bz])),
                                dbc.Col(html.P([html.Label("hauteur"), H])),
                                dbc.Col(html.P([html.Label("rayon"), R]))
                                ]),
                        dbc.Row([
                            html.Label("Position finale"),
                            dbc.Col(html.P([html.Label("x final"),Ex])), 
                            dbc.Col(html.P([html.Label("y final"),Ey])),
                            dbc.Col(html.P([html.Label("z final"), Ez])),
                            ]),
                        
                      ]),
              ]),
     ], fluid=True, className="dbc"
)                   



@callback(
    Output("form_exo", "is_open"),
    [
        Input('b_form_exo', 'n_clicks'),
        Input("valider_form_exo", "n_clicks"),
        Input("annuler_form_exo", "n_clicks"),
        Input("nom_exo", "value"),
        Input('admis_exo', 'value'),
        Input('admis_carte', 'value'),
        Input('admis_coord', 'value')
    ],
    [State("form_exo", "is_open") ],
)
def save_exo(b_form_ex, b_valid, b_ann, nom_value, admis_exo, admis_carte, admis_coord, form_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = "not pressed yet"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if  button_id == "b_form_exo":
        return True
    elif button_id == "valider_form_exo":
        if nom_value is None:
            nom_value = ''
        f = open('./exercices/'+nom_value+".pkl","wb")
        exo = {'shapes': shapes.save, 'admis_carte': admis_carte, 'admis_coord': admis_coord, 'admis_exo': admis_exo}
        # write the python object (dict) to pickle file
        pickle.dump(exo,f)
        # close file
        f.close()
        return False
    elif button_id == "annuler_form_exo":
        return False
    else:
        return form_open

    
    
                                        
@callback(
    Output('storage_exo', 'data'),
    Output('storage_exo_current', 'data'),  
    Output('Bx', 'value'),
    Output('By', 'value'),
    Output('Bz', 'value'),
    Output('Ex', 'value'),
    Output('Ey', 'value'),
    Output('Ez', 'value'),
    Output('R', 'value'),
    Output('H', 'value'),
    Input('reset', 'n_clicks'),
    Input('sauve_piece', 'n_clicks'),
    Input('Bx', 'value'),
    Input('By', 'value'),
    Input('Bz', 'value'),
    Input('Ex', 'value'),
    Input('Ey', 'value'),
    Input('Ez', 'value'),
    Input('R', 'value'),
    Input('H', 'value'),
    Input('admis', 'value'),
    State('storage_exo', 'data')
)
def update_store_button(b_reset, b_sauve, bx, by, bz, ex, ey, ez, rayon, hauteur, check_admis, data):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = "not pressed yet"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    shapes.update_shape(shapes.vars2dic(bx, by, bz, ex, ey, ez, rayon, hauteur))

    if button_id == "reset":
        shapes.save = []
        data = []
    elif button_id == "sauve_piece":
        shapes.save_pose()
        data += shapes.draw_current_shapes()
        shapes.update_shape(shapes.default_params)
        bx, by, bz, ex, ey, ez, rayon, hauteur = shapes.dic2vars(shapes.default_params)
    data_current = shapes.draw_current_shapes()

    
    if in_hull([ex, ey, ez+hauteur], delaunayout) and not(in_hull([ex, ey, ez+hauteur], delaunayin)):
        shapes.color_arrivee = 'green'
    else:
        shapes.color_arrivee = 'red'
    data_current += [shapes.show_point(ex, ey, ez, label = 'Point final', color=shapes.color_arrivee)]
    if in_hull([bx, by, bz+hauteur], delaunayout) and not(in_hull([bx, by, bz+hauteur], delaunayin)):
        shapes.color_arrivee = 'green'
    else:
        shapes.color_arrivee = 'red'
    data_current += [shapes.show_point(bx, by, bz, label='Point initial', color=shapes.color_arrivee, symbol_marker='diamond')]
    if check_admis==['show']:
        data_current = data_current + [shapes.show_points_admissibles(ls_pointsout_admis)]
        data_current = data_current + [shapes.show_points_admissibles(ls_pointsin_admis, color='orange')]
    return data, data_current, bx, by, bz, ex, ey, ez, rayon, hauteur





clientside_callback(
    """
    function(data, datacurrent) {
        return {
            'data': data.concat(datacurrent),
            'layout' : {'scene_aspectmode': 'cube',
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
                                 'aspectratio': {'x':1, 'y':1, 'z':0.95}
                             }
                        }
            }
    }
    """,
    Output('plot_exo', 'figure'),
    Input('storage_exo', 'data'),
    Input('storage_exo_current', 'data')
    )
