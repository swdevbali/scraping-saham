from django.shortcuts import render
from django.http import HttpResponse
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure


def generate_chart(company_code, periode='1Y'):
    import requests
    import json
    import pprint
    import time
    from pandas import Series
    from matplotlib import pyplot

    try:
        # DATA ACQUISITION
        url = 'https://www.idx.co.id/umbraco/Surface/Helper/GetStockChart?indexCode={}&period={}'.format(company_code,periode)
        result = requests.get(url)
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

    fig = Figure()
    canvas = FigureCanvas()



# Create your views here.
def get_chart(request):
    """
    Ambil data dari IDX kemudian plot time series
    :param request:
    :return:
    """
    return HttpResponse('Hello World!')