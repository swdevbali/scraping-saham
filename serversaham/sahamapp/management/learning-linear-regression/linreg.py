# https://enlight.nyc/projects/linear-regression
"""
 y = mx + b

 This equation describes the linear relationship between x and y, with m being our slope and b being our y-intercept.
 In machine learning, our y value is the predicted label, b is the bias, the slope m is the weight, and the x value is a feature (input).

"""
from statistics import mean
import numpy as np

x_values = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=np.float64)
y_values = np.array([1, 4, 1, 6, 4, 7, 4, 6, 10, 8], dtype=np.float64)

def best_fit_line(x_values, y_values):
    m = (((mean(x_values) * mean(y_values)) - mean(x_values * y_values)) /
         ((mean(x_values) * mean(x_values)) - mean(x_values * x_values)))

    b = mean(y_values) - m * mean(x_values)

    return m, b #tupple

# y = mx + b
m, b = best_fit_line(x_values, y_values)

print("regression line: " + "y = " + str(round(m, 2)) + "x + " + str(round(b, 2)))

# Prediction
x_prediction = 15
y_prediction = (m * x_prediction) + b
print("predicted coordinate: (" + str(round(x_prediction, 2)) + "," + str(round(y_prediction, 2)) + ")")

# y values of regression line
regression_line = [(m * x) + b for x in x_values]
print(regression_line)

# Plotting
import matplotlib.pyplot as plt
from matplotlib import style

style.use('seaborn')

plt.title('Linear Regression')
plt.scatter(x_values, y_values, color='#5b9dff', label='data')
plt.scatter(x_prediction, y_prediction, color='#fc003f', label="predicted")
plt.plot(x_values, regression_line, color='000000', label='regression line')
plt.legend(loc=4)
plt.show("graph.png")
