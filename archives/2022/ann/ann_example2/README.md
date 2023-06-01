# Prototype code for river water level prediction using LSTM
There are three datasets: 
* Upstream flow
* Sea level downstream 
* river level observed

All measured during the same time period (3 years), once every one hour. 

`prepare_data.py`: Run to prepare the input data in the single file `data.csv` with the above datasets. 

`keras-timeseries-multi-fit.ipynb`: Fits the data to a LSTM model. 

`keras-timeseries-test.ipynb`: Tests the performance of the fitted model. 

`model_good.keras`: Saved model with a good fit. 
`model_good.keras`: Saved parameters (just the mean and standard deviation of the input data). 

