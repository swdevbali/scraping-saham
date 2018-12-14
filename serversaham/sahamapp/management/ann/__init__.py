import pandas as pd

#ACQUISITION
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']
irisdata = pd.read_csv(url, names=names)
print(irisdata.head())

#PREPROCESSING
X = irisdata.iloc[:, 0:4] #Feature
y = irisdata.select_dtypes(include=[object]) #Target
print(y.head())
print(y.Class.unique())

#Beri label untuk data target
from sklearn import preprocessing
le = preprocessing.LabelEncoder()

#Ubah data tersebut menjadi numerik
y = y.apply(le.fit_transform)
print(y.Class.unique())

#Train, avoid overfitting
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

#Feature scaling
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

#Train!
from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
mlp.fit(X_train, y_train.values.ravel())

#Predict
predictions = mlp.predict(X_test)

#Evaluate
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))