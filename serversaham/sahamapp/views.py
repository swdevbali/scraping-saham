import matplotlib
from django.http import HttpResponse
from django.shortcuts import render


def get_chart(request, perusahaan, durasi):

    #perusahaan = 'BBCA'
    #durasi = '1Y'
    """

    :return:
    """
    import requests
    import json
    import pprint
    import time
    import io

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

    f = matplotlib.figure.Figure()
    series = Series.from_csv('data.csv', header=0, sep=',')
    pyplot.clf()
    pyplot.plot(series)
    #pyplot.show()

    #Django fix: create in buffer first
    buf = io.BytesIO()
    pyplot.savefig(buf, format='png')
    pyplot.close(f)

    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response

def index(request):
    return render(request, 'index.html')

