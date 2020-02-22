import requests
import operator
import pandas as pd
from datetime import timedelta, date, datetime

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
            url_station = 'https://esi.evetech.net/latest/markets/' + \
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
        # print(i, end='\r')
        i += 1

    return singleItemsLow


def svrCalc(data):
    # create DF for holding final items
    df1 = pd.DataFrame()
    for type_id in data['type_id']:
        # try excludes any sold_items/0 issues
        try:
            sold_items = productTotalSold(int(type_id))
            added_items = productTotalAdded(int(type_id))
            SVR = (sold_items/added_items)*100
        except Exception:
            continue

        # Output SVR value
        margin = ((float(data['Sell Price']) -
                  float(data['Buy Price']))/float(data['Buy Price']))*100
        if SVR >= 100 and added_items >= 14:
            df2 = pd.DataFrame[int(type_id), data['type_id'], int(SVR)]
            df1.append(df2, ignore_index=True, inplace=True)
            print(str(int(type_id)) + ': ' + data['type_id'] +
                  ' Sales to Volume Ratio (%) =', int(SVR))
            print('Margin = %.2f' % margin, '%')
            print('Total Sold:', sold_items, 'Total Posted:', added_items)
    print(df1)
    return df1

    print(datetime.today())
    print('')
    print('End Items')


def productTotalSold(number):
    time_diff = date.today() - timedelta(days=14)
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
        if products_sold['date'] > str(time_diff):
            sales.append(products_sold['volume'])

    weekly_sales = sum(sales)
    # print('Item Id: ' + str(number) ,'Weekly sales: ',weekly_sales)
    return weekly_sales


def productTotalAdded(number):
    time_diff = date.today() - timedelta(days=14)
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
        if items_total['issued'] > str(time_diff):
            volumes.append(items_total['volume_total'])
            # print('Items added per day:', items_total['volume_total'])

    weekly_vol = sum(volumes)
    # print('Items added: ', weekly_vol)
    return weekly_vol
