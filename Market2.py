import requests
import pandas as pd
from datetime import datetime
from operator import itemgetter
from marketFunctions import getOrders, getLowest, idConverter, svrCalc

#  reference
Domain = 10000043
Amarr_location_id = 60008494
Metropolis = 10000042
Hek_location_id = 60005686
Forge = 10000002
Jita_location_id = 60003760
Heimatar = 10000030
Rens_location_id = 60004588
SinqLaison = 10000032
Dodixie_location_id = 60011866

# Begin script process
pd.set_option('display.max_rows', 300)
pd.set_option('display.max_colwidth', 60)

start = datetime.today()
print(start)

# preliminary location, counter, and list requirements
regions = [Domain,
           SinqLaison]
locations = [Amarr_location_id,
             Dodixie_location_id]
locations_count = 0
lowest_highest = []

# sets the number of ESI pages to loop through in order to
# pull ALL items and will assign where to search
for region in regions:
    url_station = 'https://esi.evetech.net/latest/markets/' + \
        str(region) + '/orders/?datasource=tranquility&order_type=sell'
    region_list = requests.get(url_station)
    num_pages = region_list.headers['x-pages']
    orders = getOrders(region, locations[locations_count], int(num_pages))
    lowest = getLowest(orders)
    locations_count += 1
    print(datetime.today() - start)

# combines individual station list into one large market list
    lowest_highest.extend(lowest)

df2 = pd.DataFrame(lowest_highest)

# Replace location id number with actual location name
replace_location = {
    60008494: 'Amarr',
    60005686: 'Hek',
    60003760: 'Jita',
    60004588: 'Rens',
    60011866: 'Dodixie'
}
df2.replace(replace_location, inplace=True)
df2.reset_index(drop=True, inplace=True)
#  print(df2.head(20))  # for testing
df2.sort_values(by=['type_id'], inplace=True)

# groups type id's and gets min/max price
# and calculate margin
typeid_grp = df2.groupby('type_id')

type_group_marg = typeid_grp[['location_id', 'price']].agg(['min', 'max'])
type_group_marg.rename(columns={'min': 'Buy Price', 'max': 'Sell Price'}, inplace=True)
type_group_marg['Margin'] = ((type_group_marg['price']['Sell Price'] - type_group_marg['price']
                             ['Buy Price'])/type_group_marg['price']['Sell Price'])*100

# filters DF to only above 40% margin
type_group_marg = type_group_marg[type_group_marg['Margin'] >= 40]
type_group_marg.reset_index(inplace=True)

# make a list of type id's to get item names
id_list = list(type_group_marg['type_id'])
# print(len(id_list))  # for testing

# names of items
name_list = idConverter(id_list)
name_list = sorted(name_list, key=itemgetter('id'))
name_df = pd.DataFrame(name_list)
name_df.drop(['category', 'id'], axis=1, inplace=True)

# adds 'name' column to main DF.
type_group_marg.insert(1, 'name', name_df)
print(len(type_group_marg))

# print(str(len(type_group_marg)) + ' items\n', type_group_marg.head(20))
type_group_marg.to_csv(r'market_working_files/hi_low_price.csv')

final_df = svrCalc(type_group_marg)
print(len(final_df))  # For testing
print(final_df)  # for testing
final_df.to_html(r'market_working_files/group_table.html',
                 float_format='%.2f',
                 justify='justify-all')

print(datetime.today() - start)

print(datetime.today())
