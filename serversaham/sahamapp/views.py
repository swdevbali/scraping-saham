import io
import os

from django.http import HttpResponse
from matplotlib import pyplot
from pandas import Series


def get_chart(requests):
    perusahaan='SRTG'
    durasi = '1Y'
    """
    Fungsi ini akan menghasilkan image dari data stock seminggu terakhir dari perusahaan tertentu
    :return:
    """
    import requests
    import json
    import pprint
    import time

    url = 'https://www.idx.co.id/umbraco/Surface/Helper/GetStockChart?indexCode={}&period={}'\
        .format(perusahaan, durasi)

    try:
        #DATA ACQUISITON
        result = requests.get(url)
        if result.status_code == 200:

            data = json.loads(result.text)

            pprint.pprint(data)
            print(data['ChartData'])
            chart_data = data['ChartData']

            #DATA PROCESSING
            file_path = os.path.join(os.getcwd(), 'data.csv')
            f = open(file_path, 'w')
            f.write('#Tanggal;Value\n')

            for d in chart_data:
                #print()
                tanggal = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(d['Date'])/1000))
                value = d['Close']
                print(tanggal, ';', value)
                f.write('"{}",{}\n'.format(tanggal, value))
            f.close()
    except Exception as ex:
        print(ex)

    #DATA VISUALIZATION
    import matplotlib
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.backends.backend_agg import FigureCanvasAgg

    from matplotlib.figure import Figure
    import numpy as np


    f = matplotlib.figure.Figure()
    f.text(0, 0, 'Hai')
    series = Series.from_csv('data.csv', header=0, sep=',')
    pyplot.plot(series)

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)
    response=HttpResponse(buf.getvalue(),content_type='image/png')
    response['Content-Length'] = str(len(response.content))
    return response


