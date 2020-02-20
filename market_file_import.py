# predicting demand for items using 'SVR' value.

import pandas as pd
from marketFunctions import productTotalSold, productTotalAdded
from datetime import timedelta, date, datetime

file = 'market_working_files/hi_low_price.csv'
data = pd.read_csv(file, index_col=0)
print(datetime.today())
# print(data.keys())
# print(type(data[['TypeID']]))
count = 0
timeDiff = date.today() - timedelta(days=14)
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
        count += 1
        df2 = pd.DataFrame[int(type_id), data['type_id'], int(SVR)]
        df1.append(df2, ignore_index=True, inplace=True)
        print(str(int(type_id)) + ': ' + data['type_id'] +
              ' Amarr Sales to Volume Ratio (%) =', int(SVR))
        print('Margin = %.2f' % margin, '%')
        print('Total Sold:', sold_items, 'Total Posted:', added_items)
#    else:
#        print(str(int(type_id)) + ': ' + item_name['Item'])
print(df1)

print(datetime.today())
# print(df)
print('')
print(count, ' Items')
print('')
print('End Items')
