import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
The attributes are Variance of wavelet transformed image, 
curtosis of the image, entropy, and skewness of the image
"""
dataset = pd.read_csv("bill_authentication.csv")
print(dataset.shape)

print(dataset.head())

#PREPARE DATA
X = dataset.drop('Class', axis=1)
y = dataset['Class']

#SPLIT
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

#TRAIN
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

#PREDICT
y_pred = classifier.predict(X_test)

#EVALUTE
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))