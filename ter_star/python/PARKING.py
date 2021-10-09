# -*- coding: utf-8 -*-


import json

import folium
import urllib
from urllib import request



def parking_actualiser(): #fonction qui retourne un dictionnaire avec comme clé les coordonnées du parc-relais
                          #et comme valeurs son nom, son nombre de places disponibles et son nombre de places disponible pour PMR
    url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-parcsrelais-etat-tr&facet=nom&facet=etat"
    fp = urllib.request.urlopen(url)
    contenu = fp.read().decode("utf-8")
    dico = json.loads(contenu)
    dico_coordonnees = {}
    for dico_record in dico["records"]: 
        nom = dico_record["fields"]["nom"]
        placesdispo = dico_record["fields"]["nombreplacesdisponibles"]
        placesdispopmr = dico_record["fields"]["nombreplacesdisponiblespmr"]
        latitude = dico_record["fields"]["coordonnees"][0]
        longitude = dico_record["fields"]["coordonnees"][1]
        dico_coordonnees[latitude, longitude] = [nom, placesdispo, placesdispopmr]   
    return dico_coordonnees


def adresse_parking(dico_parking): #fonction qui prend en paramètre le dictionnaire de la fonction précédente
                                     #et qui rend ce dictionnaire avec l'adresse du parc-relais en plus dans les valeurs
    n_rows = 10
    url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-parcsrelais-topologie-td&rows={}&facet=codeinseecommune&facet=nomcommune&facet=datemiseservice".format(n_rows)
    fp = urllib.request.urlopen(url)
    contenu = fp.read().decode("utf-8")
    dico = json.loads(contenu)
    for dico_record in dico["records"]: 
        voie = dico_record["fields"]["adressevoie"]
        latitude = dico_record["fields"]["coordonnees"][0]
        longitude = dico_record["fields"]["coordonnees"][1]
        for cle, val in dico_parking.items():
            if cle == (latitude, longitude) : #si les coordonnées sont les mêmes
                val.append(voie)
                dico_parking[cle] = val 
    return dico_parking

dico_parking = parking_actualiser()

carte_parkings = folium.Map(location=[48.0833, -1.6833], zoom_start=12, tiles='Stamen Terrain') #fond de carte



logo_url = 'https://image.flaticon.com/icons/png/512/421/421836.png' #icone


for coordonnees, valeur in adresse_parking(dico_parking).items():
    icon1 = folium.features.CustomIcon(logo_url,icon_size=(40, 40))
    infos = "<p style='width: 12em; height: 100%;'><h3>"+valeur[0]+"</h3></p>" +"<p><h5>Informations : </h5></p>"+ "<p>"+valeur[3]+"</p>" + "<p><i>Places disponibles : </i>" + str(valeur[1])+"</p>" + "<p> <i>Places disponibles (PMR) : </i>" + str(valeur[2])+"</p>"
    folium.Marker(coordonnees, tooltip = 'Information sur le parc-relais {}'.format(valeur[0]), popup=infos, icon=icon1).add_to(carte_parkings)

carte_parkings.save('carte_parking.html') #on crée la carte au format html





