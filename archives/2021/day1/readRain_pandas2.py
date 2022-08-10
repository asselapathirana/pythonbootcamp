# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:58:50 2021

@author: apa
"""

import pandas as pd

rdf = pd.read_csv("./data/funabashi_rainfall.txt", delimiter="\t",
                  names=["date", "rainfall"],
                  header=0,
                  parse_dates=[0], index_col=0)

rts=rdf.squeeze()
rts.plot() 
rts_y=rts.resample("Y").sum()
rts_y.plot()