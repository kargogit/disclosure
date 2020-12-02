import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from joblib import dump

datasetPath = os.path.join( r"DatasetPrep", r"Dataset" )
featureFramePath = os.path.join( datasetPath, r"topFeaturesTFIDF.csv" )

featureFrame = pd.read_csv(featureFramePath)
X = featureFrame.iloc[:, :-1].values
Y = featureFrame.iloc[:, -1].values

X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size = 0.18, random_state = 69)
Classifier = LogisticRegression( solver = "newton-cg", multi_class = "ovr", n_jobs = -1, max_iter = 180 )
Classifier.fit( X_Train, Y_Train )

print( "Test Accuracy Score : %.2f" % Classifier.score( X_Test, Y_Test ) )

modelPath = os.path.join( r"ML", r"Models", r"LogRegClassifier.pkl" )
dump(Classifier, modelPath)
