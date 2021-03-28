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


brpop = pd.merge(br, pop3, on = "name_muni", how = "inner")

## Plotagem

mpl.style.use("seaborn")
fig, ax = plt.subplots(1, 1)


brpop.plot(column = "POPULAÇÃO ESTIMADA", cmap = "Dark2")
