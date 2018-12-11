"""
GET: data muncul jika url dijalankan lewat broswer
POST: data tidak bs diambil lewat browesr, namun via <FORM/> POST
"""

def generate_chart(perusahaan, durasi='1W'):
    """

    :return:
    """
    import requests
    import json
    import pprint
    import time

    url = 'https://www.idx.co.id/umbraco/Surface/Helper/GetStockChart?indexCode={}&period={}'\
        .format(perusahaan, durasi)

    try:
        result = requests.get(url)
        if result.status_code == 200:
            data = json.loads(result.text)
            pprint.pprint(data)
            print(data['ChartData'])
            chart_data = data['ChartData']

            f = open('data.csv', 'w')
            # f.write('#Tanggal;Value\n')
            for d in chart_data:
                tanggal = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(d['Date'])/1000))
                value = d['Close']
                print(tanggal, ';', value)
                f.write('"{}",{}\n'.format(tanggal, value))
            f.close()

    except Exception as ex:
        print(ex)

    #DATA VISUALIZATION
    #Matplotlib -> Pandas

    from pandas import Series
    from matplotlib import pyplot

    series = Series.from_csv('data.csv')
    pyplot.plot(series)
    pyplot.show()

generate_chart('BBNI', durasi='1Y')