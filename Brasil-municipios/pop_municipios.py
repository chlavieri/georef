#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 22:03:16 2021

@author: chlav
"""

import geobr
import os
import geopandas as gpd
import geoplot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

br = geobr.read_country(year = 2019)

pop2020 = pd.read_excel("Brasil-municipios/Data/estimativa_dou_2020.xls",
                        dtype = {"COD. MUNIC" : str})
