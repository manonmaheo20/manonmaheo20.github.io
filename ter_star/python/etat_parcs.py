#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:10:30 2020

"""


from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
import urllib
from urllib import request
import json


url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-parcsrelais-etat-tr&facet=nom&facet=etat"
#jeu de données de l'état des parcs relais en temps réel
fp = urllib.request.urlopen(url)
contenu = fp.read().decode("utf-8")
dico = json.loads(contenu)
dico_parc = {}
for dico_record in dico["records"] : 
    cap = dico_record["fields"]["nombreplacesdisponibles"]
    nom = dico_record["fields"]["nom"]
    etat = dico_record["fields"]["etat"]
    dico_parc[nom] = (cap, etat) #création d'un dictionnaire avec comme clé le nom du parc-relais et comme valeurs sa 
                                 #capacité actuelle et son état (Ouvert, Fermé)
                        
    
    
parc = []  
capacite = [] 
fonct = [] 
for nom, tuples in dico_parc.items() : 
    parc.append(nom)                  #Création d'une liste avec tous les noms des parcs-relais
    capacite.append(tuples[0])        #Création d'une liste avec toutes les capacités actuelles des parcs-relais  
    fonct.append(tuples[1])           #Création d'une liste avec tous les états des parcs-relais


data = ColumnDataSource(data=dict(parc=parc, capacite=capacite, fonct=fonct))

p = figure(x_range=parc, plot_height=max(capacite), toolbar_location=None, 
           title="Etat et capacité actuelle des parcs-relais", tools="hover", tooltips="@fonct") 
#tools : hover et tooltips : "@fonct" permettent d'avoir l'état du parc-relais au survol de la souris
p.vbar(x='parc', top='capacite', width=0.7, source=data, name="parc",
       line_color='white', fill_color=factor_cmap('parc', palette=Spectral6, factors=parc)) #création du diagramme en barre
#en x : les parcs-relais, en y : la capacité actuelle

p.xgrid.grid_line_color = None #permet de ne pas avoir les lignes de quadrillage de x
p.y_range.start = 0 #permet de démarrer à 0 en y


output_file("parc_etatetcapacite.html") #enregistre le diagramme dans un fichier html

    