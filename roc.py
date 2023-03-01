import json
import string
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
import uuid

# Define functions to read data and preprocess text
def read_issues(filename):
   with open("resources/" + filename, "r", encoding="utf-8") as f:
       issues = json.load(f)
   return [{'ID': str(uuid.uuid4()), 'description': issue['description'], 'COMMENT': issue['COMMENT']} for issue in issues]

def read_test_cases(filename):
   with open("resources/" + filename, "r", encoding="utf-8") as f:
       test_cases = json.load(f)
   return [{'ID': str(uuid.uuid4()), 'TC_Setup': test_case['TC_Setup'], 'TC_Steps': test_case['TC_Steps'], 'TC_Expected_Results': test_case['TC_Expected_Results']} for test_case in test_cases]

def preprocess_text(text):
   stop_words = set(stopwords.words('english'))
   if text is not None:
       tokens = word_tokenize(text.lower())
       words = [w for w in tokens if w not in stop_words and w not in string.punctuation]
       return ' '.join(words)

def preprocess_issues(issues):
   for issue in issues:
       issue['description'] = preprocess_text(issue['description'])
       issue['COMMENT'] = preprocess_text(issue['COMMENT'])
   return issues

def preprocess_test_cases(test_cases):
   for test_case in test_cases:
       test_case['TC_Setup'] = preprocess_text(test_case['TC_Setup'])
       test_case['TC_Steps'] = preprocess_text(test_case['TC_Steps'])
       test_case['TC_Expected_Results'] = preprocess_text(test_case['TC_Expected_Results'])
   return test_cases

# Read data from JSON files and preprocess text
issues = read_issues("issues.json")
test_cases = read_test_cases("test_cases.json")
issues = preprocess_issues(issues)
test_cases = preprocess_test_cases(test_cases)

# Convert preprocessed data to dataframes
issue_df = pd.DataFrame(issues)
test_case_df = pd.DataFrame(test_cases)

# Merge dataframes and create X_train and y_train arrays
merged_df = pd.merge(issue_df, test_case_df, on=["ID"], how="outer")

text_fields = []
for index, row in merged_df.iterrows():
    text_fields.append(row['description'])
    text_fields.append(row['COMMENT'])
    text_fields.append(row['TC_Setup'])
    text_fields.append(row['TC_Steps'])
    text_fields.append(row['TC_Expected_Results'])

labels = []
for index, row in merged_df.iterrows():
    labels.append(row['ID'])

X_train = np.array(text_fields)
y_train = np.array(labels)

# Train a random forest classifier and make predictions
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_train)

# Evaluate model performance using metrics
accuracy = accuracy_score(y_train, y_pred)
f1 = f1_score(y_train, y_pred, average='macro')
precision = precision_score(y_train, y_pred, average='macro')
recall = recall_score(y_train, y_pred, average='macro')
roc_auc = roc_auc_score(y_train, y_pred, average='macro')

print("Accuracy:", accuracy)
print("F1 Score:", f1)
print("Precision:", precision)
print("ROC AUC:", roc_auc)
print("recall:", recall)