#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import folium
import urllib
from urllib import request


def arret_bus(): #fonction qui retourne une liste de tuples des noms des arrêts de bus et des bus qui y passent
    url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-topologie-dessertes-td&facet=libellecourtparcours&facet=nomcourtligne&facet=nomarret&facet=estmonteeautorisee&facet=estdescenteautorisee&rows=10000"
    #on a augmenté les lignes pour avoir tout les arrêts de bus
    fp = urllib.request.urlopen(url)
    contenu = fp.read().decode("utf-8")
    dico = json.loads(contenu)
    lst = []
    for dico_record in dico["records"]:
        lst.append((dico_record["fields"]["nomarret"], dico_record["fields"]["nomcourtligne"]))
    return lst



def equipement_bus(): #fonction qui retourne un dictionnaire avec comme clé les coordonnées des arrêts
                      #en valeurs, le nom de l'arrêt, le nom de la commune de l'arrêt et le mobilier de l'arrêt
    url1 = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-topologie-pointsarret-td&facet=codeinseecommune&facet=nomcommune&facet=estaccessiblepmr&facet=mobilier&rows=5000"
    fp1 = urllib.request.urlopen(url1)
    contenu1 = fp1.read().decode("utf-8")
    dico1 = json.loads(contenu1)
    dico_coordonnees = {}
    for dico_record in dico1["records"]:
        nomcommune = dico_record["fields"]["nomcommune"]
        nomarret = dico_record["fields"]["nom"]
        mobilier = dico_record["fields"].get("mobilier","Pas de mobilier à cette station") 
        latitude = dico_record["fields"]["coordonnees"][0]
        longitude = dico_record["fields"]["coordonnees"][1]
        dico_coordonnees[latitude, longitude] = [nomarret, nomcommune, mobilier]   
    return dico_coordonnees



def concatenation(mes_arrets, equipement): #fonction qui prend en paramètres ce que retourne les 2 fonctions précédentes
                                           #qui retourne un dictionnaire qui a comme clé les coordonnées de l'arrêt de bus
                                           #et comme valeurs : le nom de l'arrêt, sa commune, son mobilier et le nom du bus qui y passe
    for cor, equi in equipement.items():
        for tuples in mes_arrets:
            if equi[0] == tuples[0] : #si c'est le même nom d'arrêt
                equi.append(tuples[1])  #on ajoute aux valeurs du dictionnaire equipement le nom de la ligne qui passe à l'arrêt
                equipement[cor] = equi
    return equipement
    

arret = arret_bus()              
bus_equip = equipement_bus()


final = concatenation(arret, bus_equip)



logo_url = "https://d30y9cdsu7xlg0.cloudfront.net/png/368019-200.png" #pour l'icône
carte_bus = folium.Map(location=[48.1133, -1.6633], zoom_start=13.5, tiles='Stamen Terrain') #fond de carte

for coordonnees, valeur in concatenation(arret, bus_equip).items(): 
    icon1 = folium.features.CustomIcon(logo_url,icon_size=(20, 20)) #ajoute les points sur la carte
    #infos : contenu de la bulle quand on clique sur un arrêt de bus, on y crée la liste des bus qui passe à l'arrêt
    infos = "<p style='width: 12em; height: 100%;'><h3>"+valeur[0]+"</h3></p>" +"<p><h5>Informations : </h5></p>"+ "<p><i>Nom commune : </i>"+valeur[1]+"</p>" + "<p><i>Mobilier : </i>" + valeur[2]+"</p>"+ "<p><i> Lignes de bus qui passent à cet arrêt : </i>"+str(list(set(([valeur[i] for i in range(3, len(valeur))]))))+"</p>"  
    folium.Marker(coordonnees, tooltip = "Information sur l'arrêt de bus {}".format(valeur[0]), popup=infos, icon=icon1).add_to(carte_bus)

carte_bus.save('carte_bus.html') #crée la carte au format html
  
