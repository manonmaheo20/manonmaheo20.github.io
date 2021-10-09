#!/usr/bin/python3
# -*- coding:utf8 -*-

"""Visualisation de données sur les Jeux Olympiques"""

###############################################################################
# fichier  : ManonMAHEO.py
# Auteur : MAHEO Manon
###############################################################################

#Le fichier de données à notre disposition (athlete_events.csv) contient 271116
#lignes et 15 colonnes. Chaque ligne correspond à un athlète individuel 
#participant à une épreuve olympique individuelle (épreuves d'athlète). 
#Les colonnes sont :
#ID (ID) - Numéro unique pour chaque athlète
#Nom (Name) - Nom de l'athlète
#Sexe (Sex) - M ou F
#Âge (Age) - Entier
#Hauteur (Height) - En centimètres
#Poids (Weight) - En kilogrammes
#Équipe (Team) - Nom de l'équipe
#CNO (NOC) - Comité national olympique Code à 3 lettres
#Jeux (Games) - Année et saison
#Année (Year) - Entier
#Saison (Season) - Été ou hiver
#Ville (City) - Ville hôte
#Sport (Sport) - Sport
#Événement (Event) - Événement
#Médaille (Medal) - Or, argent, bronze ou NA 

#Cet ensemble de données offre l'occasion de poser des questions sur l'évolution
#des Jeux olympiques au fil du temps, y compris des questions sur la participation
#et la performance des femmes par rapport aux hommes. 

#C'est pourquoi, dans un premier temps, un premier graphique présentera le nombre de médaillés 
#d'or sur une période de 100 ans (1916-2016) par discipline. L'utilisateur pourra 
#choisir s'il souhaite voir les résultats pour les athlètes féminins, masculins, 
#ou des résultats plus généraux. C'est ici que l'on peut étudier plus ou moins 
#la performance des femmes par rapport aux hommes aux JO sur une période de temps assez large.

#Dans un second temps, sera présenté une cartographie des équipes européennes (une équipe par pays) participant aux JO
#avec la proportions de femmes, d'hommes et les participants totaux pour chacune d'entre elles.
#Par le biais de ce graphique, il sera possible d'étudier la participation 
#des femmes aux JO sur une période de 100 ans (1916-2016) par rapport aux hommes.

#Ces deux graphiques sont présentés à l'aide d'une application Bokeh lancée avec
#bokeh serve.

###############################################################################
# Importation de fonctions externes :
    
import pandas as pd 
from bokeh.plotting import figure, ColumnDataSource
from math import pi
from bokeh.palettes import Plasma256
from bokeh.models import LinearColorMapper
from bokeh.models.widgets import Tabs, Panel
from bokeh.models.widgets import Dropdown
from bokeh.layouts import row
from bokeh.io import curdoc
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import HoverTool
import numpy as np
import json
from bokeh.transform import factor_cmap
from bokeh.palettes import Set1

###############################################################################
# Définition de fonctions : 
    
#Converts decimal longitude/latitude to Web Mercator format
def coor_wgs84_to_web_mercator(lon, lat):
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return (x,y)

###############################################################################
# Corps principal du programme : 

#Importation du fichier de données athlete_events.csv
donnees = pd.read_csv("athlete_events.csv", sep =",")
#print(donnees.head)
#print(donnees.iloc[0])

#CONSTRUCTION DU PREMIER GRAPHIQUE NON-CARTOGRAPHIQUE

#Pour ce premier graphique, on souhaite représenter plus ou moins la performance
#des femmes aux jeux olympiques. En ce sens, on se fixe sur les médailles d'or,
#et on regarde pour chaque type de discipline, sur une période de 100 ans
#(1916-2016) le nombre de médailles d'or pour les athlètes féminins, masculins et total. 

#On récupère les données des jeux olympiques entre 1916 et 2016 (utilisé pour les deux graphiques)
donnees['Year'] = pd.to_datetime(donnees['Year'], format="%Y")
selection = (donnees['Year'] >= '1916') & (donnees['Year'] <= '2016')
donnees2=donnees.loc[selection]
#print(donnees2['Year'])

