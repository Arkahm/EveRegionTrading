import requests
import pandas as pd
from datetime import datetime
from marketFunctions import getOrders, getLowest
# import market_file_import

#   reference
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
pd.set_option('display.max_rows', 50)
start = datetime.today()
print(start)

# these functions will set the number of ESI pages to loop through in order to
# pull ALL items and will assign where to search
regions = [Forge, Domain, SinqLaison, Metropolis, Heimatar]
locations = [Jita_location_id, Amarr_location_id, Dodixie_location_id, Hek_location_id, Rens_location_id]
locations_count = 0
lowest_highest = []

for region in regions:
    url_station = 'https://esi.evetech.net/latest/markets/' + \
        str(region) + '/orders/?datasource=tranquility&order_type=sell'
    region_List = requests.get(url_station)
    no_pages = 20  # region_List.headers['x-pages']
    orders = getOrders(region, locations[locations_count], int(no_pages))  # need to advance locations
    lowest = getLowest(orders)
    locations_count += 1
    print(datetime.today() - start)

# combines individual station list into one large market list
    lowest_highest.extend(lowest)

df2 = pd.DataFrame(lowest_highest)
# df2.to_csv(r'market_working_files/combined.csv')

replace_location = {
    60008494: 'Amarr',
    60005686: 'Hek',
    60003760: 'Jita',
    60004588: 'Rens',
    60011866: 'Dodixie'
}

df2.replace(replace_location, inplace=True)

# for testing purposes only. It is not needed.
print(df2.head(20))

# groups type id's into each type and gets min/max price
typeid_grp = df2.groupby(['type_id'])
print(typeid_grp.head(20))
type_group_marg = typeid_grp['price'].agg(['min', 'max'])
print(type_group_marg)
type_group_marg.rename(columns={'min': 'Buy Price', 'max': 'Sell Price'}, inplace=True)
type_group_marg['Margin'] = ((type_group_marg['Sell Price'] -
                             type_group_marg['Buy Price'])/type_group_marg['Sell Price'])*100

# filters DF to only above 40% margin
type_group_marg = type_group_marg[type_group_marg['Margin'] >= 40]

print(type_group_marg.head(20))
type_group_marg.to_csv(r'market_working_files/hi_low_price.csv')

type_group_marg.to_html(r'market_working_files/group_table.html',
                        float_format='%.2f',
                        justify='justify-all')

# market_file_import()

print(datetime.today() - start)

print(datetime.today())
