"""
GET: data muncul jika url dijalankan lewat broswer
POST: data tidak bs diambil lewat browesr, namun via <FORM/> POST
"""

def generate_chart(company_code, time_range):
    import requests
    import json
    import pprint
    import time
    from pandas import Series
    from matplotlib import pyplot

    try:
        # DATA ACQUISITION
        result = requests.get('https://www.idx.co.id/umbraco/Surface/Helper/GetStockChart?indexCode={}&period={}'.format(company_code,time_range))
        if result.status_code == 200:
            data = json.loads(result.text)
            pprint.pprint(data)
            print(data['ChartData'])
            chart_data = data['ChartData']

            # DATA PROCESSING
            f = open('data.csv', 'w')
            f.write('#Tanggal,Value\n')
            for d in chart_data:
                tanggal = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(d['Date']) / 1000))
                value = d['Close']
                print(tanggal, ';', value)
                f.write('"{}",{}\n'.format(tanggal, value))
            f.close()


    except Exception as ex:
        print(ex)

    # DATA VIZUALISATION
    series = Series.from_csv('data.csv')
    pyplot.plot(series)
    pyplot.show()

generate_chart('TLKM','1W')

