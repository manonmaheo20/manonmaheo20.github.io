# =============================================================================
# IMPORTS
# =============================================================================
from bokeh.models import HoverTool
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models.widgets import Dropdown
import numpy
import urllib
import json
import pandas

#Permet de reourner le dico  des informations nécessaires pour chaque station à partir de "Etat des stations de vélos en libre-service en temps réel"
def etat_station_velo():
    n_rows = 200
    url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=vls-stations-etat-tr&rows={}&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles".format(n_rows)
    fp = urllib.request.urlopen(url)
    contenu = fp.read().decode("utf-8")
    dico = json.loads(contenu)

    #Création du dictionnaire
    dico_etat = {}
    #Définition des informations qui nous intéresse
    for dico_record in dico["records"]:
        nom = dico_record["fields"]["nom"]
        nbvelosdispo = dico_record["fields"]["nombrevelosdisponibles"]
        nbemplacementsactuels = dico_record["fields"]["nombreemplacementsactuels"]
        dico_etat[nom] = [nbvelosdispo, nbemplacementsactuels]
    return (dico_etat)
        
#Création de 2 listes des infos pour répartir dans les colonnes qui nous intéressent
liste_infos = []
liste_noms = []
for nom, infos in etat_station_velo().items():
    infos.append(nom)
    liste_infos.append(infos)
    liste_noms.append(nom)
    
#Création d'un dataFrame avec nos colonnes
dataVelo = numpy.array(liste_infos)
df = pandas.DataFrame(dataVelo, index = liste_noms, columns = ['NombreVélosDispo', 'NombreEmplacementsDispo', 'NomStation'])
print(df)

#On créé dans le dataframe une colonne avec les valeurs négatives pour avoir l'effet miroir
df['NombreEmplacementsDispo'] = [int(i) for i in df['NombreEmplacementsDispo']]
df['NombreVélosDispo'] = [int(i) for i in df['NombreVélosDispo']]
NombreEmplacementsDispo_neg = - df['NombreEmplacementsDispo']

#Création du graphique 
donnees = ColumnDataSource( data = {'station' : df['NomStation'], 'velos' : df['NombreVélosDispo'], 'emplacements' : df['NombreEmplacementsDispo'],  'emplacements_neg' : NombreEmplacementsDispo_neg })

graphique = figure(y_range=list(df['NomStation']), plot_height=1000, title="Emplacements et vélos disponibles dans chaque station vélos", toolbar_location=None)

#Définition des affichages au survol de la souris
outilsurvol = HoverTool(tooltips = [('Emplacements disponibles ', '@emplacements' ),
                                    ( 'Vélos disponibles ', '@velos')])

graphique.hbar(y='station',right='velos', height=0.9, color='#008383', source=donnees, legend = ['Vélos disponibles'])

graphique.hbar(y='station',right='emplacements_neg', height=0.9, color='#FFBB00', source=donnees, legend = ['Emplacements disponibles'])

graphique.y_range.range_padding = 0.1 #Padding entre le titre et le graphique 
graphique.ygrid.grid_line_color = None
graphique.legend.location = "top_right"
graphique.axis.minor_tick_line_color = None
graphique.outline_line_color = None

#Définition des options du graphique
graphique.xaxis.visible = False

graphique.add_tools(outilsurvol)

show(graphique)