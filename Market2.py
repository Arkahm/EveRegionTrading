import requests
import pandas as pd
from datetime import datetime
from marketFunctions import get_orders, getLowest

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
start = datetime.today()
print(start)

# these functions will set the number of ESI pages to loop through in order to
# pull ALL items and will assign where to search

###############################################################################
#                     Commented out for testing                               #
###############################################################################

url_station = 'https://esi.evetech.net/latest/markets/' + \
    str(Forge) + '/orders/?datasource=tranquility&order_type=sell'
region_List = requests.get(url_station)
no_pages = region_List.headers['x-pages']
jitaOrders = get_orders(Forge, Jita_location_id, int(no_pages))
lowestJita = getLowest(jitaOrders, Jita_location_id)
print(datetime.today() - start)

url_station = 'https://esi.evetech.net/latest/markets/' + str(Domain) + \
    '/orders/?datasource=tranquility&order_type=sell'
region_List = requests.get(url_station)
no_pages = region_List.headers['x-pages']
amarrOrders = get_orders(Domain, Amarr_location_id, int(no_pages))
lowestAmarr = getLowest(amarrOrders, Amarr_location_id)
print(datetime.today() - start)

url_station = 'https://esi.evetech.net/latest/markets/' + \
    str(SinqLaison) + '/orders/?datasource=tranquility&order_type=sell'
region_List = requests.get(url_station)
no_pages = region_List.headers['x-pages']
dodiOrders = get_orders(SinqLaison, Dodixie_location_id, int(no_pages))
lowestDodi = getLowest(dodiOrders, Dodixie_location_id)
print(datetime.today() - start)

url_station = 'https://esi.evetech.net/latest/markets/' + str(Metropolis) + \
    '/orders/?datasource=tranquility&order_type=sell'
region_List = requests.get(url_station)
no_pages = region_List.headers['x-pages']
hekOrders = get_orders(Metropolis, Hek_location_id, int(no_pages))
lowestHek = getLowest(hekOrders, Hek_location_id)
print(datetime.today() - start)

url_station = 'https://esi.evetech.net/latest/markets/' + str(Heimatar) + \
    '/orders/?datasource=tranquility&order_type=sell'
region_List = requests.get(url_station)
no_pages = region_List.headers['x-pages']
rensOrders = get_orders(Heimatar, Rens_location_id, int(no_pages))
lowestRens = getLowest(rensOrders, Rens_location_id)
print(datetime.today() - start)

# combines individual staqtion list into one large market list
lowest_highest = lowestJita + lowestRens + lowestDodi + lowestAmarr + lowestHek

df2 = pd.DataFrame(lowest_highest)
# df2 = df2.set_index(['duration'])
df2 = df2.sort_values(by=['type_id'])
df2.to_csv(r'market_working_files/combined.csv')

print(df2)  # for testing purposes only. It is not needed.

# groups type id's into each type and gets min/max price
typeid_grp = df2.groupby(['type_id'])
type_group_marg = typeid_grp['price'].agg(['min', 'max'])
type_group_marg['Margin'] = ((type_group_marg['max']-type_group_marg['min'])/type_group_marg['max'])*100
print(type_group_marg)

print(datetime.today() - start)

print(datetime.today())
