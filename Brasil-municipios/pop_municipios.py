#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 22:03:16 2021

@author: chlav
"""

#%%
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

#%%
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

#%%
## Plotagem 1

mpl.style.use("seaborn")
fig, ax = plt.subplots(1, 1)

sch = mapclassify.BoxPlot(brpop["denspop"], hinge = 1.5)


brpop.plot(column = "denspop", cmap = "Reds", scheme = "Quantiles",
           classification_kwds = {"k" : 8})
#%%
## Plotagem 2

crs = ccrs.Orthographic(central_latitude = -10, central_longitude = 0)

fig, ax = plt.subplots(subplot_kw={'projection': crs})

crs_proj4 = crs.proj4_init
brpop_ae = brpop.to_crs(crs_proj4)

brpop_ae.plot(column = "denspop", cmap = "Reds", scheme = "Quantiles",
           classification_kwds = {"k" : 8})

#%%
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
renda.iloc[1753-1, 1] = "AMPARO DO SÃO FRANCISCO"

renda.where(renda.name_muni == "ARAÇAS").dropna()
renda.iloc[1852-1, 1] = "ARAÇÁS"

renda.where(renda.name_muni == "ATILIO VIVACQUA").dropna()
renda.iloc[3107-1, 1] = "ATÍLIO VIVACQUA"

renda.where(renda.name_muni == "BIRITIBA-MIRIM").dropna()
renda.iloc[3342-1, 1] = "BIRITIBA MIRIM"

renda.where(renda.name_muni == "DONA EUSÉBIA").dropna()
renda.iloc[2500-1, 1] = "DONA EUZÉBIA"

renda.where(renda.name_muni == "ELDORADO DOS CARAJÁS").dropna()
renda.iloc[198-1, 1] = "ELDORADO DO CARAJÁS"

renda.where(renda.name_muni == "ERERÊ").dropna()
renda.iloc[946-1, 1] = "ERERÉ"

renda.where(renda.name_muni == "FLORÍNIA").dropna()
renda.iloc[3452-1, 1] = "FLORÍNEA"

renda.where(renda.name_muni == "FORTALEZA DO TABOCÃO").dropna()
renda.iloc[365-1, 1] = "TABOCÃO"

renda.where(renda.name_muni == "IGUARACI").dropna()
renda.iloc[1541-1, 1] = "IGUARACY"

renda.where(renda.name_muni == "ITAPAGÉ").dropna()
renda.iloc[978-1, 1] = "ITAPAJÉ"

renda.where(renda.name_muni == "ITAÓCA").dropna()
renda.iloc[3521-1, 1] = "ITAOCA"

renda.where(renda.name_muni == "IUIÚ").dropna()
renda.iloc[2032-1, 1] = "IUIU"

renda.where(renda.name_muni == "LAURO MULLER").dropna()
renda.iloc[4456-1, 1] = "LAURO MÜLLER"

renda.where(renda.name_muni == "MOJI MIRIM").dropna()
renda.iloc[3613-1, 1] = "MOGI MIRIM"

renda.where(renda.name_muni == "MUQUÉM DE SÃO FRANCISCO").dropna()
renda.iloc[2096-1, 1] = "MUQUÉM DO SÃO FRANCISCO"

renda.where(renda.name_muni == "OLHO-D'ÁGUA DO BORGES").dropna()
renda.iloc[1167-1, 1] = "OLHO D'ÁGUA DO BORGES"

renda.where(renda.name_muni == "PASSA-VINTE").dropna()
renda.iloc[2802-1, 1] = "PASSA VINTE"

renda.where(renda.name_muni == "PINGO-D'ÁGUA").dropna()
renda.iloc[2835-1, 1] = "PINGO D'ÁGUA"

renda.where(renda.name_muni == "POXORÉO").dropna()
renda.iloc[5281-1, 1] = "POXORÉU"

renda.where(renda.name_muni == "RESTINGA SECA").dropna()
renda.iloc[4948-1, 1] = "RESTINGA SÊCA"

renda.where(renda.name_muni == "SANTA ISABEL DO PARÁ").dropna()
renda.iloc[260-1, 1] = "SANTA IZABEL DO PARÁ"

renda.where(renda.name_muni == "SÃO CRISTOVÃO DO SUL").dropna()
renda.iloc[4552-1, 1] = "SÃO CRISTÓVÃO DO SUL"

renda.where(renda.name_muni == "SÃO LUÍS DO PARAITINGA").dropna()
renda.iloc[3827-1, 1] = "SÃO LUIZ DO PARAITINGA"

renda.where(renda.name_muni == "SÃO LUÍZ DO NORTE").dropna()
renda.iloc[5542-1, 1] = "SÃO LUIZ DO NORTE"

renda.where(renda.name_muni == "SÃO THOMÉ DAS LETRAS").dropna()
renda.iloc[3009-1, 1] = "SÃO TOMÉ DAS LETRAS"

renda.where(renda.name_muni == "VESPASIANO CORREA").dropna()
renda.iloc[5089-1, 1] = "VESPASIANO CORRÊA"

renda.where(renda.name_muni == "WESTFALIA").dropna()
renda.iloc[5102-1, 1] = "WESTFÁLIA"


######

brpop_renda = pd.merge(brpop,renda, how = "inner")


######

# Plotagem 3

mpl.style.use("fivethirtyeight")



fig, ax = plt.subplots(1, 1)

sch = mapclassify.BoxPlot(brpop_renda["denspop"], hinge = 1.5)

brpop_renda.plot(column = "salario_med_mensal",
                 scheme = "Quantiles",
           classification_kwds = {"k" : 5})







