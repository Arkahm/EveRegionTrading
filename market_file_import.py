# predicting demand for items using 'SVR' value.

import pandas as pd
from marketFunctions import product_total_sold, product_total_added
from datetime import timedelta, date, datetime

file = 'market_working_files/hi_low_price.csv'
data = pd.read_csv(file, index_col=0)
print(datetime.today())
# print(data.keys())
# print(type(data[['TypeID']]))
count = 0
timeDiff = date.today() - timedelta(days=14)
df1 = pd.DataFrame()
for type_id, item_name in data.iterrows():
    # try excludes any sold_items/0 issues
    try:
        sold_items = product_total_sold(int(type_id))
        added_items = product_total_added(int(type_id))
        SVR = (sold_items/added_items)*100
    except Exception:
        continue

    # Output SVR value
    margin = ((float(item_name['Sell Price']) -
              float(item_name['Buy Price']))/float(item_name['Buy Price']))*100
    if SVR >= 100 and added_items >= 14:
        count += 1
        df2 = pd.DataFrame[int(type_id), item_name['Item'], int(SVR)]
        df = df1.append(df2, ignore_index=True)
        print(str(int(type_id)) + ': ' + item_name['Item'] +
              ' Amarr Sales to Volume Ratio (%) =', int(SVR))
        print('Margin = %.2f' % margin, '%')
        print('Total Sold:', sold_items, 'Total Posted:', added_items)
#    else:
#        print(str(int(type_id)) + ': ' + item_name['Item'])
print(df)

print(datetime.today())
# print(df)
print('')
print(count, ' Items')
print('')
print('End Items')
