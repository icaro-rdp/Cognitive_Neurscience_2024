import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.model_selection import cross_val_score

# Load HRV data (replace 'hrv.csv' with your actual file path)
hrv_data = pd.read_csv('hrv.csv')

# Load painting ratings data (replace 'ratings.csv' with your actual file path)
ratings_data = pd.read_csv('ratings.csv')

# Merge datasets based on userId and paintingId (assuming they are the common columns)
merged_data = hrv_data.merge(ratings_data, on=['userId', 'paintingId'])

# Define features and target variable
X = merged_data.drop(['userId', 'paintingId', 'mode', 'rating'], axis=1)
y = merged_data['rating']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Get subject IDs as groups for LOSO
groups = merged_data['userId'] 

# Leave-One-Subject-Out cross-validation
logo = LeaveOneGroupOut()

# Initialize SVM classifier
svm_model_L1 = SVC(kernel='linear', penalty='l1', C=1.0)  
svm_model_L2 = SVC(kernel='linear', penalty='l2', C=1.0)  

# Perform Leave-One-Subject-Out cross-validation
for train_index, test_index in logo.split(X, y, groups):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    svm_model_L1.fit(X_train_scaled, y_train)
    accuracy = svm_model_L1.score(X_test_scaled, y_test)
    print(f'L1 Accuracy for subject {groups[test_index].values[0]}: {accuracy}')

    
    svm_model_L2.fit(X_train_scaled, y_train)
    accuracy = svm_model_L2.score(X_test_scaled, y_test)
    print(f'L2 Accuracy for subject {groups[test_index].values[0]}: {accuracy}')

# Evaluate model performance using LOSO and regularization
scores = cross_val_score(svm_model_L1, X, y, groups=groups, cv=logo)
print(f'Mean L1 Accuracy: {scores.mean()}')

scores = cross_val_score(svm_model_L2, X, y, groups=groups, cv=logo)
print(f'Mean L2 Accuracy: {scores.mean()}')

# Train final model on full dataset
svm_model_L1.fit(X, y)
svm_model_L2.fit(X, y)


