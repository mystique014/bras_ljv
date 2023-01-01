#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Quentin Duchemin <qduchemin9@gmail.com>
# Licensed under the Creative Commons Attribution-ShareAlike License 4.0 (International) (CC-BY-SA 4.0) -https://creativecommons.org/licenses/by-sa/4.0/



import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import numpy as np

from scipy.spatial import ConvexHull, Delaunay

import time
import datetime
import dash_bootstrap_components as dbc  

from user import *


dbc_css = "./static/dbc.min.css"
dbc_minty = "./static/dbc_minty.css"
app = dash.Dash(__name__, external_stylesheets=[dbc_minty, dbc_css], use_pages=True, suppress_callback_exceptions=True
)


user = User()


Squelette = dbc.Modal(
            [
                html.Img(
                    id="logo",
                    src="./static/squelette.png",
                    style = {'width': '1100px',  'height': 'auto'}
                )
            ],
            is_open=False,
            id="squelette",
        )
        

Form = dbc.Modal(
            [
                dbc.ModalHeader("Authentification"),
                dbc.ModalBody(
                    [
                        dbc.Label("Date:"),
                        dbc.Input(id="date", type="text", disabled=True),
                        dcc.Dropdown(
                           options=['Eleve', 'Enseignant'],
                           value='Eleve',
                           id="compte"
                        ),
                        dbc.Label("Nom:"),
                        dbc.Input(id="nom", type="text", debounce=True),
                        dbc.Label("Mot de passe:"),
                        dbc.Input(id="mdp", type="text", debounce=True),
                    ]
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button("Valider", color="primary", id="valider_form"),
                        dbc.Button("Annuler", id="annuler_form"),
                    ]
                ),
            ],
            is_open=False,
            id="form",
        )



Page_refresh = dcc.Store(
        id='page_refresh',
        data=True)

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        html.Hr(),
        html.Button(id="home", n_clicks=0, children="Retour à l'accueil",style={"background-color": "#48494B", "color": "#EFF3EF", "width": "200px"}),
        html.Button(id="auth", n_clicks=0, children="Authentification",style={"background-color": "#48494B", "color": "#EFF3EF", "width": "200px"}),
        html.Button(id="button_squelette", n_clicks=0, children="Schema du robot",style={"background-color": "#48494B", "color": "#EFF3EF", "width": "200px"}),
        Form, Page_refresh, Squelette,
        dash.page_container,
    ]
)




@app.callback(
    Output("squelette", "is_open"),
    Input("button_squelette", "n_clicks")
)

def show_squelette(b_squelette):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = "not pressed yet"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "button_squelette":
        return True
    else:
        return False

@app.callback(
    [Output("form", "is_open"), Output("date", "value"), Output('url','pathname')],
    [
        Input("auth", "n_clicks"),
        Input("valider_form", "n_clicks"),
        Input("annuler_form", "n_clicks"),
        Input("nom", "value"),
        Input("home", 'n_clicks')
    ],
    [State("form", "is_open"), State("date", "value"), State("mdp", "value"), State("compte", "value") ],
)
def show_modal(b_auth, b_valid, b_ann, nom_value, b_home, form_open, data_val, mdp_val, compte_val):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = "not pressed yet"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if button_id == "auth":
        return True, dt, dash.no_update
    elif button_id == "valider_form":
        if compte_val == user.comptes_dispos[1] and ((nom_value, mdp_val) in user.nom2mdp.items()):
            user.compte = user.comptes_dispos[1]
            user.nom = nom_value
            return False, dt, '/create_shapes'
        elif compte_val == user.comptes_dispos[0]:
            user.compte = user.comptes_dispos[0]
            user.nom = nom_value
            print('ok')
            return False, dt, '/bras'
        else:
            return form_open, dt, dash.no_update
    elif button_id == "annuler_form":
        return False, dt, dash.no_update
    elif button_id == 'home':
        return False, dt, '/'
    else:
        return form_open, dt, dash.no_update



# Add the server clause
if __name__ == '__main__':
    if False:
        app.run_server(debug = True, host="10.3.141.1", port=8050)
    else:
        app.run_server(debug = True)