#On se fixe maintenant sur les médailles d'or pour le premier graphique
donnees3 = donnees2[donnees2.Medal == "Gold"].copy()
#print(donnees3)

#On regroupe par type de sport le nombre de médaillés féminins, masculins
#et le nombre de médaillés total
donnees3["count"] = 1
table = pd.pivot_table(donnees3, index="Sport", columns="Sex",values="count",aggfunc="sum")
table ["total"] = table.sum(axis=1)
#plutôt que d'avoir un NA correspondant à aucun médaillé de type homme ou femme, 
#on met 0 par sécurité pour la construction du graphique
table = table.fillna(0)
#print(table)
#print(table.shape)
#print(table.columns)
#print(table.index)

#Pour construire le graphique, on récupère les données précédentes et on crée
#un jeu de données final sans les index des lignes pour plus de simplicité
liste_hommes = []
liste_femmes = []
liste_total = []
liste_sport = []
for x in table.itertuples():
    liste_hommes.append(x.M)
    liste_femmes.append(x.F)
    liste_total.append(x.total)
for x in table.index :
    liste_sport.append(x)
#print(liste_hommes)
#print(liste_femmes)
#print(liste_total)    
#print(liste_sport)

donnees_final = pd.DataFrame({'SPORT': liste_sport,
                              'NUMERO':[i for i in range(1,59)], 
                              'NB_HOMMES': liste_hommes,
                              'NB_FEMMES': liste_femmes,
                              'NB_TOTAL': liste_total})
#print(donnees_final)

#Construction du diagramme en barre sur le nombre de médaillés par type de sport,
#on commence par sélectionner les données dans un ColumnDataSource
data = ColumnDataSource({'SPORT':donnees_final['SPORT'],'NUMERO':donnees_final['NUMERO'],
                         'y':donnees_final['NB_HOMMES']})

#Création de l'outil de survol : avoir la discipline et le nombre de médailles
outilsurvol = HoverTool(tooltips=[( 'Discipline','@SPORT'),( 'Nombre de médailles d\'or', '@y' )])

#Figure du graphique : noms des axes, titre, taille graphique, et gestion des outils
p = figure(title = "Nombre de médailles d'or entre 1916-2016 par discipline", 
           x_range=liste_sport, x_axis_label = "Discipline", y_axis_label= "Nombre de médailles d'or",
           plot_width=1000,plot_height=700, tools="pan,wheel_zoom,box_zoom,reset")

#Palette de couleurs pour les barres verticales
exp_cmap = LinearColorMapper(palette=Plasma256, 
                             low = min(donnees_final["NUMERO"]), 
                             high = max(donnees_final["NUMERO"]))

#Construction du diagramme en barres verticales
p.vbar(x='SPORT', top='y', source=data, width=0.8,
       fill_color={"field":"NUMERO", "transform":exp_cmap})

#Mise en forme du titre du graphique
p.title.text_color = Plasma256[58]
p.title.text_font_size = '20pt'

#Changement de l'arrière plan du graphique
p.xgrid.grid_line_color = None
p.border_fill_color = "whitesmoke"

#Avoir une bonne visibilité sur l'axe des abscisses qui est qualitatif,
#c'est le nom des disciplines
p.xaxis.major_label_orientation = pi/2

#Mise en forme des titres des axes
p.xaxis.axis_label_text_color= Plasma256[1]
p.xaxis.axis_label_text_font_style = "bold"
p.yaxis.axis_label_text_color= Plasma256[1]
p.yaxis.axis_label_text_font_style = "bold"

#Ajout de l'outil de survol au graphique
p.add_tools(outilsurvol)

#Création du widgets : menu déroullant pour choisir le type de données
menu = Dropdown(label ="Sélectionner les athlètes",menu=[('Athlètes masculins','NB_HOMMES'),
                                                          ('Athlètes féminines','NB_FEMMES'),
                                                          ('Tous les athlètes','NB_TOTAL')])

#Définition des callback functions
def callback_menu(new):
    data.data = {'SPORT':donnees_final['SPORT'],'NUMERO':donnees_final['NUMERO'],'y':donnees_final[new.item]}

menu.on_click(callback_menu)


layout = row(p,menu)
curdoc().add_root(layout)