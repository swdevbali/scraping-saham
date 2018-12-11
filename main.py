"""
GET: data muncul jika url dijalankan lewat broswer
POST: data tidak bs diambil lewat browesr, namun via <FORM/> POST
"""
import requests
import json
import pprint
import time

try:
    result = requests.get('https://www.idx.co.id/umbraco/Surface/Helper/GetStockChart?indexCode=SRTG&period=1W')
    if result.status_code == 200:
        data = json.loads(result.text)
        pprint.pprint(data)
        print(data['ChartData'])
        chart_data = data['ChartData']

        f = open('data.csv', 'w')
        f.write('#Tanggal;Value\n')
        for d in chart_data:
            tanggal = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(d['Date'])/1000))
            value = d['Close']
            print(tanggal, ';', value)
            f.write('"{}";{}\n'.format(tanggal, value))
        f.close()

except Exception as ex:
    print(ex)
