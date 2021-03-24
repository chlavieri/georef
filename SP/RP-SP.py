# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 18:20:06 2021

@author: chlav
"""

import os
import geopandas as gpd
import geoplot
import pandas as pd
import matplotlib.pyplot as plt

sp = gpd.read_file("SP_Municipios_2019.shp")

rp = sp[sp.NM_MUN == "Ribeirão Preto"]

df = pd.read_csv("dfVitimasHomicidio.csv")

df2 = df[["nome_vitima", "ano", "latitude_1", "longitude_1"]]
df2.latitude_1 = df2.latitude_1.astype(float)
df2.longitude_1 = df2.longitude_1.astype(float)

df2 = df2[df2.longitude_1 < -47]


gdf = gpd.GeoDataFrame(df2, geometry=gpd.points_from_xy(df2.longitude_1, df2.latitude_1))

rp.plot(color = "white", edgecolor = "grey", figsize = (18,10))
plt.scatter(df2.longitude_1, df2.latitude_1, s = 3, color = "red")
