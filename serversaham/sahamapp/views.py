from django.shortcuts import render
from django.http import HttpResponse
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure
import requests


def index(request):
    return render(request,'index.html')


def get_chart(request, code, period):
    import json
    import pprint
    import time
    import io
    import matplotlib
    from pandas import Series
    from matplotlib import pyplot

    try:
        # DATA ACQUISITION
        url = 'https://www.idx.co.id/umbraco/Surface/Helper/GetStockChart?indexCode={}&period={}'\
            .format(code,period)

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
    f = matplotlib.figure.Figure()
    series = Series.from_csv('data.csv', header=0, sep=',')
    pyplot.clf()
    pyplot.plot(series)

    buf = io.BytesIO()
    pyplot.savefig(buf, format='png')
    pyplot.close()

    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response
