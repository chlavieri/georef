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

br1872.plot(color = "white", edgecolor = "grey", figsize = (18,10))
