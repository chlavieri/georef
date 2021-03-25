# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import geobr
import os
import geopandas as gpd
import geoplot
import pandas as pd
import matplotlib.pyplot as plt

br1872 = geobr.read_country(year = 1872)

br1872.plot(color = "yellow", edgecolor = "blue", figsize = (18,10))

br2019 = geobr.read_country(year = 2019)
br2019.plot(color = "yellow", edgecolor = "blue", figsize = (18,10))
