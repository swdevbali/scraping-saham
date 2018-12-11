"""
GET: data muncul jika url dijalankan lewat broswer
POST: data tidak bs diambil lewat browesr, namun via <FORM/> POST
"""


def generate_chart(perusahaan, durasi='1W'):
    """
    Fungsi ini akan menghasilkan image data stock seminggu terakhir dari perusahaan tertentu
    :return:
    """
    import requests
    import json
    import pprint
    import time

    try:

        url = 'https://www.idx.co.id/umbraco/Surface/Helper/GetStockChart?indexCode={}&period={}'.format(perusahaan, durasi)
        # DATA ACQUISITION
        result = requests.get(url)
        if result.status_code == 200:
            data = json.loads(result.text)
            pprint.pprint(data)
            print(data['ChartData'])
            chart_data = data['ChartData']

            # Data Processing
            f = open('data.csv', 'w')
            f.write('#Tanggal;Value\n')
            for d in chart_data:
                # tanggal = d['Date']
                tanggal = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(d['Date'])/1000))
                value = d['Close']
                print(tanggal, ';', value)
                f.write('"{}";{}\n'.format(tanggal, value))
            f.close()

    except Exception as ex:
        print(ex)

    #Data Visualization
    #Matplotlib -> Pandas
    from pandas import Series
    from matplotlib import pyplot

    series = Series.from_csv('data.csv', header=0, sep=';')
    pyplot.plot(series)
    pyplot.show()


generate_chart('BBNI', '1Y')

