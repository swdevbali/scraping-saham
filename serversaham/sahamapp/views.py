import base64
import csv
import io
import os
from statistics import mean

import matplotlib
import numpy as np
from celery import AsyncResult
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from matplotlib import pyplot, style
from pandas import Series

from .tasks import do_linear_regression


def task_state(request, task_id):
    task = AsyncResult(task_id)

    return JsonResponse({
        'status': task.status,
        'result': task.result
    })


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
    f.clear()
    pyplot.gcf().clear()

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
        return HttpResponse('Wrong filetype', status=400)

    data = [x.decode().strip().split(',')
            for x in time_series_csv.readlines() if not x.decode().startswith('#')]

    x_values, y_values = zip(*data)
    x_values = np.array([x + 1 for x in range(len(x_values))])
    y_values = np.array([float(x) for x in y_values], dtype=np.float64)
    x_predict = int(request.POST.get('x_predicted'), 0)

    task = do_linear_regression.delay(x_values, y_values, x_predict)
    return JsonResponse({'task_id': task.id})
