dfVitHom$longitude_1 <- as.numeric(dfVitHom$longitude_1)
dfVitHom$latitude_1 <- as.numeric(dfVitHom$latitude_1)
library(stringi)
library(stringr)
library(tidyverse)
dfVitHom$latitude_1 <- as.character(dfVitHom$latitude_1)
dfVitHom$longitude_1 <- as.character(dfVitHom$longitude_1)

dfVitHom$latitude_1 <- gsub("\\.", "", dfVitHom$latitude_1)
dfVitHom$longitude_1 <- sub("\\.","", dfVitHom$longitude_1)

stri_sub(dfVitHom$latitude_1, nchar(dfVitHom$latitude_1)-5, 2) <- "."
stri_sub(dfVitHom$longitude_1, nchar(dfVitHom$longitude_1)-5, 2) <- "."

dfVitHom$latitude_1 <- as.numeric(dfVitHom$latitude_1)
dfVitHom$longitude_1 <- as.numeric(dfVitHom$longitude_1)

dfVitHom <- dfVitHom %>% filter(!is.na(dfVitHom$latitude_1))

for (i in dfVitHom$latitude_1){
  if(i > -10){
    dfVitHom$latitude_1[dfVitHom$latitude_1 == i] <- i*10
    
  }
}

for (i in dfVitHom$longitude_1){
  if(i > -10){
    dfVitHom$longitude_1[dfVitHom$longitude_1 == i] <- i*10
    
  }
}



dfVitHom %>% select(latitude_1, longitude_1) %>% View()

dfVitHom <- dfVitHom %>% filter(latitude_1 < -20)
dfVitHom <- dfVitHom %>% filter(latitude_1 > -50)
dfVitHom <- dfVitHom %>% filter(longitude_1 < -10)

write.csv(dfVitHom, "C:\\Users\\chlav\\Google Drive\\Python scripts\\SP\\dfVitimasHomicidio.csv")
