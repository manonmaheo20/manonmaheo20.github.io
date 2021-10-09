#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 09:19:03 2021

@author: manonmaheo
"""

import pandas as pd 
from bokeh.plotting import figure, output_file, show, ColumnDataSource

from math import pi
from bokeh.palettes import Plasma256
from bokeh.models import LinearColorMapper

from bokeh.models.widgets import Tabs, Panel
from bokeh.models.widgets import Dropdown

from bokeh.layouts import row
from bokeh.io import curdoc

from bokeh.tile_providers import get_provider, Vendors

import numpy as np
import json
from bokeh.models import HoverTool

from bokeh.transform import factor_cmap
from bokeh.palettes import Category20
from bokeh.models.widgets import RadioGroup

#Importation du fichier de données athlete_events.csv
donnees = pd.read_csv("athlete_events.csv", sep =",")
#print(donnees.head)
#print(donnees.iloc[0])

#CONSTRUCTION DU PREMIER GRAPHIQUE NON-CARTOGRAPHIQUE

#On récupère les données des jeux olympiques entre 1916 et 2016
donnees['Year'] = pd.to_datetime(donnees['Year'], format="%Y")
selection = (donnees['Year'] >= '1916') & (donnees['Year'] <= '2016')
donnees2=donnees.loc[selection]
#print(donnees2['Year'])

#CONSTRUCTION DU SECOND GRAPHIQUE CARTOGRAPHIQUE

#Pour ce deuxième graphique, on souhaite représenter plus ou moins la participation
#des femmes aux jeux olympiques. En ce sens, on regarde pour chaque pays européens, 
#sur une période de 100 ans (1916-2016) le nombre d'athlètes féminines (mais aussi,
#et ce, pour comparer, le nombre d'athlètes masculins et total) ayant participé aux JO. 

#On se concentre sur ceux qui ont participé aux JO, mais on retire les doublons d'athlètes
donnees4 = donnees2.copy()
donnees4 = donnees4.drop_duplicates(subset = "Name")
#print(donnees4)

#On regroupe par pays ou CNO et on regarde le nombre d'hommes, de femmes et total 
#ayant participé aux JO
donnees4["count"] = 1
table2 = pd.pivot_table(donnees4, index="NOC", columns="Sex",values="count",aggfunc="sum")
table2 ["total"] = table2.sum(axis=1)
#plutôt que d'avoir un NA correspondant à aucun participant de type homme ou femme, 
#on met 0 par sécurité pour la construction du graphique
table2 = table2.fillna(0)
#print(table2)
#print(table2.shape)
#print(table2.columns) 
#print(table2.index) #on a 230 Comité National Olympique Code à 3 lettres

#Pour construire le graphique, on récupère les données précédentes et on crée
#un jeu de données donnees_final2 sans les index des lignes pour plus de simplicité
liste_femmes2 = []
liste_hommes2 = []
liste_total2 = []
liste_cno = []
for x in table2.itertuples():
    liste_femmes2.append(x.F)
    liste_hommes2.append(x.M)
    liste_total2.append(x.total)
for x in table2.index :
    liste_cno.append(x)
#print(liste_cno)
#print(liste_hommes2)
#print(liste_femmes2)
#print(liste_total2)

donnees_final2 = pd.DataFrame({'CNO': liste_cno,
                               'NB_FEMMES': liste_femmes2,
                               'NB_HOMMES': liste_hommes2,
                               'NB_TOTAL': liste_total2})
#print(donnees_final2)


#On importe le fichier de données noc_regions.csv pour avoir le nom des pays
regions = pd.read_csv("noc_regions.csv", sep =",")
#print(regions)

#On fait une jointure avec donnees_final2 pour avoir une colonne avec les noms des pays
jointure = donnees_final2.merge(regions, left_on = "CNO", right_on = "NOC")
#print(jointure)
print(jointure['region'].unique())

#On ne conserve que les pays européens
jointure = jointure.loc[jointure['region'].isin(["France", "Germany",
                                                  "UK", "Italy", 
                                                  "Portugal",
                                                  "Greece", "Spain", "Netherlands",
                                                  "Sweden", "Denmark","Finland", "Ireland",
                                                  "Croatia", "Lithuania", "Estonia",
                                                  "Malta"])]
#print(jointure)

#On renomme les pays (notamment UK en United Kingdom) pour avoir une cohérence
#avec les coordonnées de chaque pays des bases de données geojson
jointure['region'] = jointure['region'].map({'UK':'United Kingdom',
                                             'France' : 'France',
                                             'Germany': 'Germany',
                                             'Italy': 'Italy',
                                             'Portugal': 'Portugal',
                                             'Greece': 'Greece',
                                             'Spain':'Spain',
                                             'Netherlands':'Netherlands',
                                             'Sweden':'Sweden', 
                                             'Denmark':'Denmark',
                                             'Finland':'Finland',
                                             'Ireland':'Ireland',
                                             'Croatia':'Croatia',
                                             'Lithuania':'Lithuania',
                                             'Estonia':'Estonia',
                                             'Malta': 'Malta'},na_action=None)
#print(jointure)

#On supprime les doublons de pays, on ne garde qu'un seul CNO par pays
jointure = jointure.drop_duplicates(subset = "region")
#print(jointure)

#Converts decimal longitude/latitude to Web Mercator format
def coor_wgs84_to_web_mercator(lon, lat):
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return (x,y)

#Analyse des fichier JSON pour avoir les pays
fp = open("countries.geojson","r",encoding='utf-8')
dico = json.load(fp)

fp2 = open("capitals.geojson","r",encoding='utf-8')
caps = json.load(fp2)

#Liste des pays européens que l'on souhaite conserver
mesPays = ["France","Germany","Portugal","Italy","United Kingdom", "Greece",
           "Spain", "Netherlands", "Sweden", "Denmark", "Finland", "Ireland",
           "Croatia", "Lithuania", "Estonia", "Malta"]

#Récupération des coordonnées pour chaque pays
dicoPays = {}
dicoCode = {}
for p in caps["features"]:
    nom = p["properties"]["country"]
    code = p["properties"]["iso2"]
    dicoPays[nom]=code
    dicoCode[code]=nom

mesCodes = [dicoPays[p]for p in mesPays]


nom = []
coordx = []
coordy=[]

for p in dico["features"]:
    code = p["properties"]["cca2"].upper()
    if code in mesCodes :
        pays = dicoCode[code]
        zones = p["geometry"]["coordinates"]
        for poly in zones :
            for liste in poly :
                coord = [coor_wgs84_to_web_mercator(c[0], c[1]) for c in liste]
                coordx.append([c[0] for c in coord])
                coordy.append([c[1] for c in coord])
                nom.append(pays)

#Pour chaque pays, coordonnées pour pouvoir représenter sur une carte
df = pd.DataFrame({'pays': nom, 'coordx': coordx, 'coordy':coordy})
#print(df)

#Jointure finale avec le dataframe précédent pour avoir les nombres de participants 
#dans chaque pays
jointure_finale = df.merge(jointure, left_on = "pays", right_on = "region")
#print(jointure_finale)

#Construction de la carte 
source = ColumnDataSource(jointure_finale)

p2 = figure(x_axis_type="mercator", y_axis_type="mercator", active_scroll="wheel_zoom", 
            title="Nombre de participants aux JO entre 1916-2016 par pays",
            plot_width=1000,plot_height=700)

#Mise en forme du titre du graphique
p2.title.text_color = Plasma256[58]
p2.title.text_font_size = '20pt'

#Arrière-plan de la carte
tile_provider = get_provider(Vendors.CARTODBPOSITRON)
p2.add_tile(tile_provider)

#Au survol des données : le nom du pays considéré et le nombre de participants
hover_tool = HoverTool(tooltips=[( 'Pays',   '@pays'), ('Nombre d\'athlètes féminines','@NB_FEMMES'),
                                 ('Nombre d\'athlètes masculins','@NB_HOMMES'),('Nombre total d\'athlètes','@NB_TOTAL')])
p2.add_tools(hover_tool)

p2.border_fill_color = "whitesmoke"

p2.patches(xs="coordx",ys="coordy",source =source,color = factor_cmap('pays', palette=Category20[len(mesPays)], factors=mesPays),alpha=0.7)

curdoc().add_root(p2)
