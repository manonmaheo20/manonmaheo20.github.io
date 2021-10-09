######## CHARGEMENT DES PACKAGES ########

library(shiny)
library(tidyverse)
library(shinyWidgets)
library(leaflet)
library(dygraphs)
library(sf)
library(rAmCharts)
library(plotly)
library(rsconnect)
library(highcharter)
library(here)
library(rnaturalearthdata)
library(rgeos)
library(DT)

######## PARTIE UI ########

shinyUI(
    
    navbarPage(
        
        title = img(src="img/ClimateTracker.png", height="80px", id="ClimateTracker"), #logo de l'application
        windowTitle = "Changement climatique", #nom de l'onglet
        theme = "style/style.css", #utilisation du fichier style.css
        collapsible = TRUE, #pour que lorsque l'affichage se réduit, le menu devient une liste
        footer = includeHTML("footer.html"), #footer des pages de l'application
    
        # ----------------------------------
        # tab panel 1 - Page d'accueil 
        
        tabPanel(title = "Accueil",
                 includeHTML("accueil.html"), #carrousel d'images
        ),#fin tab panel 1
        
        # ----------------------------------
        # tab panel 2 - Conséquences à l'échelle mondiale
        
        tabPanel(title = "Échelle mondiale",
                 HTML('<center><h2 style="color:#0B4F6C"><strong>Quel climat pour demain ?</strong></h2></center>'),
                 HTML('<center><h3 style="color:#0B4F6C">Évolution de la température moyenne à l\'échelle du globe</h2></center>'),
                 leafletOutput(outputId = "texte",width="100%"),
                 absolutePanel(style="background-color:white;padding:2px 5px;opacity:0.75;",
                     top = 170, left = 75, width = 270,height = "auto",
                      
                     tags$div(class = "distribution",h6(textOutput("titre"), align = "right")),
                      h6(textOutput("moy_annee"), align = "right"),
                
                       plotOutput("temp2",height  =  "200px"),
                      
                       sliderInput(inputId = "idSlider2", label = "Sélectionnez une année :",min=2021, max=2039,
                                  value = 2021,sep=""),
                       selectInput(inputId = "idSelect", label = "Sélectionnez un mois : ", selected = "Jan Average",
                                choices = c("Janvier" = "Jan Average", "Février" = "Feb Average", "Mars" = "Mar Average","Avril"="Apr Average",
                                            "Mai"="May Average","Juin"="Jun Average","Juillet"="Jul Average","Aout"="Aug Average","Septembre"="Sep Average","Octobre"="Oct Average",
                                            "Novembre"="Nov Average","Decembre"="Dec Average")),
                  ),
        ),#fin tab panel 2     
                  
        # ----------------------------------
        # tab panel 3 - Déterminants climatiques à l'échelle européenne
        
        tabPanel(title = "Échelle européenne",
                 tabsetPanel(
                     tabPanel("Anomalie de la température moyenne annuelle de l'air",
                              HTML('<br><h3 style="color:#01BAEF"><center><strong>Zoom sur l\'évolution des températures à l\'échelle européenne</strong></center></h3><br>'),
                              HTML('<img src="img/indice1_1.png" width = "50%">'),
                              HTML("<br><br>"),
                              fluidRow( column(6,plotlyOutput("indice2_1")),
                                        column(6,dygraphOutput("indice2_2"))
                                      ),
                              HTML('<br><br>'),
                              HTML('<img src="img/indice1_2.png" width = "50%" align=right>'),
                              HTML('<br><br><br><br>'),
                             ),
                     tabPanel("Émission de gaz à effet de serre",
                              fluidRow(column(4,HTML("<br>"),HTML('<h3 style="color:#01BAEF";><center><strong>Emission de gaz à effet de serre</center></strong></h3><br>'),
                                              sidebarPanel("Visualisez l'émission de gaz à effet de serre (GES)",style="background-color:#01BAEF;padding:2px 5px;opacity:0.75;color:white;",width="100%",
                                                             textInput(inputId = "indice1", label = "Entrez un pays (exemple : France) : ", value = "France"),
                                                             selectInput(inputId = "var", label = "Choisissez une année : ", choices = colnames(indice)[2:ncol(indice)]),
                                                             textInput(inputId = "indice3", label = "Entrez un autre pays pour comparer dans le dernier graphique (exemple : Belgique) : ", value = "Belgique"),
                                              actionButton("update", "Visualisez")),
                                              HTML("<p>(*) : Le deuxième graphique permet de se rendre compte de la situation du premier pays donné par rapport aux autres, en fonction du maximum et
                                                   du minimum d'émission de GES tous pays confondus. </p>")),
                                       column(4,HTML("<br><br>"),amChartsOutput("indice")),HTML("<br><br>"),column(4,amChartsOutput("indice_2"))),
                              HTML("<br> <br>"),
                              fluidRow(column(6,highchartOutput("indice_3")),column(6,highchartOutput("indice_4")))),
                     
                     tabPanel("Émissions de gaz à effet de serre par activité",
                              HTML("<br>"),
                              highchartOutput("indice3_1"),
                              HTML("<p>Lecture : en 2019, le secteur d’activité du transport routier émet une quantité de gaz à effet de serre équivalant à 127,7 millions de tonnes de CO2.</p>"))
                     )
        ),#fin tab panel 3
        
        # ----------------------------------
        # tab panel 4 - Initiatives en faveur du climat à l'échelle nationale
        
        tabPanel(title="Échelle nationale",
                 navlistPanel(
                     tabPanel("Production d'énergies renouvelables", 
                              HTML('<center><h2 style="color:#20BF55"><strong>Quelles initiatives ?</strong></h2></center>'),
                              HTML('<center><h3 style="color:#20BF55">La production d\'énergies renouvelables en France</h2></center>'),
                              leafletOutput(outputId = "france",width="100%"),
                              sidebarPanel(style="background-color:white;padding:2px 5px; color:#20BF55;",
                                           top = 130, right = 0, width = 270,height = "auto",
                                            sliderInput(inputId = "nouveau", label = "Sélectionnez une année : ", min = 2008, max=2015, value=2008, sep=""),
                                            selectInput(inputId = "var2", label = "Sélectionnez un type de production : ", choices = c("Production hydraulique renouvelable"="production_hydraulique_renouvelable",
                                                                                                                             "Production bioénergies renouvelable" ="production_bioenergies_renouvelable",
                                                                                                                             "Production éolienne renouvelable"= "production_eolienne_renouvelable",
                                                                                                                             "Production solaire renouvelable" = "production_solaire_renouvelable",
                                                                                                                             "Production électrique renouvelable" = "production_electrique_renouvelable",
                                                                                                                             "Production gaz renouvelable" = "production_gaz_renouvelable"))
                                           )),
                     
                     tabPanel("Production d'énergies renouvelables par région",
                              HTML('<center><h2 style="color:#20BF55"><strong>Quelles initiatives ?</strong></h2></center>'),
                              HTML('<center><h3 style="color:#20BF55">La production d\'énergies renouvelables en France, par régions</h2></center><br><br>'),
                              sidebarPanel(style="background-color:white;padding:2px 5px; color:#20BF55;", top = 130, right = 0, width = 270,height = "auto",
                                           sliderInput(inputId = "annee_region", label = "Sélectionnez une année:",min=2008, max=2020,
                                                       value = 2008,sep=""),
                                           selectInput(inputId = "region", label = "Sélectionnez une région", selected = 2, choices = c("Bretagne" = "53", "Nouvelle-Aquitaine" = "75",
                                                                                                                                               "Ile-de-France" ="11", "Centre - Val de Loire"="24",
                                                                                                                                               "Bourgogne - Franche-Comté"="27", "Normandie"= "28",
                                                                                                                                               "Hauts-de-France"="32","Grand-Est"= "44",
                                                                                                                                               "Pays de la Loire"= "52", 
                                                                                   "Occitanie"="76", "Auvergne-Rhône-Alpes"="84", "Provence-Alpes-Côte d'Azur"="93","Corse"="94")),
                                           amChartsOutput("graph_regions"),
                              )
                 ),
                 
                 tabPanel("Classification des régions françaises",HTML('<center><h3 style="color:#20BF55"><strong>Classification ascendante hiérarchique des régions</strong></h3></center>'),
                          HTML('<center><h4 style="color:#20BF55">Quel regroupement des régions en fonction de leur production d\'énergies renouvelables ?</h4></center><br>'),
                          sidebarPanel(style="background-color:white;padding:2px 5px; color:#20BF55;", top = 130, right = 0, width = 270,height = "auto",
                                       sliderInput(inputId = "idSlider5", label = "Sélectionnez une année:",min=2008, max=2015,
                                                   value = 2008,sep=""),
                                       sliderInput(inputId = "choix_8", label = "Sélectionnez un nombre de groupes:",min=2, max=11,
                                                   value = 2),
                                       plotOutput("classi")),
                 )
        )),
        
        # ----------------------------------
        # tab panel 5 - Données utilisées
        
        navbarMenu("Nos données",
                 
                     tabPanel("Données mondiales",HTML('<h4 style="color:#757575"><strong>Températures mensuelles moyennes</strong></h4>'),dataTableOutput(outputId = "dataTable1")),
                     tabPanel("Données européennes",HTML('<h4 style="color:#757575"><strong>Anomalies de températures</strong></h4>'),dataTableOutput(outputId = "dataTable2"),HTML('<br><h4 style="color:#757575"><strong>Émission de gaz à effet de serre</strong></h4>'),dataTableOutput(outputId = "dataTable2_2"),HTML('<br><h4 style="color:#757575"><strong>Émission de gaz à effet de serre par activité</strong></h4>'), dataTableOutput(outputId = "dataTable2_3")),
                     tabPanel("Données françaises",HTML('<h4 style="color:#757575"><strong>Production d\'énergies renouvelables</strong></h4>'),dataTableOutput(outputId = "dataTable3"))
                 
        ),#fin du tab panel 5
        
        # ----------------------------------
        # tab panel 6 - Informations et médias
        
        tabPanel(title="À propos", 
                 
                 fluidRow(
                     HTML('<br><center><img src="img/apropos.png" width = "70%"></center><br>'),
                 ),
                 
                 fluidRow(
                     HTML('<center><img src="img/apropos1.png" width = "80%"></center><br>'),
                     column(3),
                     column(6,
                            tags$div(class="apropos", 
                                     HTML("<p>Le<strong> réchauffement climatique</strong> est le constat d’une augmentation de la température terrestre moyenne sur de longues périodes. 
                                          On parle aussi de <strong>changement climatique</strong> ou de <strong>dérèglements climatiques</strong> car on note des changements importants dans 
                                          les phénomènes climatiques : plus de canicules, ou inversement plus de précipitations, fréquence des tempêtes ou des ouragans 
                                          plus élevés, etc. <br><br>Il s’agit d’étudier et d’anticiper les variations de température pour l’ensemble du globe et sur des temps 
                                          longs <em>(étude du climat à grande échelle)</em> et non la variabilité des températures à l’échelle de quelques jours ou sur une saison 
                                          <em>(prévisions météorologiques)</em>.</p>"), )
                     ),
                     column(3)
                 ),
                 
                 fluidRow(
                     HTML('<br><br><center><img src="img/apropos2.png" width = "80%"></center><br>'),
                     column(2),
                     column(8,
                            tags$div(class="apropos2",
                                     HTML('<h4 style="color:#757575;"><center><strong>L’effet de serre, un phénomène naturel</strong></center></h4><br>'),
                                     HTML('<p>Un tiers des rayons du soleil que reçoit la terre est renvoyé par elle dans l’atmosphère 
                                 sous forme de rayonnement infrarouge ; les deux tiers restants étant absorbés par les océans et les sols. 
                                 Des gaz naturellement présents dans l’atmosphère, <em>comme l’ozone (O3), la vapeur d’eau (H20), 
                                 le protoxyde d’azote (NO2), le méthane (CH4) ou le dioxyde de carbone (CO2)</em>, empêchent une partie 
                                 de ce rayonnement de s’échapper dans l’espace et le renvoient vers la terre, ce qui la réchauffe. 
                                 C’est l’effet de serre. Ce phénomène naturel nécessaire joue un <strong>rôle de régulateur du climat</strong> et 
                                 permet à la terre d’avoir une température moyenne habitable (15°C au lieu de -18°C).</p>'),
                                     HTML('<h4 style="color:#757575;"><center><strong><br>L’augmentation des gaz à effet de serre due aux activités humaines</strong></center></h4><br>'),
                                     HTML('<p><strong>L’homme a modifié cet équilibre en envoyant de grandes quantités de gaz à effet de serre dans l’atmosphère 
                                 depuis les premières révolutions industrielles jusqu’à nos jours (effet de serre additionnel). </strong>
                                 Principalement du CO2 (77% des émissions) avec l’utilisation massive des énergies fossiles (pétrole, charbon, gaz) mais 
                                 aussi du méthane avec l’agriculture intensive et les décharges. En cause également la déforestation, les forêts ayant un 
                                 rôle de captage du CO2 (puits de carbone). Depuis 1850, le CO2 a augmenté de 40%. Il était de 270 ppm (parties par millions) 
                                 à la fin du 19e siècle. Il atteint les 400 ppm aujourd’hui, la plus forte concentration depuis 800 000 ans ! Sa présence dans 
                                 l’atmosphère peut durer plusieurs centaines d’années. L’augmentation du dioxyde de carbone (ou gaz carbonique) dans l’atmosphère 
                                 est la principale cause du réchauffement climatique.</p>')
                            )),
                     column(2)
                 ),
                 
                 
                 fluidRow(
                     tags$div(class="apropos2",
                              HTML('<br><br><center><img src="img/apropos3.png" width = "80%"></center>'),
                              HTML('<br><center><img src="img/consequences_climat.png" width = "70%"></center><br>'),
                     ),
                 ),
                 
                 
                 fluidRow(
                     HTML('<br><br><center><img src="img/apropos4.png" width = "80%"></center><br>'),
                     column(2),
                     column(8,
                            tags$div(class="apropos2",
                                     HTML('<h4 style="color:#20BF55;"><center><strong>Stratégie d’attenuation</strong></center></h4><br>'),
                                     HTML('<p>Parmi les principaux secteurs émetteurs de GES, on trouve <strong>l’énergie (35%), les transports (14%), 
                                          le l’agriculture (14%), le bâtiment (6%)</strong>… Dans ces secteurs, la révolution pour réduire les émissions de 
                                          gaz à effet de serre est déjà en marche : <em>développement des transports en commun, covoiturage, véhicules électriques, 
                                          rénovation du bâti, bâtiment basse consommation (BBC), réduction ou optimisation des déchets et de l’eau…</em></p><br>'),
                                     HTML('<h4 style="color:#20BF55;"><center><strong>Stratégie d’adaptation</strong></center></h4><br>'),
                                     HTML('<p>Le changement climatique est déjà là et produit des effets réels partout dans le monde.
                                          Il est donc nécessaire de s’adapter. Cela passe par la protection des biens et des personnes 
                                          <em>(plan canicule, plan inondation, lutte contre la précarité énergétique…)</em>, l’entretien et la préservation du 
                                          patrimoine naturel <em>(forêts, dunes, digues…)</em> ou l’aménagement de l’espace urbain <em>(ordonnancement urbain et bâti ; 
                                          fontaines et points de rafraîchissement, espaces verts et végétalisation…)</em>.<br></p>')
                            )),
                     column(2)
                 ),
                 
                 HTML("<br><br>"),
                 HTML('<center><img src="img/apropos5.png" width = "90%"></center>'),
                 HTML("<br>"),
                 HTML('<iframe style = "display: block; margin: auto;" width="640" height="360" src="https://www.youtube.com/embed/T4LVXCCmIKA?hd=1"></iframe>'),
                 
        ) #fin du tab panel 6
        )) #fin du navbarPage et du shinyUI