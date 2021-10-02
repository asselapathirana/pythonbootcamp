import pandas as pd
import plotly.express as px

countries = pd.read_pickle("./data/country_profile_variables.csv.pickle")

# So we assin them to variables so that our code can be shorter
GDP = "GDP per capita (current US$)"
IMR = "Infant mortality rate (per 1000 live births"
LEX = "Life expectancy at birth (years)"
HTE = "Health: Total expenditure (% of GDP)"
countries2=countries.dropna(subset=[GDP, IMR, LEX, HTE]) # get rid of rows with missing data in our interested columns
fig = px.scatter(
    countries2,
    x=GDP,
    y=LEX,
    color=HTE,
    size=IMR,
    hover_name="country", #
    marginal_x='box',
    marginal_y='histogram',
)
fig.update_xaxes(type="log")
fig.show()

fig2= px.scatter_geo(countries2, locations="country", 
                     locationmode="country names", 
                     color=HTE,
                     hover_name="country", size=IMR,
                     projection='winkel tripel')
fig2.show()
