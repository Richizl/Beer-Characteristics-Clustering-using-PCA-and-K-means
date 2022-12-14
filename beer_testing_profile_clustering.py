# -*- coding: utf-8 -*-
"""Beer testing profile clustering

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LCD_LiWljlctzfya2H9A096g-EJNMqhx

# Finding clusters on Beer testing profiles, PCA and K-mean
"""

# Ricardo Zepeda - A01174203 
# October 31, 2022

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, adjusted_rand_score

"""Access to Drive"""

from google.colab import drive
drive.mount('/content/drive')

"""Navigate to the folder in drive where you want to work"""

# Commented out IPython magic to ensure Python compatibility.
!pwd  #show current path

#change floder
# %cd "/content/drive/MyDrive/Intelligent Systems/Project 2: Alcoholism"

!pwd  #show current path
!ls   #show files in current path

"""Link to dataset"""

#Read data set
df=pd.read_csv('beer_data_set.csv')
df.head()

"""Choosing variables"""

#Getting rid of non trivial variables
df=df.drop(['Name','key', 'Style','Brewery','Description','Ave Rating'], axis=1)
df

"""Normalizing data"""

from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing

min_max_scaler = preprocessing.MinMaxScaler()
data_minmax = min_max_scaler.fit_transform(df)
data_minmax

df = pd.DataFrame(data_minmax, columns=['Style Key', 'ABV','Min IBU', 'Max IBU','Astringency',	'Body',	'Alcohol',	'Bitter',	'Sweet',	'Sour',	'Salty',	'Fruits',	'Hoppy',	'Spices',	'Malty'])
df.head()

from sklearn.decomposition import PCA

pca = PCA(n_components=5)
pca.fit(df)

df_PCA = pca.transform(df)

df_PCA = pd.DataFrame(df_PCA)
df_PCA.index = df.index
df_PCA.columns = ['PCA1','PCA2','PCA3','PCA4','PCA5']
df_PCA.head()

pca.explained_variance_ratio_

df_PCA.plot(
        kind='scatter',
        x='PCA1',y='PCA2',
        figsize=(16,8))

"""Clustering"""

reduced_data = PCA(n_components=2).fit_transform(df)
kmeans = KMeans(init='k-means++', n_clusters=2, n_init=10)
kmeans.fit(reduced_data)

#choosing centers (elbow method)
kmeans_kwargs = {
    "init": "random",
    "n_init": 10,
    "max_iter": 300,
    "random_state": 42,
}

# A list holds the SSE values for each k
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(df)
    sse.append(kmeans.inertia_)

plt.style.use("fivethirtyeight")
 plt.plot(range(1, 11), sse)
 plt.xticks(range(1, 11))
 plt.xlabel("Number of Clusters")
 plt.ylabel("SSE")
 plt.show()

reduced_data = PCA(n_components=2).fit_transform(df)
kmeans = KMeans(init='k-means++', n_clusters=5, n_init=10)
kmeans.fit(reduced_data)

# Step size of the mesh. Decrease to increase the quality of the VQ.
h = 0.02     # point in the mesh [x_min, x_max]x[y_min, y_max].

# Plot the decision boundary. For that, we will assign a color to each
x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obtain labels for each point in mesh. Use last trained model.
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.figure(1)
plt.clf()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.Paired,
           aspect='auto', origin='lower')

plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
# Plot the centroids as a white X
centroids = kmeans.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
#plt.title('K-means clustering on beer dataset (PCA-reduced data)\n','Centroids are marked with white cross')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
plt.show()

from sklearn.cluster import KMeans   
kmeans = KMeans(n_clusters=10)
clusters = kmeans.fit(df)

df_PCA['cluster'] = pd.Series(clusters.labels_, index=df_PCA.index)

df_PCA.plot(
        kind='scatter',
        x='PCA1',y='PCA2',
        c=df_PCA.cluster.astype(np.float),
        figsize=(16,8))

kmeans = KMeans(
    n_clusters = 5,
    init="random",
    n_init=10,
    max_iter=300,
    random_state=42
)
kmeans.fit(df_PCA)

kmeans.inertia_