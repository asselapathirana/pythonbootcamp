"""
    ===============================================
    How to analyse a large (> 0.5 millon records and about 20 columns)
    meteorological dataset with pandas
    
    The data file is > 80 MB. So, it is stored online: 
    https://github.com/asselapathirana/pythonbootcamp/releases/download/NA/KNMI_20190815_hourly.zip
    as a zip file. 
    
    We use python to download the data file. 
    ===============================================
    The data file looks like the following
# BRON: KONINKLIJK NEDERLANDS METEOROLOGISCH INSTITUUT (KNMI)
# Opmerking: door stationsverplaatsingen en veranderingen in waarneemmethodieken zijn deze tijdreeksen van uurwaarden mogelijk inhomogeen! Dat betekent dat deze reeks van gemeten waarden niet geschikt is voor trendanalyse. Voor studies naar klimaatverandering verwijzen we naar de gehomogeniseerde reeks maandtemperaturen van De Bilt <http://www.knmi.nl/klimatologie/onderzoeksgegevens/homogeen_260/index.html> of de Centraal Nederland Temperatuur <http://www.knmi.nl/klimatologie/onderzoeksgegevens/CNT/>.
# 
# 
# STN      LON(east)   LAT(north)     ALT(m)  NAME
# 260:         5.180       52.100       1.90  DE BILT
# 
# YYYYMMDD = datum (YYYY=jaar,MM=maand,DD=dag); 
# HH       = tijd (HH=uur, UT.12 UT=13 MET, 14 MEZT. Uurvak 05 loopt van 04.00 UT tot 5.00 UT; 
# DD       = Windrichting (in graden) gemiddeld over de laatste 10 minuten van het afgelopen uur (360=noord, 90=oost, 180=zuid, 270=west, 0=windstil 990=veranderlijk. Zie http://www.knmi.nl/kennis-en-datacentrum/achtergrond/klimatologische-brochures-en-boeken; 
# FH       = Uurgemiddelde windsnelheid (in 0.1 m/s). Zie http://www.knmi.nl/kennis-en-datacentrum/achtergrond/klimatologische-brochures-en-boeken; 
# FF       = Windsnelheid (in 0.1 m/s) gemiddeld over de laatste 10 minuten van het afgelopen uur; 
# FX       = Hoogste windstoot (in 0.1 m/s) over het afgelopen uurvak; 
# T        = Temperatuur (in 0.1 graden Celsius) op 1.50 m hoogte tijdens de waarneming; 
# T10N     = Minimumtemperatuur (in 0.1 graden Celsius) op 10 cm hoogte in de afgelopen 6 uur; 
# TD       = Dauwpuntstemperatuur (in 0.1 graden Celsius) op 1.50 m hoogte tijdens de waarneming; 
# SQ       = Duur van de zonneschijn (in 0.1 uren) per uurvak, berekend uit globale straling  (-1 for <0.05 uur); 
# Q        = Globale straling (in J/cm2) per uurvak; 
# DR       = Duur van de neerslag (in 0.1 uur) per uurvak; 
# RH       = Uursom van de neerslag (in 0.1 mm) (-1 voor <0.05 mm); 
# P        = Luchtdruk (in 0.1 hPa) herleid naar zeeniveau, tijdens de waarneming; 
# VV       = Horizontaal zicht tijdens de waarneming (0=minder dan 100m, 1=100-200m, 2=200-300m,..., 49=4900-5000m, 50=5-6km, 56=6-7km, 57=7-8km, ..., 79=29-30km, 80=30-35km, 81=35-40km,..., 89=meer dan 70km); 
# N        = Bewolking (bedekkingsgraad van de bovenlucht in achtsten), tijdens de waarneming (9=bovenlucht onzichtbaar); 
# U        = Relatieve vochtigheid (in procenten) op 1.50 m hoogte tijdens de waarneming; 
# WW       = Weercode (00-99), visueel(WW) of automatisch(WaWa) waargenomen, voor het actuele weer of het weer in het afgelopen uur. Zie http://bibliotheek.knmi.nl/scholierenpdf/weercodes_Nederland; 
# IX       = Weercode indicator voor de wijze van waarnemen op een bemand of automatisch station (1=bemand gebruikmakend van code uit visuele waarnemingen, 2,3=bemand en weggelaten (geen belangrijk weersverschijnsel, geen gegevens), 4=automatisch en opgenomen (gebruikmakend van code uit visuele waarnemingen), 5,6=automatisch en weggelaten (geen belangrijk weersverschijnsel, geen gegevens), 7=automatisch gebruikmakend van code uit automatische waarnemingen); 
# M        = Mist 0=niet voorgekomen, 1=wel voorgekomen in het voorgaande uur en/of tijdens de waarneming; 
# R        = Regen 0=niet voorgekomen, 1=wel voorgekomen in het voorgaande uur en/of tijdens de waarneming; 
# S        = Sneeuw 0=niet voorgekomen, 1=wel voorgekomen in het voorgaande uur en/of tijdens de waarneming; 
# O        = Onweer 0=niet voorgekomen, 1=wel voorgekomen in het voorgaande uur en/of tijdens de waarneming; 
# Y        = IJsvorming 0=niet voorgekomen, 1=wel voorgekomen in het voorgaande uur en/of tijdens de waarneming; 
# 
# STN,YYYYMMDD,   HH,   DD,   FH,   FF,   FX,    T,  T10,   TD,   SQ,    Q,   DR,   RH,    P,   VV,    N,    U,   WW,   IX,    M,    R,    S,    O,    Y
# 
  260,19510801,    1,  180,   26,   10,   21,  182,     ,  174,     ,     ,    0,    0,10126,     ,    8,   95,   29,     ,    0,    1,    0,    1,    0
  260,19510801,    2,  160,   26,   26,   36,  182,     ,  176,     ,     ,    0,    0,10132,     ,    8,   96,    2,     ,    0,    0,    0,    0,    0
  260,19510801,    3,  180,   31,   21,   41,  182,     ,  176,     ,     ,    0,    0,10131,     ,    7,   96,    1,     ,    0,    0,    0,    0,    0
  260,19510801,    4,  270,   36,   31,   46,  187,     ,  177,     ,     ,    0,    0,10137,     ,    8,   94,   95,     ,    0,    1,    0,    1,    0
   
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

import os
import wget
import pandas as pd
import matplotlib.pyplot as plt


# name of the zip file with data
datafile = "./data/KNMI_20190815_hourly.zip"
# url of the same file (to download if it is not available locally)
dataurl = "https://github.com/asselapathirana/pythonbootcamp/releases/download/NA/KNMI_20190815_hourly.zip"
# is the file available locally ?
# note: this is a very simple test for existance of the file!
# if we want to force the program to download file, simply delete the zip file and run again!
if not os.path.isfile(datafile):
    # download the file
    wget.download(dataurl, datafile)

# remember pandas counts from 0!
# skip the first 32 (index 0-31) lines and 34th (index 33)
skip = list(range(32)) + [33]
data = pd.read_csv(
    datafile,  # data file name
    sep=",",  # values are seprated by comma
    skiprows=skip,  # skipe the rows with these indexes
    skipinitialspace=True,  # any whitespace before a value will be ignored
)
# lets create a new index of  Datetime
data.index = pd.to_datetime(
    data["YYYYMMDD"].astype(str)  # take YYYYMMDD column as a string
    + " "  # add a space
    + (data["HH"] - 1)
    .astype(str)
    .str.pad(
        width=2, fillchar="0"
    ),  # take HH column as string, add a leading zero if needed (e.g. 14-> 14, 1->01)
    format="%Y%m%d %H",  # tell pandas how our datetime string looks like e.g. '20010708 03'
)

# remove columns 'YYYYDDMM', 'HH' - we don't need them any more. also drop '# STN' column - useless!
data.drop(columns=["YYYYMMDD", "HH", "# STN"], inplace=True)

# Read the header of the data, many columns are represented by 0.1 units (e.g. rainfall .1 mm units). So before using the data any further
# it is needed to multiply them by the correct scale factor (often .1)
# FH       = Uurgemiddelde windsnelheid (in 0.1 m/s). Zie http://www.knmi.nl/kennis-en-datacentrum/achtergrond/klimatologische-brochures-en-boeken; 
# FF       = Windsnelheid (in 0.1 m/s) gemiddeld over de laatste 10 minuten van het afgelopen uur; 
# FX       = Hoogste windstoot (in 0.1 m/s) over het afgelopen uurvak; 
# T        = Temperatuur (in 0.1 graden Celsius) op 1.50 m hoogte tijdens de waarneming; 
# T10N     = Minimumtemperatuur (in 0.1 graden Celsius) op 10 cm hoogte in de afgelopen 6 uur; 
# TD       = Dauwpuntstemperatuur (in 0.1 graden Celsius) op 1.50 m hoogte tijdens de waarneming; 
# SQ       = Duur van de zonneschijn (in 0.1 uren) per uurvak, berekend uit globale straling  (-1 for <0.05 uur); 
# Q        = Globale straling (in J/cm2) per uurvak; 
# DR       = Duur van de neerslag (in 0.1 uur) per uurvak; 
# RH       = Uursom van de neerslag (in 0.1 mm) (-1 voor <0.05 mm); 
# P        = Luchtdruk (in 0.1 hPa) herleid naar zeeniveau, tijdens de waarneming;
data["FF"] = data["FF"] * 0.1
data["FX"] = data["FX"] * 0.1
data["T"] = data["T"] * 0.1
data["T10"] = data["T10"] * 0.1
data["SQ"] = data["SQ"].clip(lower=0.0) * 0.1
data["DR"] = data["DR"] * 0.1
data["RH"] = data["RH"].clip(lower=0.0) * 0.1
data["P"] = data["P"] * 0.1
#

# save the data so that we can use it later (with other scripts)

data.to_pickle(datafile+".pickle", compression='zip')




# resample data annually and plot
an = data["T"].resample("1y").max()
ax = an.plot(figsize=(15, 4))
an.rolling(10, center=True).mean().plot(ax=ax)
plt.show()
