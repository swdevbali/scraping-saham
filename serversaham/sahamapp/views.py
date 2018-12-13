import csv
import io
import os
from statistics import mean

import matplotlib
import base64
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from matplotlib import pyplot 
from matplotlib import style
from pandas import Series


def get_chart(requests, perusahaan, durasi):
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
        # DATA ACQUISITON
        result = requests.get(url)
        if result.status_code == 200:

            data = json.loads(result.text)

            pprint.pprint(data)
            print(data['ChartData'])
            chart_data = data['ChartData']

            # DATA PROCESSING
            file_path = os.path.join(os.getcwd(), 'data.csv')
            f = open(file_path, 'w')
            f.write('#Tanggal;Value\n')

            for d in chart_data:
                # print()
                tanggal = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(int(d['Date'])/1000))
                value = d['Close']
                print(tanggal, ';', value)
                f.write('"{}",{}\n'.format(tanggal, value))
            f.close()
    except Exception as ex:
        print(ex)

    # DATA VISUALIZATION
    f = matplotlib.figure.Figure()
    series = Series.from_csv('data.csv', header=0, sep=',')
    pyplot.clf()
    pyplot.plot(series)

    # Django fix: create in buffer first
    buf = io.BytesIO()
    pyplot.savefig(buf, format='png')
    pyplot.close(f)

    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response


def index(request):
    return render(request, 'index.html')


def linreg_view(request):
    return render(request, 'linreg.html')


@require_POST
def linreg_process(request):
    time_series_csv = request.FILES.get('time_series_csv')

    if not time_series_csv.name.endswith('csv'):
        return 'error'

    data = [x.decode().strip().split(',')
            for x in time_series_csv.readlines() if not x.decode().startswith('#')]

    x_values, y_values = zip(*data)
    x_values = np.array([x + 1 for x in range(len(x_values))])
    y_values = np.array([float(x) for x in y_values], dtype=np.float64)

    def best_fit_line(x_values, y_values):
        m = (((mean(x_values) * mean(y_values)) - mean(x_values * y_values)) /
             ((mean(x_values) * mean(x_values)) - mean(x_values * x_values)))

        b = mean(y_values) - m * mean(x_values)

        return m, b  # tupple

    m, b = best_fit_line(x_values, y_values)
    print("regression line: " + "y = " +
          str(round(m, 2)) + "x + " + str(round(b, 2)))

    # Prediction
    print(request.POST.get('x_predicted'))
    x_prediction = int(request.POST.get('x_predicted'), 0)
    y_prediction = (m * x_prediction) + b
    print("predicted coordinate: (" + str(round(x_prediction, 2)) +
          "," + str(round(y_prediction, 2)) + ")")

    # y values of regression line
    # list
    regression_line = [(m * x) + b for x in x_values]
    regression_line_copy = [x for x in x_values]
    print(regression_line)

    # Plotting

    style.use('seaborn')

    pyplot.title('Linear Regression')
    pyplot.scatter(x_values, y_values, color='#5b9dff', label='data')
    pyplot.scatter(x_prediction, y_prediction, color='#fc003f', label="predicted")
    pyplot.plot(x_values, regression_line,
             color='000000', label='regression line')
    pyplot.legend(loc=4)

    # Django fix: create in buffer first
    buf = io.BytesIO()
    pyplot.savefig(buf)
    pyplot.close()

    returned = base64.b64encode(buf.getvalue()).decode()
    response = HttpResponse(returned)
    return response
