import requests
import operator
import pandas as pd
import numpy as np
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
def getOrders(region, location, pages):
    page = 1
    time_diff = date.today() - timedelta(days=14)

    # list to store individual trade hub
    station_list = []*(pages*600)

    # list to store url response
    station_List = []
    while page <= pages:
        try:
            url_station = 'https://esi.evetech.net/dev/markets/' + \
                str(region) + '/orders/?datasource=tranquility&order_type=sell&page=' + str(page)
            station_List = requests.get(url_station)

            # list to store JSON return from url
            station_json = station_List.json()

        # initiating loop to get only one location id within a set time period
            for item in station_json:
                if item['location_id'] == location and item['issued'] >= str(time_diff):
                    station_list.insert(len(station_list), item)
            print(' Page =', page, end='\r')
            page += 1
        except Exception:
            continue

    # ordering list of transactions by item type
    station_list = sorted(station_list, key=operator.itemgetter('price'), reverse=True)
    station_list = sorted(station_list, key=operator.itemgetter('type_id'))

    return station_list


# sorts items and gets each of the lowest priced items from the station
def getLowest(systems):
    i = 0
    singleItemsLow = []
    for system in systems:
        if i < len(systems)-1:
            system_order = systems[i+1]
        if system['type_id'] != system_order['type_id']:
            singleItemsLow.append(system)
        i += 1

    return singleItemsLow


def svrCalc(data):
    # create DF for holding final items
    df1 = pd.DataFrame()
    # print(data)  # for testing
    data.set_index('type_id', inplace=True)

    # print(data)  # for testing
    n = 1
    for type_id, item_name in data.iterrows():
        # try excludes any sold_items/0 issues
        try:
            if item_name[('location_id', 'Sell Price')] == 'Amarr':
                sold_items = productTotalSold(type_id, str(Domain))
                added_items = productTotalAdded(type_id, str(Domain))
            elif item_name[('location_id', 'Sell Price')] == 'Dodixie':
                sold_items = productTotalSold(type_id, str(SinqLaison))
                added_items = productTotalAdded(type_id, str(SinqLaison))
            elif item_name[('location_id', 'Sell Price')] == 'Hek':
                sold_items = productTotalSold(type_id, str(Metropolis))
                added_items = productTotalAdded(type_id, str(SinqLaison))
            elif item_name[('location_id', 'Sell Price')] == 'Jita':
                sold_items = productTotalSold(type_id, str(Forge))
                added_items = productTotalAdded(type_id, str(Forge))
            elif item_name[('location_id', 'Sell Price')] == 'Rens':
                sold_items = productTotalSold(type_id, str(Heimatar))
                added_items = productTotalAdded(type_id, str(Heimatar))
            SVR = (sold_items/added_items)*100
        except Exception:
            continue

        # Output SVR value
        if SVR >= 150 and added_items >= 14 and sold_items >= 14:
            print('Gathering items...(' + str(n) + ')', end='\r')
            df2 = pd.DataFrame([[int(type_id), item_name['name'].to_string(),
                               item_name[('location_id', 'Buy Price')],
                               float(item_name[('price', 'Buy Price')]),
                               item_name[('location_id', 'Sell Price')],
                               float(item_name[('price', 'Sell Price')]),
                               int(SVR), float(item_name['Margin'].values)]],
                               index=[0], columns=['Type ID',
                                                   'Name',
                                                   'Buy Location',
                                                   'Buy Price',
                                                   'Sell Location',
                                                   'Sell Price',
                                                   'SVR',
                                                   'Margin'])
            df1 = pd.concat([df1, df2], ignore_index=True)
            n += 1
        # print(df1)  # for testing
    print('End Items\n')
    return df1


def productTotalSold(number, station):
    time_diff = date.today() - timedelta(days=14)
    url = 'https://esi.evetech.net/latest/markets/' + station + \
        '/history/?datasource=tranquility&type_id=' + str(number)
    region = requests.get(url)
    all_region_Markets = region.json()
    # print(all_region_Markets)  # for testing
    sales = []

    # find items sold per day
    for products_sold in all_region_Markets:
        if products_sold['date'] > str(time_diff):
            sales.append(products_sold['volume'])

    weekly_sales = sum(sales)
    # print(weekly_sales)  # for testing
    return weekly_sales


def productTotalAdded(number, station):
    time_diff = date.today() - timedelta(days=14)
    url2 = 'https://esi.evetech.net/dev/markets/' + station + \
        '/orders/?datasource=tranquility&order_type=sell&page=1&type_id=' + str(number)
    daily_items = requests.get(url2)
    all_products = daily_items.json()
    # print(all_products)  # for testing
    # number of items on market per day
    volumes = []
    # Find total items added to market in 14 days.
    for items_total in all_products:
        # print(items_total.keys())  # for testing
        if items_total['issued'] > str(time_diff):
            volumes.append(items_total['volume_total'])

    weekly_vol = sum(volumes)
    # print(weekly_vol)  # for testing
    return weekly_vol


def idConverter(id):
    split_list = np.array_split(id, 10)
    # print(split_list)  # for testing
    added_names = []
    for arr in split_list:
        arr = arr.tolist()
        # print(type(arr))  # for testing
        url = 'https://esi.evetech.net/dev/universe/names/?datasource=tranquility'
        r = requests.post(url, json=arr)
        # print(type(r))  # for testing
        names = r.json()
        added_names.extend(names)

    return added_names


def deleteGroups():
    groups = [280, 281, 282, 284, 342, 343, 344, 345, 346, 347, 348, 349, 350, 352,
              355, 356, 360, 370, 371, 400, 401, 408, 409, 447, 477, 486, 487, 489,
              490, 493, 500, 503, 516, 525, 651, 723, 727, 787, 841, 853, 854, 855,
              856, 857, 858, 860, 870, 871, 879, 912, 914, 915, 917, 918, 944, 945,
              965, 976, 1013, 1045, 1048, 1083, 1084, 1088, 1089, 1090, 1091, 1092,
              1137, 1139, 1142, 1143, 1144, 1145, 1146, 1147, 1151, 1152, 1160, 1162,
              1190, 1194, 1195, 1197, 1206, 1222, 1224, 1225, 1239, 1248, 1271, 1293,
              1294, 1317, 1318, 1397, 1399, 1461, 1462, 1543, 1670, 1679, 1703, 1707,
              1708, 1709, 1718, 1723, 1810, 1812, 1888, 1889, 1890, 1950, 1953]

    del_group_list = []
    for group in groups:
        group_url = 'https://esi.evetech.net/dev/universe/groups/' + str(group) + \
                    '/?datasource=tranquility&language=en-us'
        group_r = requests.get(group_url)
        group_json = group_r.json()
        # print(group_json)
        del_group = group_json['types']
        del_group_list.extend(del_group)
    # print(del_group_list)
    return del_group_list
