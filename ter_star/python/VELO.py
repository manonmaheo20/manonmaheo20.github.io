# =============================================================================
# IMPORTS
# =============================================================================
import json
import folium
import urllib
from geopy.distance import distance

# =============================================================================
# FONCTIONS
# =============================================================================

#Permet de retourner les informations principales des stations de vélo à partir de la base de données "Topologie des stations de vélos en libre-service"
def topologie_velo():
    n_rows = 300
    url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=vls-stations-topologie-td&rows={}&facet=codeinseecommune&facet=nomcommune&facet=coordonnees&facet=nombreemplacementstheorique&facet=possedetpe".format(n_rows)
    fp = urllib.request.urlopen(url)
    contenu = fp.read().decode("utf-8")
    dico = json.loads(contenu)
    dico_topologie = {}

    for dico_record in dico["records"]:
        nom = dico_record["fields"]["nom"]
        nb_emplacements_theo = dico_record["fields"]["nombreemplacementstheorique"]
        id = dico_record["fields"]["id"]
        num_adresse = dico_record["fields"].get("adressenumero", "")
        adresse = dico_record["fields"]["adressevoie"]
        latitude = dico_record["fields"]["coordonnees"][0]
        longitude = dico_record["fields"]["coordonnees"][1]
        idstationproche = dico_record["fields"]["idstationproche1"]
        dico_topologie[latitude, longitude] = [nom, num_adresse, adresse, nb_emplacements_theo, idstationproche]
    return (dico_topologie)

#La base de données "Etat des stations de vélos en libre-service en temps réel" permet de compléter notre dico avec de nouvelles informations
def etat_station_velo(objet_topologie_velo):
    n_rows = 200
    url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=vls-stations-etat-tr&rows={}&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles".format(n_rows)
    fp = urllib.request.urlopen(url)
    contenu = fp.read().decode("utf-8")
    dico = json.loads(contenu)

    #Création du dictionnaire à partir du dico précédent
    dico_etat = dict(objet_topologie_velo)
    #Définition des informations qui nous intéresse
    for dico_record in dico["records"]:
      latitude = dico_record["fields"]["coordonnees"][0]
      longitude = dico_record["fields"]["coordonnees"][1]
      etat = dico_record["fields"]["etat"]
      nbvelosdispo = dico_record["fields"]["nombrevelosdisponibles"]
      nombreemplacementsactuels = dico_record["fields"]["nombreemplacementsactuels"]
      id = dico_record["fields"]["idstation"]

    #Ajout des informations dans le dictionnaire précédent
      for cle, val in dico_etat.items():
        if cle == (latitude, longitude) : 
          val.append(id)
          val.append(etat)
          val.append(nbvelosdispo)
          val.append(nombreemplacementsactuels)
          dico_etat[(latitude, longitude)] = val
    return (dico_etat)

#Cette fonction permet de retourner un dico [coordonnées_station] = [id, distance] pour l'id de la station la plus proche
def distance_stations(dico_etat) : 
  dico_final = dict(dico_etat)
  #Récupération des données utiles
  dico_id = {}
  for coordonnees, valeurs in dico_etat.items():
    id = valeurs[5]
    stationproche = valeurs[4]
    dico_id[id] = [stationproche]

  #Créatin du dico des coordonnées
  dico_coordonnees = {}
  for id_station, stationproche in dico_id.items():
    coord = conversion_id_coord(id_station)
    dico_coordonnees[id_station, coord] = stationproche

  for cle, liste_id_station_proche in dico_coordonnees.items():
    for station_proche in liste_id_station_proche :
      coordonnees_station_proche = conversion_id_coord(str(station_proche))  
    dico_coordonnees[cle] = [liste_id_station_proche, coordonnees_station_proche]

  #Calcul des distances en km pour chaque station
  dico_distance = {}
  for station, coord in dico_coordonnees.items():
    d1 = round((distance(station[1], coord[1]).m),1)
    dico_distance[station[0]]= [coord[0][0], d1]

  for coordonnees, val in dico_final.items():
    for station, dist in dico_distance.items():
      if val[5] == station :
        val.append(conversion_id_nom(dist[0]))
        val.append(dist[1])
    dico_final[coordonnees] = val
  return(dico_final)

#Permet de retourner les coordonées d'un id quelconque
def conversion_id_coord(id_station):
  for coordonnees, id in dico_correspondance_id_coord.items():
    if id_station == id :
      return(coordonnees)

#Permet de retourner le nom d'un id quelconque
def conversion_id_nom(id_station):
  for nom, id in dico_correspondance_id_nom.items():
    if str(id_station) == id :
      return(nom)

# =============================================================================
# IMAGE
# =============================================================================
logo_url = "https://www.android-logiciels.fr/wp-content/uploads/2014/07/Paris-Velib-icone-1.png"

# =============================================================================
# CODE
# =============================================================================
dico_correspondance_id_coord = {}
for coordonnees, valeurs in (etat_station_velo(topologie_velo())).items():
  dico_correspondance_id_coord[coordonnees] = valeurs[5]

dico_correspondance_id_nom = {}
for valeurs in (etat_station_velo(topologie_velo())).values():
  dico_correspondance_id_nom[valeurs[0]] = valeurs[5]

# =============================================================================
# CARTE
# =============================================================================
carte_velos = folium.Map(location=[48.0833, -1.6833], zoom_start=12, tiles='Stamen Terrain')

for coordonnees, valeur in distance_stations(etat_station_velo(topologie_velo())).items():
    icon1 = folium.features.CustomIcon(logo_url,icon_size=(30, 30)) 
    infos = "<center><p style='width: 16em; height: auto;'><h4> {} </h4></p><p><h5>Informations : </h5></p><p> {} {}</p><p><strong> Etat : {} </strong></p><p>Nombre  de vélos disponibles actuellement : {} </p><p> Nombre de places disponibles : {}</p> <p> Station la plus proche : {} à {} mètres</p> </center>".format(valeur[0], valeur[1], valeur[2], valeur[6], valeur[7], valeur[8], valeur[9], valeur[10]) 
    folium.Marker(coordonnees, tooltip = 'Information sur la station de vélos {}'.format(valeur[0]), popup=infos, icon=icon1).add_to(carte_velos)

carte_velos.save('carte_velos.html')

