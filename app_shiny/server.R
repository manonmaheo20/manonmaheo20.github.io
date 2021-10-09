######## CHARGEMENT DES PACKAGES ########

library(shiny)
library(tidyverse)
library(leaflet)
library(sf)
library(rAmCharts)
library(here)
library(plotly)
library(rsconnect)
library(highcharter)
library(dygraphs)
library(plotly)
library(rnaturalearthdata)
library(rgeos)
library(DT)

######## PARTIE SERVER ########

shinyServer(function(input, output) {
    
    #Carte des évolutions de températures à l'échelle du globe
    output$texte <- renderLeaflet({ 
      
      temp3<-temp2[temp2$...5==input$idSlider2 & temp2$Statistics==input$idSelect ,]
      b <- leaflet() %>% addProviderTiles(providers$CartoDB.Positron) %>%
        
        addPolygons(data = temp3,color=~pal(temp3$Monthly.Temperature....Celsius.),fillOpacity = 0.6, 
                    stroke = TRUE,weight=1,
                    popup=~paste(as.character(Country),paste(as.character(round(Monthly.Temperature....Celsius.)),"°C"),sep=" : "),highlightOptions = highlightOptions(color="white",weight = 2)) %>% 
        addLayersControl(options=layersControlOptions(collapsed = FALSE))  %>%
        addLegend(
          title = "Température mensuelle",
          pal = pal, values = temp3$Monthly.Temperature....Celsius.,labFormat = labelFormat(suffix = "°"),opacity = 1) %>%
        addEasyButton(
          button = easyButton(
            icon = "fa-globe",
            title = "Zoom initial",
            onClick = JS("function(btn, map){ map.setZoom(1); }") 
          ))
      b
      

      })
     
      #Histogramme du menu
      output$temp2<-renderPlot({
        temp3<-temp2[temp2$...5==input$idSlider2 & temp2$Statistics==input$idSelect ,]
        ggplot(temp3, aes(x=Monthly.Temperature....Celsius.)) + geom_histogram( fill="lightblue")+geom_vline(aes(xintercept=mean(Monthly.Temperature....Celsius.)),
                                                                                                             color="blue", linetype="dashed", size=1)+xlab("Température en degré")+ylab("Nombre de pays")
      })
      
      #Titre du menu
      output$titre <- renderText({
          paste("Distribution de températures pour l'année",input$idSlider2,"et pour le mois de",input$idSelect)
      })
      
      #Texte du menu
      output$moy_annee <- renderText({
        temp3<-temp2[temp2$...5==input$idSlider2,]
        paste("Température annuelle moyenne pour l'année",input$idSlider2,":",round(mean(temp3$Monthly.Temperature....Celsius.),2),"°C")
      })
      
      #Tableaux de nos données
      output$dataTable1 <- renderDataTable({
        temp3 
      })
      
      output$dataTable2 <- renderDataTable({
        anomalies
      })
      
      output$dataTable2_2 <- renderDataTable({
        indice
      })
      
      output$dataTable2_3 <- renderDataTable({
        secteur
      })
      
      output$dataTable3 <- renderDataTable({
        bd
      })
      
      #Carte pour la France
      output$france <- renderLeaflet({
        bd <- bd %>% gather(key = cle, value = variable, -annee, -geometry, -code_insee_)
        bd$annee <- as.numeric(bd$annee)
        bd2<-bd[bd$annee==input$nouveau & bd$cle==input$var2, ]
        bd2 <- st_transform(bd2, crs = 4326)
        pal2 <- colorNumeric(scales::seq_gradient_pal(low = "#d8f3dc", high = "#2d6a4f",
                                                      space = "Lab"), domain = bd2$variable)
        
        m <- leaflet() %>% addTiles() %>% 
          addPolygons(data = bd2,color=~pal2(variable),fillOpacity = 0.6, 
                      stroke = TRUE,weight=1,
                      popup=~paste("Code INSEE",as.character(code_insee_),as.character(variable),sep=" : ")) %>% 
          addLayersControl(options=layersControlOptions(collapsed = FALSE)) %>%
          addLegend(
            title = "Production énergies renouvelables",
            pal = pal2, values = bd2$variable,labFormat = labelFormat(suffix = "°"),opacity = 1)
        m
      })
      
      #Indice d'émission de gaz à effet de serres, les quatre graphiques : 
      
      output$indice <-renderAmCharts({
        input$update 
        isolate({
        col <- indice %>% arrange(desc(input$var)) %>% select(PAYS, input$var) %>% head(5)
        colnames(col) <- c("label","value")
        amPie(data = col, main = paste("Les cinq pays émettant le plus de gaz à effet de serre en ", input$var, "en millions de tonnes"),
              mainColor = "#757575", mainSize = 15, creditsPosition = "bottom-right",
              inner_radius = 50, export=TRUE)})
      })
      
      output$indice_2 <-renderAmCharts({
        input$update 
        isolate({
        col2 <- indice %>% filter(PAYS == input$indice1) %>% select(PAYS,`2018`) 
        
        
        min <- min(indice$`2018`)
        max <- max(indice$`2018`)
        amBullet(value = col2$`2018`, min = min, max = max, steps = FALSE) %>% amOptions( main = paste("Evaluation de l'émission de gaz à effet de serre de",input$indice1, "en 2018*"),
                                                                                           mainColor = "#757575", 
                                                                                           mainSize = 15, creditsPosition = "bottom-right",export=TRUE)})
      })
      
      output$indice_3<-renderHighchart({
        input$update 
        isolate({
        evolution <- indice %>% filter (PAYS == input$indice1)
        evolution <- evolution %>% gather(key = variable, value = valeur, -PAYS)
        evolution$variable <- as.Date(evolution$variable, "%Y")
        
        hc <- evolution %>%
          hchart(
            "line", 
            hcaes(x = variable, y = valeur)) %>%
          hc_title(text = paste("Evolution de l'indice de gaz à effet de serre de", input$indice1)) %>%
          hc_xAxis(title = list(text= "Années")) %>%
          hc_yAxis(title = list(text = "Emission de gaz à effet de serre"))
        hc})
      })
      
      output$indice_4<-renderHighchart({
        input$update 
        isolate({
        evolution2 <- indice
        evolution2 <- evolution2 %>% gather(key = variable, value = valeur, -PAYS)
        evolution2 <- evolution2 %>% filter(PAYS==input$indice1 | PAYS==input$indice3)
        
        hc2 <- evolution2 %>%
          hchart("line", hcaes(x = variable, y = valeur, group = PAYS)) %>%
          hc_title(text = paste("Comparaison de ", input$indice1, "et de ", input$indice3, "en termes d'émission de GES")) %>%
          hc_xAxis(title = list(text= "Années")) %>%
          hc_yAxis(title = list(text = "Emission de gaz à effet de serre"))
        hc2})
      })
 
      #Anomalies de températures
      output$indice2_1<-renderPlotly({
       ggplot(anomalies, aes(x = date, y = 1, fill = Value))+ geom_tile()+ scale_x_date(date_breaks = "6 years", date_labels = "%Y",expand = c(0, 0))+ scale_y_continuous(expand = c(0, 0))+ scale_fill_gradientn(colors = rev(col_strip))+ guides(fill = guide_colorbar(barwidth = 1))+ labs(title = "Températures moyennes Europe 1910-2020",caption = "Anomalie température moyenne à la surface de la terre")+theme_strip
       })
      
      output$indice2_2<-renderDygraph({
        dygraph(anomalies, main = "Anomalies de températures", xlab = "Années", ylab = "Anomalies de températures") %>% 
          dyOptions(stackedGraph = TRUE) %>% dyRangeSelector(height = 20)
      })
      
      #GES par secteur d'activité
      output$indice3_1<-renderHighchart({
        empil <- secteur %>% hchart('column', hcaes(x = 'variable', y = 'valeur', group = 'Secteur'), stacking = "normal") %>% hc_title(text = "Émissions de gaz à effet de serre par activité") %>%
          hc_xAxis(title = list(text= "Années")) %>%
          hc_yAxis(title = list(text = "Secteur"))
        empil
      })
      
     #Classification
      output$classi<-renderPlot({
        bd_classi<-bd_name[bd_name$annee==input$idSlider5,]
      
        bd_classi<-as.data.frame(bd_classi[,3:9],row.names=bd_classi[,2])
       
        d        = dist(bd_classi)
        cah.ward = hclust(d,method="ward.D")
        plot(cah.ward,hang=-1,xlab="Numéro INSEE région",ylab="Distance")
       
        rect.hclust(cah.ward, input$choix_8, border ="blue")
        
      })
      
      
      #Graphique des productions énergies renouvelables
      
      output$graph_regions <- renderAmCharts({
        bd_name$production_hydraulique_renouvelable <- as.numeric(bd_name$production_hydraulique_renouvelable)
        bd_name$production_bioenergies_renouvelable <- as.numeric(bd_name$production_bioenergies_renouvelable)
        bd_name$production_eolienne_renouvelable <- as.numeric(bd_name$production_eolienne_renouvelable)
        bd_name$production_electrique_renouvelable <- as.numeric(bd_name$production_electrique_renouvelable)
        bd_name$production_solaire_renouvelable <- as.numeric(bd_name$production_solaire_renouvelable)
        bd_name$annee <- as.character(bd_name$annee)
        bd_name$code_insee_region <- as.character(bd_name$code_insee_region)
        bd_name <- filter(bd_name, annee == as.character(input$annee_region), code_insee_region == input$region)
        r <- amBarplot(x = "code_insee_region", y = 
                    c("production_hydraulique_renouvelable", "production_bioenergies_renouvelable",
                      "production_eolienne_renouvelable","production_eolienne_renouvelable","production_electrique_renouvelable"), data = bd_name)%>% setChartCursor()
        r
      })
})


