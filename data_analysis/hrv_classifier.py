import pandas as pd
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
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

merged_data.head()

# Drop unnecessary columns
X = merged_data.drop(['Id','userId', 'paintingId', 'mode', 'rating'], axis=1)
y = merged_data['rating'].apply(lambda x: 1 if x > 5 else 0)

# Check Dataset inbalances
binary_values = y.value_counts()
# Get the baseline
baseline_acc = binary_values.max()/len(y)

# Check corr matrix
plt.figure(figsize=(12, 10))
cor = X.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.CMRmap_r)
plt.show()

def correlated_features(dataset, threshold):
    col_corr = set()
    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > threshold:
                colname = corr_matrix.columns[i]
                col_corr.add(colname)
    return col_corr

corr_features = correlated_features(X, 0.85)
# Drop correlated features
X = X.drop(corr_features, axis=1)

X.head()

# get y values
y = y.values
X = X.values

# Leave-one-out cross-validation
loo = LeaveOneOut()

# Initialize models
svm_model = SVC(kernel='poly', C=1.0,random_state=0)
rf_model = RandomForestClassifier(n_estimators=20, random_state=42)
kn_model = KNeighborsClassifier(n_neighbors=5)
svm_scores = []
rf_scores = []
kn_scores = []
for i, (train_index, test_index) in enumerate(loo.split(X)):
    scaler = StandardScaler()
    X_train =  scaler.fit_transform(X[train_index])
    X_test = scaler.transform(X[test_index])
    y_train, y_test = y[train_index], y[test_index]
    # SVM
    svm_model.fit(X_train, y_train)
    svm_pred = svm_model.predict(X_test)
    svm_scores.append(accuracy_score(y_test, svm_pred))
    # RF
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_scores.append(accuracy_score(y_test, rf_pred))
    # KN
    kn_model.fit(X_train, y_train)
    kn_pred = rf_model.predict(X_test)
    kn_scores.append(accuracy_score(y_test, kn_pred))

print(f'SVM Average accuracy: {np.mean(svm_scores)}')
print(f'Random forest Average accuracy: {np.mean(rf_scores)}')
print(f'KNeighbors Average accuracy: {np.mean(kn_scores)}')