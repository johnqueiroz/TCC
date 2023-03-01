import json
import pandas as pd
import numpy as np
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder

# Carregar os dados
def read_issues(filename):
 with open("resources/" + filename, "r", encoding="utf-8") as f:
       return json.load(f)

def read_test_cases(filename):
 with open("resources/" + filename, "r", encoding="utf-8") as f:
       return json.load(f)

issues = read_issues("issues.json")
test_cases = read_test_cases("test_cases.json")

# Pré-processamento dos dados
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
   stop_words = set(stopwords.words('english'))
   lemmatizer = WordNetLemmatizer()
   if text is not None:
       tokens = word_tokenize(text.lower())
       words = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words and w not in string.punctuation]
       return ' '.join(words)
   else:
       return ''

for issue in issues:
    issue['description'] = preprocess_text(issue['description'])
    issue['COMMENT'] = preprocess_text(issue['description'])

for test_case in test_cases:
    test_case['TC_Setup'] = preprocess_text(test_case['TC_Setup'])
    test_case['TC_Steps'] = preprocess_text(test_case['TC_Steps'])
    test_case['TC_Expected_Results'] = preprocess_text(test_case['TC_Expected_Results'])


# Vetorização TF-IDF
vectorizer = TfidfVectorizer()

X_train = vectorizer.fit_transform([issue['description'] + ' ' + issue['COMMENT'] for issue in issues]).toarray()
y_train = np.array([issue['issue_key'] for issue in issues])

# Converter labels para valores numéricos
le = LabelEncoder()
y_train = le.fit_transform(y_train)


X_test = vectorizer.transform([test_case['TC_Setup'] + ' ' + test_case['TC_Steps'] + ' ' + test_case['TC_Expected_Results'] for test_case in test_cases])
y_test = np.array([test_case['Test_Case'] for test_case in test_cases])

y_test = le.fit_transform(y_test)

# Treinamento e avaliação do modelo
clf = MultinomialNB()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

# Avaliação do modelo
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='weighted')
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)

print("Accuracy:", accuracy)
print("f1:", f1)
print("precision:", precision)
print("recall:", recall)