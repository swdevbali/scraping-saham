import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

#ACQUITISION
X = np.array([[5,3],
     [10,15],
     [15,12],
     [24,10],
     [30,45],
     [85,70],
     [71,80],
     [60,78],
     [55,52],
     [80,91],])

plt.scatter(X[:,0],X[:,1], label='True Position')
plt.show()

#FIT MODEL
kmeans = KMeans(n_clusters=4)
kmeans.fit(X)

#TITIK TENGAH SEMUA KLASTER YANG TERCIPTA
print(kmeans.cluster_centers_)

#ORDER LABEL DARI CLUSTER TERSEBUT
print(kmeans.labels_)

#DISPLAY
plt.scatter(X[:,0],X[:,1], c=kmeans.labels_, cmap='rainbow')
plt.show()
