#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 15:24:43 2020

"""


import json

import folium
import urllib
from urllib import request

def ligne_metro(): #fonction qui récupère une liste de tuples des coordonnées du parcours du métro
    url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-metro-topologie-parcours-td&facet=nomcourtligne&facet=senscommercial&facet=type&facet=nomarretdepart&facet=nomarretarrivee&facet=estaccessiblepmr"
    fp = urllib.request.urlopen(url)
    contenu = fp.read().decode("utf-8")
    dico = json.loads(contenu)
    lst = []
    for dico_record in dico["records"]:
        points = dico_record["fields"]["parcours"]["coordinates"]
    for point in points : 
        latitude = point[0]
        longitude = point[1]
        coordonnees = (longitude, latitude) #obligé d'échanger car dans le jeu de données, on nous fourni l'inverse
        lst.append(coordonnees)
    return(lst)

    
def station_metro(): #fonction qui récupère un dictionnaire qui a comme clé les coordonnées des arrêts de métro
                     #et comme valeurs le nom de l'arrêt et son niveau (nombre d'étages ou sous-sol)
    url2 = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-metro-topologie-stations-td&sort=nom&facet=codeinseecommune&facet=nomcommune&facet=niveaux&rows=25"
    #augmentation du nombre de lignes car sinon il n'y avait pas toutes les stations 
    fp2 = urllib.request.urlopen(url2)
    contenu2 = fp2.read().decode("utf-8")
    dico2 = json.loads(contenu2)
    dico_coordonnees = {}
    for dico_record in dico2["records"]: # Renvoie un dico_record
        nom = dico_record["fields"]["nom"]
        latitude = dico_record["fields"]["coordonnees"][0]
        longitude = dico_record["fields"]["coordonnees"][1]
        niveau = dico_record["fields"]["niveaux"]
        dico_coordonnees[latitude, longitude] = [nom, niveau]
    return dico_coordonnees


def acces_PMR(objet_station_metro): #fonction qui prend comme paramètre le dictionnaire de la fonction précédente
                                    #et qui ajoute aux valeurs de ce dictionnaire l'accessibilité ou non aux PMR
    url2 = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-metro-topologie-pointsarret-td&facet=codeinseecommune&facet=nomcommune&facet=nomstationparente&facet=estaccessiblepmr&rows=30"
    #augmentation du nombre de lignes car sinon il n'y avait pas toutes les stations 
    fp2 = urllib.request.urlopen(url2)
    contenu2 = fp2.read().decode("utf-8")
    dico2 = json.loads(contenu2)
    for dico_record in dico2["records"]: # Renvoie un dico_record
        nom = dico_record["fields"]["nom"]
        if dico_record["fields"]["estaccessiblepmr"] :  
            accessibilitepmr = "Oui"
        else:
            accessibilitepmr = "Non"
        for cle, val in objet_station_metro.items():
            if val[0] == nom : 
                val.append(accessibilitepmr)
                objet_station_metro[cle] = val
    return objet_station_metro


def etat_station(objet_acces_PMR): #fonction qui prend en paramètre le dictionnaire de la fonction précédente
                                   #et qui ajoute aux valeurs de ce dictionnaire l'état de la station (Ouverte ou fermé)
    url3 = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-metro-stations-etat-tr&facet=nom&facet=etat&rows=30"
    #augmentation du nombre de lignes car sinon il n'y avait pas toutes les stations 
    fp3 = urllib.request.urlopen(url3)
    contenu3 = fp3.read().decode("utf-8")
    dico3 = json.loads(contenu3)
    for dico_record in dico3["records"]: # Renvoie un dico_record
        nom = dico_record["fields"]["nom"]
        etat = dico_record["fields"]["etat"]
        for cle, val in objet_acces_PMR.items():
            if val[0] == nom : 
                val.append(etat)
                objet_acces_PMR[cle] = val
    return objet_acces_PMR

mastation = acces_PMR(station_metro())

metro = folium.Map(location=[48.1133, -1.6833], zoom_start=13, tiles='Stamen Terrain') #permet de créer le fond de carte


etat_des_stations = []
for description in etat_station(mastation).values() : 
    etat_des_stations.append(description[-1]) #on ajoute à etat_des_stations l'état des stations
if 'Fermée' in etat_des_stations : #Si une (ou plusieurs) des stations est (sont) fermées, alors on affiche quand on passe la souris que la ligne a un problème
    folium.PolyLine(ligne_metro(), color="red", weight=3, opacity=0.8, tooltip = "Ligne <img src='ligneA.png' alt='A' width='15' height='15'> Attention ! Problème sur la ligne A").add_to(metro)
else : 
    folium.PolyLine(ligne_metro(), color="red", weight=3, opacity=0.8, tooltip = "Ligne <img src='ligneA.png' alt='A' width='15' height='15'>").add_to(metro)

logo_url = 'https://image.flaticon.com/icons/png/512/1183/1183363.png' #pour les icônes


for coordonnees, valeur in etat_station(mastation).items():
    icon1 = folium.features.CustomIcon(logo_url,icon_size=(30, 30)) #pour les icônes
    #infos : bulle d'information quand on clique sur un arrêt de métro
    infos = "<center><p style='width: 13em; height: auto;'><h4> {}</h4></p><p><h5>Informations : </h5></p><p><i> Ligne de métro <img src='ligneA.png' alt='ligneA' width='15' height='15'> </i></p><p>Etat : {}<p>Niveaux : {} </p><p>Accessibilité pour personnes à mobilité réduite : {} </p></center>".format(valeur[0], valeur[-1], valeur[1], valeur[2]) 
    folium.Marker(coordonnees, tooltip = 'Information sur la station {}'.format(valeur[0]), popup=infos, icon=icon1).add_to(metro) #nom de la station qui s'affiche quand on passe la souris
    

metro.save('metro.html') #génère une carte au format html
    
    
    
    
    
    