import base64
import io
import json
import os
import pprint
import time
from statistics import mean

import requests

import matplotlib
import numpy as np
from celery import shared_task
from matplotlib import pyplot, style
from pandas import Series


@shared_task
def do_scraping(perusahaan, durasi):

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
            file_path = os.path.join(
                os.getcwd(), f'data-{perusahaan}-{durasi}.csv')
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
    series = Series.from_csv(
        f'data-{perusahaan}-{durasi}.csv', header=0, sep=',')
    pyplot.clf()
    pyplot.plot(series)

    # Django fix: create in buffer first
    buf = io.BytesIO()
    pyplot.savefig(buf)
    pyplot.close(f)
    f.clear()
    pyplot.gcf().clear()

    result = {
        'img_base64': base64.b64encode(buf.getvalue()).decode()
    }

    return result


@shared_task
def do_linear_regression(x, y, x_predict):
    """
    celery task for linear regression
    """
    x = np.array([i + 1 for i in range(len(x))])
    y = np.array([float(x) for x in y], dtype=np.float64)

    def best_fit_line(x_values, y_values):
        m = (((mean(x_values) * mean(y_values)) - mean(x_values * y_values)) /
             ((mean(x_values) * mean(x_values)) - mean(x_values * x_values)))

        b = mean(y_values) - m * mean(x_values)

        return m, b  # tupple

    m, b = best_fit_line(x, y)
    print("regression line: " + "y = " +
          str(round(m, 2)) + "x + " + str(round(b, 2)))

    # Prediction
    y_prediction = (m * x_predict) + b
    print("predicted coordinate: (" + str(round(x_predict, 2)) +
          "," + str(round(y_prediction, 2)) + ")")

    # y values of regression line
    # list
    regression_line = [(m * x) + b for x in x]
    print(regression_line)

    # Plotting

    style.use('seaborn')

    pyplot.title('Linear Regression')
    pyplot.scatter(x, y, color='#5b9dff', label='data')
    pyplot.scatter(x_predict, y_prediction, color='#fc003f', label="predicted")
    pyplot.plot(x, regression_line,
                color='000000', label='regression line')
    pyplot.legend(loc=4)

    # Django fix: create in buffer first
    buf = io.BytesIO()
    pyplot.savefig(buf)
    pyplot.gcf().clear()

    result = {
        'img_base64': base64.b64encode(buf.getvalue()).decode()
    }

    return result
