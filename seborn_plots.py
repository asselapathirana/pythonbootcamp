import numpy as np
import pandas as pd
import seaborn as sns

data = pd.read_pickle("./data/KNMI_20190815_hourly.zip.pickle", compression="zip")

# see the relationship between pressure and relative humidity

sns.jointplot("P", "U", data=data, kind='kde')
sns.show()


