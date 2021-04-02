#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 22:03:16 2021

@author: chlav
"""

## Chama os pacotes

import geobr
import os
import geopandas as gpd
import geoplot
import cartopy.crs as ccrs
import pandas as pd
import numpy as np
import mapclassify
import matplotlib.pyplot as plt
import matplotlib as mpl
import re


## Le as bases de shapefile dos municipios e de populacao
br = geobr.read_municipality(code_muni="all", year=2019)

pop = pd.read_excel("Brasil-municipios/Data/estimativa_dou_2020.xls",
                        dtype = {"COD. MUNIC" : str,
                                 "POPULAÇÃO ESTIMADA" : str})

## Arruma a base de pop e junta com a dos municipios
pop2 = pop.dropna()

pop2["POPULAÇÃO ESTIMADA"] = [int(re.sub("\(.*\)", "",
                            i)) for i in list(pop2["POPULAÇÃO ESTIMADA"])]

pop3 = pop2.rename(columns = {"COD. UF" : "code_state",
                    "NOME DO MUNICÍPIO" : "name_muni", "UF" : "abbrev_state"})

#### Ver diferencas dos nomes dos municipios nas bases

dif1 = np.setdiff1d(pop3["name_muni"], br["name_muni"])

dif2 = np.setdiff1d(br["name_muni"],pop3["name_muni"])

#### Arruma

pop3["name_muni"] = [i.upper() for i in pop3["name_muni"]]
br["name_muni"] = [i.upper() for i in br["name_muni"]]

pop3.where(pop3.name_muni =="AMPARO DE SÃO FRANCISCO").dropna()
pop3.iloc[1752, 3] = "AMPARO DO SÃO FRANCISCO"

pop3.where(pop3.name_muni =="ATILIO VIVACQUA").dropna()
pop3.iloc[3106, 3] = "ATÍLIO VIVACQUA"

pop3.where(pop3.name_muni =="OLHO-D'ÁGUA DO BORGES").dropna()
pop3.iloc[1166, 3] = "OLHO D'ÁGUA DO BORGES"

pop3.where(pop3.name_muni =="PINGO-D'ÁGUA").dropna()
pop3.iloc[2834, 3] = "PINGO D'ÁGUA"

#### Junta

brpop = pd.merge(br, pop3, how = "inner")

brpop = brpop.rename(columns = {"POPULAÇÃO ESTIMADA" : "pop"})

brpop["area"] = brpop['geometry'].to_crs({'init': 'epsg:3395'})\
               .map(lambda p: p.area / 10**6)

brpop["denspop"] = brpop["pop"] / brpop["area"]

## Plotagem 1

mpl.style.use("seaborn")
fig, ax = plt.subplots(1, 1)

sch = mapclassify.BoxPlot(brpop["denspop"], hinge = 1.5)


brpop.plot(column = "denspop", cmap = "Reds", scheme = "Quantiles",
           classification_kwds = {"k" : 8})

## Plotagem 2

crs = ccrs.Orthographic(central_latitude = -10, central_longitude = 0)

fig, ax = plt.subplots(subplot_kw={'projection': crs})

crs_proj4 = crs.proj4_init
brpop_ae = brpop.to_crs(crs_proj4)

brpop_ae.plot(column = "denspop", cmap = "Reds", scheme = "Quantiles",
           classification_kwds = {"k" : 8})


## Pegando data frame de renda

renda = pd.read_excel("Brasil-municipios/Data/renda_municipios.xlsx")

renda["Municípios"] = [str(x) for x in list(renda["Municípios"])]
renda["Municípios"] = [re.sub(" -.*", "", x) for x in list(renda["Municípios"])]
renda["Municípios"] = [x.upper() for x in renda["Municípios"]]





renda.columns = ["name_state", "name_muni", "n_unid_local", "pessoal_ocup_t",
                 "pessoal_ocup_assal", "pessoal_assal_med",
                 "salario_total", "salario_medio_sal_min",
                 "salario_med_mensal", "n_empresas"]

renda = renda.iloc[1:,:]


dif3 = np.setdiff1d(brpop["name_muni"], renda["name_muni"])

dif4 = np.setdiff1d(renda["name_muni"],brpop["name_muni"])

renda.where(renda.name_muni == "AMPARO DE SÃO FRANCISCO").dropna()
renda.iloc[1753, 2] = "AMPARO DO SÃO FRANCISCO"

renda.where(renda.name_muni == "ARAÇAS").dropna()
renda.iloc[1852, 2] = "ARAÇÁS"

renda.where(renda.name_muni == "ATILIO VIVACQUA").dropna()
renda.iloc[3107, 2] = "ATÍLIO VIVACQUA"

renda.where(renda.name_muni == "BIRITIBA-MIRIM").dropna()
renda.iloc[3342, 2] = "BIRITIBA MIRIM"

renda.where(renda.name_muni == "DONA EUSÉBIA").dropna()
renda.iloc[2500, 2] = "DONA EUZÉBIA"

renda.where(renda.name_muni == "ELDORADO DOS CARAJÁS").dropna()
renda.iloc[198, 2] = "ELDORADO DO CARAJÁS"

renda.where(renda.name_muni == "ERERÊ").dropna()
renda.iloc[946, 2] = "ERERÉ"

renda.where(renda.name_muni == "FLORÍNIA").dropna()
renda.iloc[3452, 2] = "FLORÍNEA"

renda.where(renda.name_muni == "FORTALEZA DO TABOCÃO").dropna()
renda.iloc[365, 2] = "TABOCÃO"

renda.where(renda.name_muni == "IGUARACI").dropna()
renda.iloc[1541, 2] = "IGUARACY"

renda.where(renda.name_muni == "IGUARACI").dropna()
renda.iloc[1541, 2] = "IGUARACY"




######

brpop_renda = pd.merge(brpop,renda, how = "inner")

brpop_renda = brpop_renda.drop_duplicates()




