"""
    ===============================================
    A bit advanced example of plotting data with seaborn
    We use the country_profile_variables.csv dataset downloaded from
    https://www.kaggle.com/sudalairajkumar/undata-country-profiles
    
    Its a messy dataset. We use pandas to do some processing to get data straightened up
    ===============================================
   
   .. Copyright 2019 Assela Pathirana

    .. This program is free software: you can redistribute it and/or modify
       it under the terms of the GNU General Public License as published by
       the Free Software Foundation, either version 3 of the License, or
       (at your option) any later version.

    .. This program is distributed in the hope that it will be useful,
       but WITHOUT ANY WARRANTY; without even the implied warranty of
       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
       GNU General Public License for more details.

    .. You should have received a copy of the GNU General Public License
       along with this program.  If not, see <http://www.gnu.org/licenses/>.
       
    .. author:: Assela Pathirana <assela@pathirana.net>
"""

# first import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#
sns.set(
    style="darkgrid"
)  # you can have five basic styles: darkgrid, whitegrid, dark, white, and ticks

# our data is messy.
# we need to reat all the following symbols/values as missing data
missing_values = ["n/a", "-99", "...", ".../..."]

# now read data
countries = pd.read_csv(
    "./data/country_profile_variables.csv", na_values=missing_values
)
# The column names of this dataset is really long.
# So we assin them to variables so that our code can be shorter
GDP = "GDP per capita (current US$)"
IMR = "Infant mortality rate (per 1000 live births"
LEX_ = "Life expectancy at birth (females/males, years)"
HTE = "Health: Total expenditure (% of GDP)"


# LEX is of the pattern x/y split the two and make a new column
LEX = "Life expectancy at birth (years)"
# first get rid rows with  'missing' values in LEX_ column - otherwise they can create problems below
countries.dropna(subset=[LEX_], inplace=True)
# create a temporary series 'temp' by splitting LEX_ at / (55/57 will become [55, 57])
temp = countries[LEX_].str.split("/", n=1, expand=True)
# assing mean value of these two series to LEX
countries[LEX] = (temp[0].astype(float) + temp[1].astype(float)) / 2.0


# we are going to use HTE='Health: Total expenditure (% of GDP)' as a color in the plot.
# so we convert it from a continious variable to a discrete variable with NBINS quantiles
# pandas has the function qcut for this. 
NBINS = 7
countries[HTE] = pd.qcut(countries[HTE], NBINS)

# now we are ready to plot.

# first plot a regression line (linear-log type) to the data.
# in this case we do not plot the points - you'll know why later.
graph = sns.regplot(
    x=GDP, # GDP as x value
    y=LEX, # LEX as y value
    data=countries, # pabdas dataframe to be used as input
    scatter_kws=dict(alpha=0),  # do not plot  points - make them invisible!
    logx=True, # regression line calculation should be done for y~log(x), not for y~x!
)
# ^^ notice we assinged the return value ('axis') to the variables 'graph'
# we use this value in the next plotting operation to indicate that we want to plot on the same axis


# now plot the points, using an extra variable IMR to be represented by the size of each point
# Also use color to indicate HTE
sns.scatterplot(
    x=GDP,
    y=LEX,
    size=IMR,
    hue=HTE,
    palette=sns.color_palette(
        "RdBu", n_colors=NBINS
    ),  # we use a nicer color palette rather than the default.
    data=countries,
    ax=graph,  # here we tell the scatterplot to use the same axis as above
)

graph.set(xscale="log")  # make x axis log scale

# now we want to label some countries in the plot (not all - as it will make a very messy graph!)
# following are the countries we want to label
label_countries = [
    "Cuba",
    "United States of America",
    "Sri Lanka",
    "Netherlands",
    "Saudi Arabia",
    "Burundi",
    "Japan",
    "Malawi",
]

# create a new dataframe containing only those
countries_text = countries[countries["country"].isin(label_countries)]

# go through each row in countries_text
for line in countries_text.index:
    # make a label for each row
    graph.text(
        countries_text[GDP][line] + 0.2,
        countries_text[LEX][line],
        countries_text["country"][line],
        horizontalalignment="left",
        size="medium",
    )

# finally show the graph
plt.show()
