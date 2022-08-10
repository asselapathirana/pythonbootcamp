""""
 Copyright (c) 2021 Assela Pathirana
This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""
import pandas as pd
from matplotlib import pyplot as plt

rdf = pd.read_csv('Data/funabashi_rainfall.txt', sep='\t', 
                  names=['date', 'rainfall'], header=None)

rdf['DateTime'] = pd.to_datetime(rdf['date'])

# Convert to time series:
rbs = pd.Series(data=rdf["rainfall"].values, index=rdf["DateTime"])

# resample to annual totals 
ras = rbs.resample("A").sum()
ras.plot()
plt.show()