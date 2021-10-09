######## CHARGEMENT DES PACKAGES ########

library(shiny)
library(tidyverse)
library(leaflet)
library(sf)
library(rAmCharts)
library(plotly)
library(rsconnect)
library(readxl)
library(highcharter)
library(lubridate)
library(RColorBrewer)
library(here)
library(lubridate)
library(dygraphs)
library(rnaturalearthdata)
library(rgeos)
library(DT)

######## PARTIE GLOBALE ########

### Chargement des bases de données à l'échelle mondiale ###

temp<-read.csv("donnees/donnes_nettoye.csv",fileEncoding="utf-8")
world <- rnaturalearth::ne_countries(scale = "medium", returnclass = "sf")

temp<-temp[,-1]
temp$ISO3<-gsub("^\\s+|\\s+$", "",temp$ISO3)
temp$Statistics<-gsub("^\\s+|\\s+$", "",temp$Statistics)

world<-world[,10]
world$ISO3<-world$adm0_a3

temp2<-inner_join(world,temp,by="ISO3")

temp3<-temp2[temp2$...5==2037 & temp2$Statistics=="Dec Average" ,]

pal <- colorNumeric(scales::seq_gradient_pal(low = "yellow", high = "red",
                                             space = "Lab"), domain = temp3$Monthly.Temperature....Celsius.,na.color = "transparent")
b <- leaflet() %>% addProviderTiles(providers$CartoDB.Positron) %>%
  
  addPolygons(data = temp3,color=~pal(temp3$Monthly.Temperature....Celsius.),fillOpacity = 0.6, 
              stroke = TRUE,weight=1,
              popup=~paste(as.character(Country),paste(as.character(round(Monthly.Temperature....Celsius.)),"°C"),sep=" : "),highlightOptions = highlightOptions(color="white",weight = 2)) %>% 
  
  addLayersControl(options=layersControlOptions(collapsed = FALSE))  %>%
  
  addLegend(
    title = "Température mensuel",
    pal = pal, values = temp3$Monthly.Temperature....Celsius.,labFormat = labelFormat(suffix = "°"),opacity = 1) %>%
  
  addEasyButton(
    button = easyButton(
      icon = "fa-globe",
      title = "Zoom initial",
      onClick = JS("function(btn, map){ map.setZoom(1); }")
    )) 


### Chargement des bases de données à l'échelle européenne ###

## Evolution des anomalies de températures ##

anomalies <- read.csv("donnees/evolution_anomalie.csv", skip=4)
anomalies <- as_tibble(anomalies)

anomalies <- mutate(anomalies, date = str_c(Year, "01-01", sep = "-") %>% ymd())
theme_strip <- theme_minimal()+
  theme(axis.text.y = element_blank(),
        axis.line.y = element_blank(),
        axis.title = element_blank(),
        panel.grid.major = element_blank(),
        legend.title = element_blank(),
        axis.text.x = element_text(vjust = 3),
        panel.grid.minor = element_blank(),
        plot.title = element_text(size = 14, face = "bold")
  )


col_strip <- brewer.pal(11, "RdBu")

brewer.pal.info

## Indice émission gaz à effet de serre ##

fp <- file.path("donnees", "emission_gaz_effet_serre.xlsx") 

indice <- readxl::read_excel(fp, sheet="Feuille 1")

## Emission de gaz à effet de serre par secteur d'activité ##

secteur <- file.path("donnees", "type_secteurs.xlsx") 
secteur <- readxl::read_excel(secteur, sheet="Données")
secteur <- secteur %>% gather(key = variable, value = valeur, -Secteur)


### Chargement des bases de données à l'échelle nationale ###

bd<-read_sf("donnees/prod-region-annuelle-enr_1.shp")
colnames(bd)[3:9]<-c("production_hydraulique_renouvelable","production_bioenergies_renouvelable","production_eolienne_renouvelable","production_solaire_renouvelable","production_electrique_renouvelable","production_gaz_renouvelable","production_totale_renouvelable")

## Classification ##

bd_name<-read.csv2("donnees/fr_reno_1.csv")

