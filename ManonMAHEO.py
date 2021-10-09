#!/usr/bin/python3
# -*- coding:utf8 -*-

"""Visualisation de données sur les Jeux Olympiques"""

###############################################################################
# fichier  : ManonMAHEO.py
# Auteur : Manon MAHEO
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
#et la performance des femmes par rapport aux hommes aux Jeux Olympiques. 

#C'est pourquoi, dans un premier temps, un premier graphique présentera le nombre de médailles 
#d'or sur une période de 100 ans (1916-2016) par discipline. L'utilisateur pourra 
#choisir s'il souhaite voir les résultats pour les athlètes féminins, masculins, 
#ou des résultats plus généraux. C'est ici que l'on peut étudier plus ou moins 
#la performance des femmes par rapport aux hommes aux JO sur une période de temps assez large.
#Il sera aussi intéressant de remarquer quelles sont les displines qui accordent 
#le plus de médailles d'or et qui par conséquent, ont eu beaucoup plus d'évenements.

#Dans un second temps, sera présentée une cartographie de quelques équipes européennes 
#(une équipe par pays) participant aux JO avec la proportions de femmes, d'hommes
#et les participants totaux pour chacune d'entre elles.
#Par le biais de ce graphique, il sera possible d'étudier la participation 
#des femmes aux JO sur une période de 100 ans (1916-2016) par rapport aux hommes.

#Ces deux graphiques sont présentés à l'aide d'une application Bokeh lancée avec
#bokeh serve.

###############################################################################
# Importation de fonctions externes :

import pandas as pd #pour l'importation des fichiers de données en dataframe
from bokeh.plotting import figure, ColumnDataSource #pour la construction de graphiques
from math import pi #pour avoir une orientation de pi/2 des noms des x dans le premier graphique 
from bokeh.palettes import Plasma256 #palette de couleurs pour le premier graphique
from bokeh.models import LinearColorMapper #pour les couleurs des barres verticales
from bokeh.models.widgets import Tabs, Panel #pour la partition de l'application
from bokeh.models.widgets import Dropdown #pour le menu déroullant
from bokeh.layouts import row #pour faire une partition de la première page
from bokeh.io import curdoc #pour lancer les graphiques en bokeh serve
from bokeh.tile_providers import get_provider, Vendors #pour la carte
from bokeh.models import HoverTool #pour les outils de survol de données
import numpy as np #pour la fonction de conversion des coordonnées
from bokeh.transform import factor_cmap #pour les patches du deuxième graphique
from bokeh.palettes import Category20 #palette de couleurs pour le deuxième graphique
import json #pour les fichiers de données geojson contenant les coordonnées des pays

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

#Importation du fichier de données principal athlete_events.csv
donnees = pd.read_csv("athlete_events.csv", sep =",")
#print(donnees.head)
#print(donnees.iloc[0])

#On récupère les données des jeux olympiques entre 1916 et 2016 (utilisé pour les deux graphiques)
donnees['Year'] = pd.to_datetime(donnees['Year'], format="%Y")
selection = (donnees['Year'] >= '1916') & (donnees['Year'] <= '2016')
donnees2=donnees.loc[selection]
#print(donnees2['Year'])




#CONSTRUCTION DU GRAPHIQUE CARTOGRAPHIQUE

#Pour ce graphique, on souhaite représenter plus ou moins la participation
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
#print(table2.index) #on a 225 Comité National Olympique Code à 3 lettres

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
#print(jointure['region'].unique())

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

#On supprime les doublons de pays, on ne garde qu'une seule équipe par pays
jointure = jointure.drop_duplicates(subset = "region")
#print(jointure)

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

p1 = figure(x_axis_type="mercator", y_axis_type="mercator", active_scroll="wheel_zoom", 
            title="Nombre d'athlètes participant aux JO entre 1916-2016 par pays européen",
            plot_width=1000,plot_height=650)

tile_provider = get_provider(Vendors.CARTODBPOSITRON)
p1.add_tile(tile_provider)

p1.patches(xs="coordx",ys="coordy",source =source,color = factor_cmap('pays', palette=Category20[len(mesPays)], factors=mesPays),alpha=0.7)

#Mise en forme du titre du graphique
p1.title.text_color = Plasma256[58]
p1.title.text_font_size = '15pt'

#Mise en forme de l'arrière plan du graphique
p1.border_fill_color = "whitesmoke"

#Outil de survol des données : on veut le noms des pays, le nombre d'athlètes féminins
#masculins et total
hover_tool = HoverTool(tooltips=[( 'Pays',   '@pays'), ('Nombre d\'athlètes féminines','@NB_FEMMES'),
                                 ('Nombre d\'athlètes masculins','@NB_HOMMES'),('Nombre total d\'athlètes','@NB_TOTAL')])
p1.add_tools(hover_tool)




#CONSTRUCTION DU GRAPHIQUE NON-CARTOGRAPHIQUE

#Pour ce graphique, on souhaite représenter plus ou moins la performance
#des femmes aux jeux olympiques. En ce sens, on se fixe sur les médailles d'or,
#et on regarde pour chaque type de discipline, sur une période de 100 ans
#(1916-2016) le nombre de médailles d'or pour les athlètes féminins, masculins et total. 
#(étant donné qu'il y aura autant de médailles d'argent et bronze que de médailles d'or,
#puisque on attribut à chaque évènement une médaille de chaque)

#On se fixe sur les médailles d'or obtenues
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
                              #on met un numéro pour avoir un numéro par sport,
                              #plus facile pour la gestion des couleurs 
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
p = figure(title = "Nombre de médailles d'or obtenues entre 1916-2016 par discipline", 
           x_range=liste_sport, x_axis_label = "Disciplines", y_axis_label= "Nombre de médailles d'or obtenues",
           plot_width=1000,plot_height=650, tools="pan,wheel_zoom,box_zoom,reset")

#Palette de couleurs pour les barres verticales
exp_cmap = LinearColorMapper(palette=Plasma256, 
                             low = min(donnees_final["NUMERO"]), 
                             high = max(donnees_final["NUMERO"]))

#Construction du diagramme en barres verticales
p.vbar(x='SPORT', top='y', source=data, width=0.8,
       fill_color={"field":"NUMERO", "transform":exp_cmap})


#Ajout de l'outil de survol au graphique
p.add_tools(outilsurvol)

#Mise en forme du titre du graphique
p.title.text_color = Plasma256[58]
p.title.text_font_size = '15pt'

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

#Création du widgets : menu déroullant pour choisir le type de données
menu = Dropdown(label ="Sélectionner les athlètes",menu=[('Athlètes masculins','NB_HOMMES'),
                                                          ('Athlètes féminines','NB_FEMMES'),
                                                          ('Tous les athlètes','NB_TOTAL')])

#Définition des callback functions
def callback_menu(new):
    data.data = {'SPORT':donnees_final['SPORT'],'NUMERO':donnees_final['NUMERO'],'y':donnees_final[new.item]}

menu.on_click(callback_menu)




#PARTITION DE L'APPLICATION BOKEH EN DEUX PANELS

layout = row(p,menu)

tab1 = Panel(child=layout, title="Thème 1 : Performance aux Jeux-Olympiques")
tab2 = Panel(child=p1, title="Thème 2 : Participation aux Jeux-Olympiques")
tabs = Tabs(tabs = [tab1, tab2])

curdoc().add_root(tabs)