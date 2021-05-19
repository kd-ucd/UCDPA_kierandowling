import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.io import output_file, show
from bokeh.plotting import figure, ColumnDataSource
import geopandas as gpd

#Company data on Fortune 1000 companies.
#Data was collected for the year end February 2021
#https://www.kaggle.com/winston56/fortune-500-data-2021
#gps_data.csv manually generated

# importing and cleaning the data
f1000 = pd.read_csv("data/Fortune_1000.csv")
print(f1000.info())
print(f1000.isnull().sum())
#dropCol = f1000.dropna(axis=1, subset=['newcomer'])
#print(dropCol.shape)
avg_rev = np.mean(f1000['revenue'])
mean_rev = np.median(f1000['revenue'])
print('The average revuene is ' + str(avg_rev) + ' and the median is ' + str(mean_rev))


# is there a corrolation between company revenue vs employee headcount
num_emp = f1000['num. of employees']
rev = f1000['revenue']

#plt.scatter(rev, num_emp, s=10)
#plt.show()


# how many companies were profitable in 2020
are_profitable = (f1000['profit']>0)
values = are_profitable.value_counts().values
index = are_profitable.value_counts().index
# DO THIS IN A SMARTER WAY. ADD COLUMN AND INCLUDE YES NO BASED ON + - TO GET VALUES. fUNCTION?
#plt.bar(index, values)
#plt.show()

# visualising the revenue of the top 10 most profitable companies
most_profitable = f1000.sort_values('profit', ascending=False)
top10_profitable = most_profitable.iloc[:10]
top10_comp = top10_profitable['company']
top10_rev = top10_profitable['revenue']
plt.barh(top10_comp, top10_rev)
#plt.show()


# looping through data top find the CEOs of the top 10 most profitable companies
df = pd.DataFrame(top10_profitable)
ceo = df.set_index('company')

for lab, row in ceo.iterrows():
    print(lab + ': ' + row['CEO'])

#interactive visualization
f1000_df = pd.DataFrame(f1000)
source = ColumnDataSource(df)
p = figure(plot_width=500, plot_height=500, x_axis_label='Market Cap', y_axis_label='Revenue')
p.circle(x='Market Cap', y='revenue', source=source)
#output_file('bokeh.html')
#show(p)

# merging dataframe containing top 10 most profitable companies with GPS data for geospatial visualisations
hq_df = pd.DataFrame({ 'company': [	'Berkshire Hathaway',	'Apple',	'Microsoft',	'JPMorgan Chase',	'Alphabet',	'Bank of America',	'Intel',	'Wells Fargo',	'Citigroup',	'Verizon Communications'],
            'HQ_GPS_lat': [	41.2665652155238,	37.3320344033222,	47.6423030655177,	40.7560918430126,	37.4244444307427,	35.2516984332765,	37.3872860733935,	37.7939978437439,	40.7207149964738,	40.7544511859009],
            'HQ_GPS_lng': [	-95.9359591891807,	-122.029665403973,	-122.136943931254,	-73.9755801511926,	-122.083169609495,	-80.8643427511356,	-121.963906989321,	-122.402969302892,	-74.0112209712649,	-73.9848621227913]})

# merge
top10_with_gps = df.merge(hq_df)

states = gpd.read_file('data/geo/USA_States_Generalized.shp')
states.plot(figsize=(10,10), cmap = 'Dark2')
pins = sns.scatterplot(data=top10_with_gps, x='HQ_GPS_lng', y='HQ_GPS_lat', hue='company')
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.title('Headquarters of the top 10 most profitable companies')
#plt.show()


