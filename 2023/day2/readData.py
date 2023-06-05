
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

csv_file = './data/AHUH1.csv'
df = pd.read_csv(csv_file, parse_dates=[0], index_col=0)
print(df[:100])
df_monthly = df.resample('M').sum()

sns.histplot(data=df, x='RF_mm', kde=True)

sns.set(style="darkgrid")
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_monthly, x=df_monthly.index, y='RF_mm')
plt.xlabel('Date')
plt.ylabel('RF_mm')
plt.title('Monthly Resampled Time Series')
plt.show()