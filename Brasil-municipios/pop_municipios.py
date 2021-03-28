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

## Plotagem

mpl.style.use("seaborn")
fig, ax = plt.subplots(1, 1)

sch = mapclassify.BoxPlot(brpop["denspop"], hinge = 1.5)


geoplot.choropleth(brpop, hue = pop,
                   cmap = "Dark2", scheme = scheme)


brpop.plot(column = "denspop", cmap = "Reds", scheme = "Quantiles",
           classification_kwds = {"k" : 8})
