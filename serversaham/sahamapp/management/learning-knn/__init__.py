import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']
#https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data
dataset = pd.read_csv('iris.csv', names=names)
# dataset = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', names=names)
print(dataset.head())

X = dataset.iloc[:, :-1].values #ambil semua baris, kurangi 1 kolom dari kanan
y = dataset.iloc[:, 4].values # ambil semua baris, kolom ke-4
print(X)
print(y)

# SPLIT
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# Normalisasi, sehingga data tidak menyebar terlalu besar, Gaussian
#https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# BUAT MODEL
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=5)

# FITTING
classifier.fit(X_train, y_train)

# MENCARI NILAI K TERBAIK
error = []

# Calculating error for K values between 1 and 40
for i in range(1, 40):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train)
    pred_i = knn.predict(X_test)
    error.append(np.mean(pred_i != y_test))

plt.figure(figsize=(12, 6))
plt.plot(range(1, 40), error, color='red', linestyle='dashed', marker='o', markerfacecolor='blue', markersize=10)
plt.title('Error Rate K Value')
plt.xlabel('K Value')
plt.ylabel('Mean Error')
plt.show()

# PREDIKSI
y_pred = classifier.predict(X_test)

# EVALUASI
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
