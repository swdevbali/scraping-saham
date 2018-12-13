import base64
import io
from statistics import mean

from celery import shared_task
from matplotlib import pyplot, style


@shared_task
def do_linear_regression(x, y, x_predict):
    """
    celery task for linear regression
    """
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
    pyplot.scatter(x, y, color='#fc003f', label="predicted")
    pyplot.plot(x, regression_line,
                color='000000', label='regression line')
    pyplot.legend(loc=4)

    # Django fix: create in buffer first
    buf = io.BytesIO()
    pyplot.savefig(buf)
    pyplot.gcf().clear()

    return base64.b64encode(buf.getvalue()).decode()
