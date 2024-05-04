import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.model_selection import cross_val_score
import numpy as np
import os
import sys
# Set the working directory
os.chdir('data_analysis')

# Load HRV data (replace 'hrv.csv' with your actual file path)
hrv_data = pd.read_csv('hrv_baseline_balanced.csv')

# Load painting ratings data (replace 'ratings.csv' with your actual file path)
ratings_data = pd.read_csv('ratings.csv')

merged_data = hrv_data.merge(ratings_data, on=['Id', 'userId', 'paintingId'], how='inner')


# Or Numpy arrays?
X = merged_data.drop(['Id','userId', 'paintingId', 'mode', 'rating'], axis=1)
y = merged_data['rating']

# Standardize features
scaler = StandardScaler()


# Get subject IDs as groups for LOSO
groups = merged_data['Id'] 

# Leave-One-Subject-Out cross-validation
logo = LeaveOneGroupOut()

# Initialize SVM classifier
svm_model = SVC(kernel='linear', C=1.0)  

# Perform Leave-One-Subject-Out cross-validation
for train_index, test_index in logo.split(X, y, groups):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
        
    svm_model.fit(X_train_scaled, y_train)
    accuracy = svm_model.score(X_test_scaled, y_test)
    print(f'Accuracy for subject {groups[test_index].values[0]}: {accuracy}')

# Evaluate model performance using LOSO and regularization

scores = cross_val_score(svm_model, X, y, groups=groups, cv=logo)
print(f'Mean Accuracy: {scores.mean()}')

# Train final model on full dataset
svm_model.fit(X, y)






