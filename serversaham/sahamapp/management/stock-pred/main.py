from matplotlib import pyplot
import pandas as pd
import numpy as np
import datetime

from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, svm
from sklearn import model_selection as cross_validation

df = pd.read_csv('data.csv', delimiter=',', header=0)
print('1', df)


df = df[['Value']]
print('2', df)
forecast_out = 30

df['Prediction'] = df[['Value']].shift(-forecast_out)
print('3', df)

X = np.array(df.drop(['Prediction'], 1))
X = preprocessing.scale(X)

X_forecast = X[-forecast_out:]
X = X[:-forecast_out]

y = np.array(df['Prediction'])
y = y[:-forecast_out]

#TRAIN
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.2)

clf = LinearRegression()
clf.fit(X_train,y_train)

confidence = clf.score(X_test, y_test)
print("confidence: ", confidence)

forecast_prediction = clf.predict(X_forecast)
print(forecast_prediction)
pyplot.plot(forecast_prediction)
pyplot.show()