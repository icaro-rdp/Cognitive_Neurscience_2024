import pandas as pd
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import accuracy_score
import os
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
# Set the working directory
os.chdir('data_analysis')

# Load HRV data 
hrv_data = pd.read_csv('hrv_baseline_balanced.csv')
ratings_data = pd.read_csv('ratings.csv')
merged_data = hrv_data.merge(ratings_data, on=['Id', 'userId', 'paintingId'], how='inner')

# Drop unnecessary columns
X = merged_data.drop(['Id','userId', 'paintingId', 'mode', 'rating'], axis=1)
y = merged_data['rating'].apply(lambda x: 1 if x > 5 else 0)

# Check corr matrix
plt.figure(figsize=(12, 10))
cor = X.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.CMRmap_r)


def correlated_features(dataset, threshold):
    col_corr = set()  # Set of all the names of correlated columns
    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > threshold: # we are interested in absolute coeff value
                colname = corr_matrix.columns[i]  # getting the name of column
                col_corr.add(colname)
    return col_corr

corr_features = correlated_features(X, 0.8)
# Drop correlated features
X = X.drop(corr_features, axis=1)

# Standardize features
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = y.values

# Leave-one-out cross-validation
loo = LeaveOneOut()

# Initialize models
svm_model = SVC(kernel='poly', C=1.0)  
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
svm_scores = []
rf_scores = []
for i, (train_index, test_index) in enumerate(loo.split(X)):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    svm_model.fit(X_train, y_train)
    svm_pred = svm_model.predict(X_test)
    svm_scores.append(accuracy_score(y_test, svm_pred))

    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_scores.append(accuracy_score(y_test, rf_pred))


print(f'SVM Average accuracy: {np.mean(svm_scores)}')
print(f'Random forest Average accuracy: {np.mean(rf_scores)}')
