import os
import pandas as pd
import pprint

# SERIES: Array satu dimensi
country = pd.Series([3, -5, 7, 4],
                    index=['2012-12-3', '2012-12-14', '2012-12-15',
                           '2012-12-16'])
print(country)
# DATAFRAME: Array dua dimensi
data = {'Country': ['Belgium', 'India', 'Brazil'],
        'Capital': ['Brussels', 'New Delhi', 'Brasilia'],
        'Population': [11190846, 1303171035, 207847528]}
df = pd.DataFrame(data,columns=['Country',  'Capital',  'Population'])
pprint.pprint(df)

data_csv = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data.csv'),
                       header=0, sep=',')
#openpyxl
df.to_excel(os.path.join(os.path.dirname(__file__),'data.xlsx'),
              sheet_name='Sheet1')
print(df)
# NOTE: ALSO SUPPORT EXPORT TO DATABASE

#SLICING
print('1', country[:])
print('2', country[1:1])
#FINISH!