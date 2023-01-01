#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Quentin Duchemin <qduchemin9@gmail.com>
# Licensed under the Creative Commons Attribution-ShareAlike License 4.0 (International) (CC-BY-SA 4.0) -https://creativecommons.org/licenses/by-sa/4.0/

import dash
from dash import html, dcc

import dash_bootstrap_components as dbc  

dash.register_page(__name__, path="/")




button_howto = dbc.Button(
    "Voir la documentation",
    id="howto-open",
    outline=True,
    color="info",
    # Turn off lowercase transformation for class .button in stylesheet
    style={"textTransform": "none", 'width':'200px', 'font-size':'20px', 'font-weight':'bold'},
)

button_github = dbc.Button(
    "Voir le code sur Github",
    outline=True,
    color="primary",
    href="https://github.com/mystique014/bras_ljv",
    id="gh-link",
    style={"text-transform": "none", 'width':'200px', 'font-size':'20px', 'font-weight':'bold'},
)

# Header
header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            id="logo",
                            src="./static/logo.png",
                            height="200px",
                        ),
                        md="auto",
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H3("Bras Robotisé avec contrôle à distance"),
                                    html.P("Plateforme interactive et exercices"),
                                ],
                                id="app-title",
                            )
                        ],
                        md=True,
                        align="center",
                    ),
                ],
                align="center",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.NavbarToggler(id="navbar-toggler"),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavItem(button_howto),
                                        dbc.NavItem(button_github),
                                    ],
                                    navbar=True,
                                ),
                                id="navbar-collapse",
                                navbar=True,
                            ),
                        ],
                        md=2,
                    ),
                ],
                align="center",
            ),
        ],
        fluid=True,
    ),
    sticky="top",
)

# Description
description = dbc.Col(
    [
        dbc.Card(
            id="description-card",
            children=[
                dbc.CardHeader("Description du projet"),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Img(
                                            src="./static/exemple_exo.png",
                                            width="900px",
                                        )
                                    ],
                                    md="auto",
                                ),
                                dbc.Col([
                                    html.P(
                                        "Cet outil permet le contrôle d'un bras robotisé à distance à l'aide d'un Raspberry Pi. " 
                                        "La plateforme interactive permet de jouer des scénarios virtuels et de réaliser des exercices. "
                                    ,style={'font-size':'20px'}),
                                    html.Label(["Copyright \u00A9  Quentin Duchemin et Stéphane Duchemin. 2023. Sauf indication contraire, le code correspondant au projet Bras LJV developpé par Quentin Duchemin et Stéphane Duchemin est autorisé sous la licence ", html.A("Creative Commons Attribution-ShareAlike License 4.0 (International) (CC-BY-SA 4.0)", href='https://creativecommons.org/licenses/by-sa/4.0/')])]
                                ),
                            ]
                        ),
                    ]
                ),
            ],
        )
    ],
    md=12,
)



layout = html.Div(
    [   header,
        description
    ]
)