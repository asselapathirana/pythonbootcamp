import pandas as pd
from pandas import datetime
from matplotlib import pyplot

def parser(x):
	return datetime.strptime(x+' 10:00', '%m/%d/%Y %H:%M') # water levels are measured in the daytime. Due to lack of information, let's assume 10:00
series = pd.read_csv('data/flow_ups.txt', header=None, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser, sep='\t')
upsampled = series.resample('H')
interpolated = upsampled.interpolate(method='spline', order=2)
print(interpolated.head(32))
interpolated.plot()
#pyplot.show()

# 
def parser2(x):
	return datetime.strptime(x, '%m/%d/%Y %H:%M') # water levels are measured in the daytime. Due to lack of information, let's assume 10:00
dsl=pd.read_csv("./data/sea_level.txt", parse_dates=[[0,1]], sep='\t', header=None).set_index('0_1')
rlv=pd.read_csv("./data/river_level.txt", parse_dates=[[0,1]], sep='\t', header=None).set_index('0_1')
res=interpolated.merge(dsl, left_index=True, right_index=True).merge(rlv, left_index=True, right_index=True)
res=res.drop([1], axis=1)
res=res.rename(columns={"2_x": "FL", "2_y": "SL" ,2: "RL"})
res.to_csv("data.csv")