#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 12:21:49 2022

@author: duchemin
"""



class User():
    def __init__(self):
        self.comptes_dispos = ['Eleve', 'Enseignant']
        self.compte = self.comptes_dispos[0]
        self.nom2mdp = {'prof': 'prof'}
        self.nom = ''
        
    def hidden_components(self):
        if self.compte == self.comptes_dispos[0]:
            return {'create_shapes'}
            