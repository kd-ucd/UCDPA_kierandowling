import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.io import output_file, show
from bokeh.plotting import figure, ColumnDataSource
import geopandas as gpd

# Company data on Fortune 1000 companies.
# Data was collected for the year end February 2021
# https://www.kaggle.com/winston56/fortune-500-data-2021
# gps_data.csv manually generated
# Shape file downloaded from the United States Census Bureau
#https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html

# importing and cleaning the data
f1000 = pd.read_csv("data/Fortune_1000.csv")
print(f1000.info())
print(f1000.isnull().sum())
# there are 500 null values in the newcomer column. No further analysis will be done on this column so let's drop it. There are other null values, in Ticker for example. Nulls will not effect analysis so choosing to leave as is.
f1000.drop(['newcomer'], axis=1, inplace=True)


avg_rev = round(np.mean(f1000['revenue'])*1000000)
med_rev = round(np.median(f1000['revenue'])*1000000)
avg_rev_legible =  '{:,}'.format(avg_rev)
med_rev_legible =  '{:,}'.format(med_rev)
print('The average revenue is $' + str(avg_rev_legible) + '  and the median is $' + str(med_rev_legible))

# is there a correlation between company revenue vs employee headcount
sector = f1000['sector']
rev = f1000['revenue']
rev_sector = plt.barh(sector, rev)
plt.ylabel('Sector')
plt.xlabel('Revenue ($M)')
plt.title('Revenue by Sector')
#plt.show()

# how many companies were profitable in 2020
print(f1000.value_counts(['profitable']))
profitable = sns.countplot(data=f1000, x='profitable')
profitable.set_title('Profitable vs Not Profitable Companies')
profitable.set(xlabel='Profitable', ylabel='Number of companies')
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

# interactive visualization
f1000_df = pd.DataFrame(f1000)
source = ColumnDataSource(df)
p = figure(plot_width=500, plot_height=500, x_axis_label='Market Cap', y_axis_label='Revenue', title='Interactive visualisation of Market Cap vs Revenue')
p.circle(x='Market Cap', y='revenue', source=source)
output_file('bokeh.html')
show(p)

# merging dataframe containing top 10 most profitable companies with GPS data for geospatial visualisations
hq_df = pd.DataFrame({'company': ['Berkshire Hathaway', 'Apple', 'Microsoft', 'JPMorgan Chase', 'Alphabet',
                                  'Bank of America', 'Intel', 'Wells Fargo', 'Citigroup', 'Verizon Communications'],
                      'HQ_GPS_lat': [41.2665652155238, 37.3320344033222, 47.6423030655177, 40.7560918430126,
                                     37.4244444307427, 35.2516984332765, 37.3872860733935, 37.7939978437439,
                                     40.7207149964738, 40.7544511859009],
                      'HQ_GPS_lng': [-95.9359591891807, -122.029665403973, -122.136943931254, -73.9755801511926,
                                     -122.083169609495, -80.8643427511356, -121.963906989321, -122.402969302892,
                                     -74.0112209712649, -73.9848621227913]})

# merge dataframes
top10_with_gps = df.merge(hq_df)

states = gpd.read_file('data/geo/USA_States_Generalized.shp')
states.plot(figsize=(10, 10), cmap='Blues', edgecolor="black")
pins = sns.scatterplot(data=top10_with_gps, x='HQ_GPS_lng', y='HQ_GPS_lat', hue='company')
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.title('Headquarters of the top 10 most profitable companies')
#plt.show()

# creating a function extract some key information about a specified company
index_df = f1000_df.set_index('company')

def comp_info(company):
    print(f"Company: {company}")

comp_info('Apple')
