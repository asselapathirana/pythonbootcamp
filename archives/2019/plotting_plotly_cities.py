import os
import numpy as np
import pandas as pd
import plotly.express as px

data  = './data/worldcities.zip'
datap = data+'.pickle'
if not os.path.isfile(datap):
    # download the file
    data=pd.read_csv(data, sep=',', compression='zip')
    data.to_pickle(datap, compression='zip')
else:
    data=pd.read_pickle(datap, compression='zip')
    
datafilt=data[data['population']>0] # all cities with population data
#datafilt['logpopulation']=np.log(datafilt['population'])
fig = px.scatter_geo(datafilt, lat='lat', lon='lng',
                     size="population", # size of markers, 
                     hover_name='city',
                     hover_data=['population'],
                     size_max=50,
                     color = 'population',
                     projection='robinson',
                     )

fig.show()

