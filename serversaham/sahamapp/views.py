import base64
import csv
import io
import os
from statistics import mean

import matplotlib
import numpy as np
from serversaham.celery import app
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from matplotlib import pyplot, style
from pandas import Series

from .tasks import do_linear_regression, do_scraping

def index(request):
    return render(request, 'index.html')


def linreg_view(request):
    return render(request, 'linreg.html')


def task_state(request, task_id):
    task = app.AsyncResult(task_id)

    return JsonResponse({
        'status': task.status,
        'result': task.result
    })


def get_chart(requests, perusahaan, durasi):
    """
    Fungsi ini akan menghasilkan image dari data stock seminggu terakhir dari perusahaan tertentu
    :return:
    """
    task = do_scraping.delay(perusahaan, durasi)
    return JsonResponse({'task_id': task.id})



@require_POST
def linreg_process(request):
    time_series_csv = request.FILES.get('time_series_csv')

    if not time_series_csv.name.endswith('csv'):
        return HttpResponse('Wrong filetype', status=400)

    data = [x.decode().strip().split(',')
            for x in time_series_csv.readlines() if not x.decode().startswith('#')]

    x_values, y_values = zip(*data)
    x_predict = int(request.POST.get('x_predicted'), 0)

    task = do_linear_regression.delay(x_values, y_values, x_predict)
    return JsonResponse({'task_id': task.id})
