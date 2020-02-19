import requests
import operator
import pandas as pd
from datetime import timedelta, date

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


# retrieves items from a specific station
def get_orders(region, location, pages):
    page = 1
    timeDiff = date.today() - timedelta(days=14)
    # list to store individual trade hub
    station_list = []*(pages*600)
    # list to store url response
    station_List = []
    while page <= pages:
        try:
            url_station = 'https://esi.evetech.net/latest/markets/' + \
                str(region) + '/orders/?datasource=tranquility&order_type=sell&page=' + str(page)
            station_List = requests.get(url_station)

            # list to store JSON return from url
            station_json = station_List.json()

        # initiating loop to get only one location id within a set time period
            for item in station_json:
                if item['location_id'] == location and item['issued'] >= str(timeDiff):
                    station_list.insert(len(station_list), item)
            print(' page = ', page, end='\r')
            page += 1
        except Exception:
            continue

    # ordering list of transactions by item type
    station_list = sorted(station_list, key=operator.itemgetter('price'), reverse=True)
    station_list = sorted(station_list, key=operator.itemgetter('type_id'))

    return station_list


# sorts items and gets each of the lowest priced items from the station
def getLowest(system, location):
    i = 0
    singleItemsLow = []
    for this in system:
        if i < len(system)-1:
            systemOrder = system[i+1]
        if this['type_id'] != systemOrder['type_id']:
            singleItemsLow.append(this)
        # print(i, end='\r')
        i += 1

# using PANDAS for ease of file transfer to disks
# This is not needed if you are good with archaic PYTHON methods.

    df1 = pd.DataFrame(singleItemsLow)
    df1 = df1.set_index(['type_id'])
    df1 = df1.sort_index()

# selection of file name for selected items by location
#    if location == Amarr_location_id:
#        df1.to_csv(r'market_working_files/lowest_items_Amarr.csv')
#    elif location == Hek_location_id:
#        df1.to_csv(r'market_working_files/lowest_items_Hek.csv')
#    elif location == Jita_location_id:
#        df1.to_csv(r'market_working_files/lowest_items_Jita.csv')
#    elif location == Rens_location_id:
#        df1.to_csv(r'market_working_files/lowest_items_Rens.csv')
#    elif location == Dodixie_location_id:
#        df1.to_csv(r'market_working_files/lowest_items_Dodixie.csv')

    return singleItemsLow


def product_total_sold(number):
    timeDiff = date.today() - timedelta(days=14)
    url = 'https://esi.evetech.net/latest/markets/' + Domain \
        + '/history/?datasource=tranquility&type_id=' + str(number)
    region = requests.get(url)
    all_region_Markets = region.json()
    # print(all_region_Markets)

    sales = []
    # find items sold per day
    for products_sold in all_region_Markets:
        # print(products_sold['date'], number,' sales per day:', products_sold['volume'])
        # print(products_sold.keys())
        if products_sold['date'] > str(timeDiff):
            sales.append(products_sold['volume'])

    weekly_sales = sum(sales)
    # print('Item Id: ' + str(number) ,'Weekly sales: ',weekly_sales)
    return weekly_sales


def product_total_added(number):
    timeDiff = date.today() - timedelta(days=14)
    url2 = 'https://esi.evetech.net/latest/markets/' + Domain + \
        '/orders/?datasource=tranquility&order_type=sell&page=1&type_id=' + str(number)
    daily_items = requests.get(url2)
    all_products = daily_items.json()
    # print(all_products)
    # number of items on market per day
    volumes = []
    # Find total items added to market in 7 days.
    for items_total in all_products:
        # print(items_total.keys())
        if items_total['issued'] > str(timeDiff):
            volumes.append(items_total['volume_total'])
            # print('Items added per day:', items_total['volume_total'])

    weekly_vol = sum(volumes)
    # print('Items added: ', weekly_vol)
    return weekly_vol
