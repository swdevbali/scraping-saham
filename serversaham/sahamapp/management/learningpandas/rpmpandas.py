import os
import pandas as pd
import pprint

# SERIES: ARRAY 1 Dimensi

country = pd.Series([3, -5, 7, 4],
                    index=['2018-12-13', '2018-12-14', '2018-12-15', '2018-12-16'])
print(country)

# DATAFRAME: ARRAY 2 Dimensi
data = {'Country':['a',' b', 'c'],
        'Capital':['a1', 'b1', 'c1'],
        'Population':[1000,2000,3000]
        }
df = pd.DataFrame(data, columns=['Country', 'Capital', 'Population'])
print(df)

data_csv = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data.csv'), header=0, sep=',')
print(data_csv.head())

df.to_excel(os.path.join(os.path.dirname(__file__), 'data.xlsx'), sheet_name='data')

