# -*- coding: utf-8 -*-
"""Ensemble_espData.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18mErQ3YBq1Pp9V4kUZFqBzHtoALFtmJ-
"""

import pandas as pd
# from keras.models import Sequential
# from keras.layers import Dense
# import keras
import xgboost
# from tensorflow.keras import layers
# import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier

# tf.config.experimental_run_functions_eagerly(True)

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report

# from sklearn.metrics import plot_confusion_matrix 
import numpy as np
from sklearn.linear_model import RidgeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import GradientBoostingClassifier
from numpy import mean
from numpy import std
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
import time
import pickle

df=pd.read_csv('esp_all_denoised_D1.csv')
df.shape

Dataset_X=df.iloc[:,0:51]
Dataset_Y=df.iloc[:,51]
print(Dataset_X.shape)
print(Dataset_Y.shape)



Dataset_Y.unique

X_train, X_test, Y_train, Y_test = train_test_split(Dataset_X, Dataset_Y, test_size=0.2,random_state=42)

clf1=RidgeClassifier()
# clf1=GaussianNB()

clf2=LinearDiscriminantAnalysis()
clf3=RandomForestClassifier(n_estimators=100,max_depth=37,random_state=42)
ensemble = VotingClassifier(estimators=[('gnb', clf1), ('lda', clf2), ('rfc', clf3)], voting='hard')

start=time.time()
clf=ensemble.fit(X_train, Y_train)
stop=time.time()
print(f"Training time: {stop - start}s")

start1=time.time()
Y_pred = ensemble.predict(X_test)
stop1=time.time()

print(f"Prediction time time: {stop1 - start1}s")
print("Number of mislabelled points=",(Y_test != Y_pred).sum())
# Model Accuracy
print("Accuracy of Decision Tree classifier:",metrics.accuracy_score(Y_test, Y_pred))

# Plot non-normalized confusion matrix

title= "Normalized Confusion matrix"
confusion_matrix=metrics.confusion_matrix(Y_test,Y_pred)
disp = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix)
#disp.ax_.set_title(title)

#print(title)
print(disp.confusion_matrix)

plt.show()

cv = KFold(n_splits=10, random_state=42, shuffle=True)

# evaluate model
scores= cross_val_score(ensemble, Dataset_X, Dataset_Y, scoring='accuracy', cv=cv, n_jobs=-1)
# report performance
print('Accuracy: %.3f (%.3f)' % (mean(scores), std(scores)))



