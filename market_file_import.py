# predicting demand for items using 'SVR' value.

import pandas as pd
from marketFunctions import productTotalSold, productTotalAdded
from datetime import timedelta, date, datetime

def svr_calc(data):
    # sets number of past days to include for number of sold items
    time_diff = date.today() - timedelta(days=14)
    
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

    print(datetime.today())
    print('')
    print('End Items')
